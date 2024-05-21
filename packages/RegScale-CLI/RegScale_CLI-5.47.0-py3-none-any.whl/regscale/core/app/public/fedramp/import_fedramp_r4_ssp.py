"""Import FedRAMP Revision 4 SSP XML into RegScale"""

# flake8: noqa
from datetime import datetime
from typing import Any, Dict, Tuple, Generator

from lxml import etree
from pydantic import ValidationError

from regscale.core.app.api import Api
from regscale.core.app.application import Application
from regscale.core.app.logz import create_logger
from regscale.core.app.public.fedramp.fedramp_traversal import FedrampTraversal
from regscale.core.app.public.fedramp.metadata import parse_metadata
from regscale.core.app.public.fedramp.reporting import write_events
from regscale.core.app.public.fedramp.system_characteristics import (
    parse_minimum_ssp,
    parse_system_characteristics,
)
from regscale.core.app.public.fedramp.system_control_implementations import (
    fetch_implementations,
)
from regscale.core.app.public.fedramp.system_implementation import (
    parse_system_implementation,
)
from regscale.core.app.utils.app_utils import get_file_name
from regscale.core.app.utils.regscale_utils import create_new_data_submodule
from regscale.models.regscale_models.files import File
from regscale.models.regscale_models.securityplans import SecurityPlan

logger = create_logger()


def parse_and_load_xml_rev4(
    context: Any, file_path: str, catalogue_id: int, filename: str = "Sample.xml"
) -> Generator[Tuple[str, Dict, Dict], None, None]:
    """
     Parse and load XML Rev4

    :param Any context: Flask app context
    :param str file_path: Path to XML file
    :param int catalogue_id: Catalogue ID user selected
    :param str filename: Name of file that will be uploaded to RegScale
    :yields Generator[Tuple[str, Dict, Dict]]: Tuple of filename and upload results
    :return: Tuple of filename and upload results
    :rtype: Generator[Tuple[str, Dict, Dict]]
    """
    # Process with app request context to yield partial content to the browser
    with context:
        logger.info(f"Parsing and loading file {file_path}.")
        events_list = []  # will store events as they take place throughout the import process
        app = Application()
        api = Api()
        events_list = []  # will store events as they take place throughout the import process

        ns = {
            "ns1": "http://csrc.nist.gov/ns/oscal/1.0",
            "oscal": "http://csrc.nist.gov/ns/oscal/1.0",
            "fedramp": "https://fedramp.gov/ns/oscal",
        }

        yield "<div>Creating Security Plan...</div>"
        tree = etree.parse(file_path)
        root = tree.getroot()
        ssp_uuid = root.attrib["uuid"]
        new_ssp = {"uuid": ssp_uuid}

        # Create fedramp traversal object.
        trv = FedrampTraversal(
            api=api,
            root=root,
            namespaces=ns,
        )
        # --- Set the catalogue_id on the traversal object.
        trv.catalogue_id = catalogue_id

        # 0. Create the EMPTY SSP that we need for later posts.
        ssp_id = parse_minimum_ssp(api=api, root=root, new_ssp=new_ssp, ns=ns, events_list=events_list)
        logger.info(f"Created new SSP in RegScale with ID {ssp_id}.")
        yield f"<div>Created new SSP in RegScale with ID {ssp_id}.</div>"
        # --- Set the ssp_id on the traversal object.
        trv.ssp_id = ssp_id

        # 1. Parse the <metadata> tag
        parse_metadata(trv)
        yield "<div>Parsing metadata...</div>"

        # upload xml file & data submodules in the SSP
        attach_artifact_to_ssp(trv=trv, file_path=file_path)
        yield "<div>Attaching OSCAL XML file to SSP</div>"

        # 2. Parse the <system-characteristics> tag
        parse_system_characteristics(ssp_id=ssp_id, root=root, ns=ns, events_list=events_list)
        logger.info("System characteristics parsed successfully.")

        # 3. Parse the <system-implementation> tag!
        yield "<div>Creating control implementations (this may take several minutes)...</div>"
        parse_system_implementation(trv)
        yield "<div>Control implementations created.</div>"

        # 4. TODO <control-implementation>
        # parse_control_implementation()

        # 5. Parse <back-matter>
        # parse_back_matter()

        # Write the events.
        resultfile = "artifacts/import-results.csv"
        now = datetime.now()
        resultfile = resultfile.replace(".", "-SSP-{0}_".format(ssp_id) + now.strftime("%Y%m%d."))

        # final_list = [*events_list, *trv.errors, *trv.infos]
        # write_events(final_list, resultfile)

        # TODO: review with Josh
        # If data is incomplete This fails w/ 500 error ( which means the json string being received by the server is either malformed or missing something
        logger.info("Uploading SSP to RegScale...")
        yield "<div>Uploading source SSP to RegScale...</div>"
        try:
            ssp = SecurityPlan(**new_ssp)
        except ValidationError as exc:
            logger.error(f"Failed to validate: {exc}")
            return resultfile, {
                "status": "failed",
            }
        # you can create a new ssp without the userId populated, but we normally use the userId from init.yaml
        ssp.systemOwnerId = app.config["userId"]
        ssp.id = ssp_id
        new_ssp = ssp.update_ssp(api=api, return_id=False)
        new_ssp_id = new_ssp.id
        oscal_implementations = fetch_implementations(trv=trv, root=root, ssp=new_ssp)
        if oscal_implementations:
            implementation_results = {
                "status": "success",
                "ssp_id": new_ssp_id,
                "implementations_loaded": len(oscal_implementations),
            }

        # upload_results["implementations"] = implementation_results
        """ properties handling is getting moved. Comment out for now.
        properties_response = Properties.create_properties_from_list(
            parent_id=new_ssp_id,
            parent_module="securityplans",
            properties_list=properties_list,
        )
        upload_results["properties_response"] = properties_response
        """
        upload_results = {
            "ssp_id": new_ssp_id,
            "implementations_loaded": len(oscal_implementations),
            "ssp_title": new_ssp.systemName,
        }
        logger.info(f"Finished uploading SSP {ssp_id}")

        final_list = [*events_list, *trv.errors, *trv.infos]
        write_events(final_list, resultfile)

        # upload privacyImpactAssessment. If is None then dont.
        logger.info(f"Uploading validation results for import SSP {new_ssp_id}")
        attach_artifact_to_ssp(trv=trv, file_path=resultfile)
        yield resultfile, upload_results, oscal_implementations


def attach_artifact_to_ssp(trv: FedrampTraversal, file_path: str) -> None:
    """
    Function to attach the XML file to the SSP's data and file submodules in RegScale
    :param FedrampTraversal trv: FedrampTraversal object
    :param str file_path: Path to the file to upload
    :rtype: None
    """
    # upload xml file to SSP
    if File.upload_file_to_regscale(
        file_name=file_path,
        parent_id=trv.ssp_id,
        parent_module="securityplans",
        api=trv.api,
        return_object=True,
    ):
        trv.log_info(
            {
                "record_type": "file",
                "event_msg": f"Uploaded file '{get_file_name(file_path)}' to SSP# {get_file_name(file_path)}"
                "File module in RegScale.",
            }
        )
    else:
        trv.log_error(
            {
                "record_type": "file",
                "event_msg": f"Failed to upload file '{get_file_name(file_path)}' to SSP# {trv.ssp_id} "
                "File module in RegScale.",
            }
        )
    if create_new_data_submodule(
        api=trv.api,
        parent_id=trv.ssp_id,
        parent_module="securityplans",
        file_path=file_path,
    ):
        trv.log_info(
            {
                "record_type": "Data",
                "event_msg": f"Uploaded file '{get_file_name(file_path)}' to SSP# {get_file_name(file_path)}"
                "Data module in RegScale.",
            }
        )
    else:
        trv.log_error(
            {
                "record_type": "Data",
                "event_msg": f"Failed to upload file '{get_file_name(file_path)}' to SSP# {trv.ssp_id} "
                " Data module in RegScale.",
            }
        )
