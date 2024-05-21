"""fedramp v5 docx parser"""

import datetime
import logging
import os
import sys
import zipfile
from dataclasses import dataclass
from tempfile import gettempdir
from typing import List, Dict, Optional, Tuple, Any

from dateutil.relativedelta import relativedelta

from regscale.core.app.api import Api
from regscale.core.app.application import Application
from regscale.core.app.public.fedramp.appendix_parser import AppendixAParser
from regscale.core.app.public.fedramp.docx_parser import SSPDocParser
from regscale.core.app.utils.app_utils import get_current_datetime
from regscale.models import (
    SecurityPlan,
    PortsProtocol,
    LeveragedAuthorization,
    StakeHolder,
    Profile,
    User,
    File,
    SecurityControl,
    ProfileMapping,
    ControlImplementation,
    Parameter,
    ControlParameter,
    ParameterDataTypes,
    ControlImplementationStatus,
    ImplementationObjective,
    ImplementationOption,
    ControlObjective,
)

DEFAULT_STATUS = ControlImplementationStatus.NotImplemented.value

logger = logging.getLogger(__name__)


@dataclass
class Person:
    """
    Represents a person.
    """

    name: str
    phone: str
    email: str
    title: str
    user_id: Optional[str] = None


@dataclass
class Organization:
    """
    Represents an organization.
    """

    name: str
    address: str
    point_of_contact: Person


@dataclass
class PreparedBy:
    """
    Represents the prepared by information.
    """

    name: str
    street: str
    building: str
    city_state_zip: str


@dataclass
class SSPDoc:
    """
    Represents an SSP document.
    """

    name: str
    fedramp_id: str
    service_model: str
    digital_identity_level: str
    fips_199_level: str
    date_fully_operational: str
    deployment_model: str
    authorization_path: str
    description: str
    expiration_date: Optional[str] = None
    date_submitted: Optional[str] = None
    approval_date: Optional[str] = None
    csp_name: Optional[str] = None
    csp_street: Optional[str] = None
    csp_building: Optional[str] = None
    csp_city_state_zip: Optional[str] = None
    three_pao_name: Optional[str] = None
    three_pao_street: Optional[str] = None
    three_pao_building: Optional[str] = None
    three_pao_city_state_zip: Optional[str] = None
    version: str = "1.0"


@dataclass
class LeveragedService:
    """
    Represents a leveraged service.
    """

    fedramp_csp_name: str
    cso_name: str
    auth_type_fedramp_id: str
    agreement_type: str
    impact_level: str
    data_types: str
    authorized_user_authentication: str


@dataclass
class LeveragedServices:
    """
    Represents a list of leveraged services.
    """

    leveraged_services: List[LeveragedService]


@dataclass
class PortsAndProtocolData:
    """
    Represents ports and protocol data.
    """

    service: str
    port: int
    start_port: int
    end_port: int
    protocol: str
    ref_number: str
    purpose: str
    used_by: str


@dataclass
class ParamData:
    """
    Represents parameter data.
    """

    control_id: str
    parameter: Optional[str]
    parameter_value: str


def process_company_info(list_of_dicts: List[Dict[str, str]]) -> Organization:
    """
    Processes the company information table.
    :param List[Dict[str, str]] list_of_dicts: The table to process.
    :return: An Organization object representing the company information.
    :rtype: Organization
    """
    company_info = merge_dicts(list_of_dicts, True)

    person = Person(
        name=company_info.get("Name"),
        phone=company_info.get("Phone Number"),
        email=company_info.get("Email Address"),
        title="System Owner",
    )

    return Organization(
        name=company_info.get("Company / Organization"),
        address=company_info.get("Address"),
        point_of_contact=person,
    )


def process_ssp_info(list_of_dicts: List[Dict[str, str]]) -> SSPDoc:
    """
    Processes the SSP information table.

    :param List[Dict[str, str]] list_of_dicts: The table to process.
    :return: An SSPDoc object representing the SSP information.
    :rtype: SSPDoc
    """
    ssp_info = merge_dicts(list_of_dicts, True)
    # print(ssp_info)

    today_dt = datetime.date.today()
    expiration_date = datetime.date(today_dt.year + 3, today_dt.month, today_dt.day).strftime("%Y-%m-%d %H:%M:%S")

    return SSPDoc(
        name=ssp_info.get("CSP Name:"),
        fedramp_id=ssp_info.get("FedRAMP Package ID:"),
        service_model=ssp_info.get("Service Model:"),
        digital_identity_level=ssp_info.get("Digital Identity Level (DIL) Determination (SSP Appendix E):"),
        fips_199_level=ssp_info.get("FIPS PUB 199 Level (SSP Appendix K):"),
        date_fully_operational=ssp_info.get("Fully Operational as of:"),
        deployment_model=ssp_info.get("Deployment Model:"),
        authorization_path=ssp_info.get("Authorization Path:"),
        description=ssp_info.get("General System Description:"),
        expiration_date=ssp_info.get("Expiration Date:", expiration_date),
        date_submitted=ssp_info.get("Date Submitted:", get_current_datetime()),
        approval_date=ssp_info.get("Approval Date:", get_current_datetime()),
    )


def build_leveraged_services(leveraged_data: List[Dict[str, str]]) -> List[LeveragedService]:
    """
    Processes the leveraged services table.

    :param List[Dict[str, str]] leveraged_data: The table to process.
    :return: A list of LeveragedService objects representing the leveraged services.
    :rtype: List[LeveragedService]
    """
    services = []
    for row in leveraged_data:
        service = LeveragedService(
            fedramp_csp_name=row.get("CSP/CSO Name (Name on FedRAMP Marketplace)"),
            cso_name=row.get(
                "CSO Service (Names of services and features - services from a single CSO can be all listed in one cell)"
            ),
            auth_type_fedramp_id=row.get("Authorization Type (JAB or Agency) and FedRAMP Package ID #"),
            agreement_type=row.get("Nature of Agreement"),
            impact_level=row.get("Impact Level (High, Moderate, Low, LI-SaaS)"),
            data_types=row.get("Data Types"),
            authorized_user_authentication=row.get("Authorized Users/Authentication"),
        )
        services.append(service)

    return services


def process_person_info(list_of_dicts: List[Dict[str, str]]) -> Person:
    """
    Processes the person information table.
    :param List[Dict[str, str]] list_of_dicts: The table to process.
    :return: A Person object representing the person information.
    :rtype: Person
    """
    person_data = merge_dicts(list_of_dicts, True)
    person = Person(
        name=person_data.get("Name"),
        phone=person_data.get("Phone Number"),
        email=person_data.get("Email Address"),
        title=person_data.get("Title"),
    )
    return person


def process_ports_and_protocols(list_of_dicts: List[Dict[str, str]]) -> List[PortsAndProtocolData]:
    """
    Processes the ports and protocols table.
    :param List[Dict[str, str]] list_of_dicts: The table to process.
    :return: A list of PortsAndProtocolData objects representing the ports and protocols information.
    :rtype: List[PortsAndProtocolData]
    """
    ports_an_protocols = []
    for row in list_of_dicts:
        try:
            port_col = "Port #"
            ports_an_protocols.append(
                PortsAndProtocolData(
                    service=row.get("Service Name"),
                    port=int(row.get(port_col)) if "-" not in row.get(port_col) else 0,
                    start_port=(
                        int(row.get(port_col).split("-")[0]) if "-" in row.get(port_col) else row.get(port_col, 0)
                    ),
                    end_port=int(row.get(port_col).split("-")[1]) if "-" in row.get(port_col) else row.get(port_col, 0),
                    protocol=row.get("Transport Protocol"),
                    ref_number=row.get("Reference #"),
                    purpose=row.get("Purpose"),
                    used_by=row.get("Used By"),
                )
            )
        except ValueError:
            logger.warning(f"Skipping bad data unable to processing row: {row}")

    return ports_an_protocols


def merge_dicts(list_of_dicts: List[Dict], prioritize_first: bool = False) -> dict:
    """
    Merges a list of dictionaries into a single dictionary.
    :param List[Dict] list_of_dicts: The list of dictionaries to merge.
    :param bool prioritize_first: Whether to prioritize the first dictionary in the list.
    :return: A single dictionary containing the merged data.
    :rtype: dict
    """

    merged_dict = {}
    for d in list_of_dicts:
        if prioritize_first:
            merged_dict.update(d, **merged_dict)  # Merge with priority to earlier values
        else:
            merged_dict.update(d)  # Simple merge

    return merged_dict


def identify_and_process_tables(tables: List[Dict[str, Any]]):
    """
    Identifies and processes tables based on their content keywords and processes them accordingly.
    :param List[Dict[str, Any]] tables: The tables to process.
    :return: A dictionary containing the processed data.
    :rtype: Dict[str, Any]
    """
    processed_data = {
        "ssp_doc": None,
        "org": None,
        "prepared_by": None,
        "stakeholders": [],
        "services": [],
        "ports_and_protocols": [],
    }
    # logger.info(tables)
    for item in tables:
        process_table_based_on_keys(item, processed_data)
        logger.debug(item.get("preceding_text"))
        logger.debug(item.get("table_data"))

    owner, isso = identify_owner_or_isso(processed_data.get("stakeholders", []))
    logger.debug(f"Owner: {owner}")
    if owner:
        processed_data["owner"] = owner
    if isso:
        processed_data["isso"] = isso

    return processed_data


def identify_owner_or_isso(people: List[Person]) -> Tuple[Person, Person]:
    """
    Identifies the ISSO and the Owner from a list of people.

    :param List[Person] people: A list of Person objects representing the stakeholders.
    :returns: A tuple containing the ISSO and the Owner.
    :rtype: Tuple[Person, Person]
    """
    logger.info(f"Found People: {len(people)}")
    existing_users = []
    try:
        existing_users = User.get_list()
    except Exception as e:
        logger.warning(f"Error getting Users: {e}")
    logger.debug(f"Found Users: {existing_users}")
    owner, isso = find_owner_and_isso(people)

    logger.debug(f"Found owner: {owner}")
    logger.debug(f"Found isso: {isso}")
    if owner or isso:
        logger.debug(f"Found existing Users: {len(existing_users)}")
    existing_users_dict = {u.email: u for u in existing_users if hasattr(u, "email")}
    if existing_users_dict and owner and isso:
        try:
            owner = existing_users_dict.get(owner.email)
            isso = existing_users_dict.get(isso.email)
        except Exception as e:
            logger.warning(f"Error getting Users: {e}")
    return owner, isso


def find_owner_and_isso(
    people: List[Person],
) -> Tuple[Optional[Person], Optional[Person]]:
    """
    Identifies the ISSO and the Owner from a list of people.

    :param List[Person] people: A list of Person objects representing the stakeholders.
    :returns: A tuple containing the ISSO and the Owner.
    :rtype: Tuple[Optional[Person], Optional[Person]]
    """
    owner = None
    isso = None
    try:
        for person in people:
            percent_match_owner = "System Owner".lower() in person.title.lower()
            percent_match_isso = "Information System Security Officer".lower() in person.title.lower()

            logger.debug(f"Owner match: {percent_match_owner}")
            logger.debug(f"Isso match: {percent_match_isso}")
            if percent_match_owner:
                owner = person
            if percent_match_isso:
                isso = person
    except Exception as e:
        logger.warning(f"Error finding Owner and ISSO: {e}")
    return owner, isso


def process_table_based_on_keys(table: any, processed_data: Dict[str, Any]):
    """
    Processes a table based on the keys present in the first row of the table.
    :param any table: The table to process.
    :param Dict[str, Any] processed_data: The dictionary where processed data is stored.
    """
    try:
        key = table.get("preceding_text")
        merged_dict = merge_dicts(table.get("table_data"), True)
        table_data = table.get("table_data")
        fetch_ports(key, processed_data, table_data, merged_dict)
        fetch_stakeholders(merged_dict, table_data, processed_data, key)
        fetch_services(merged_dict, table_data, processed_data)
        fetch_ssp_info(merged_dict, table_data, processed_data, key)
        fetch_prep_data(table_data, processed_data, key)
    except Exception as e:
        logger.warning(f"Error Processing Table - {table.get('preceding_text', '') if table else ''}: {e}")


def fetch_prep_data(
    table_data: List[Dict[str, str]],
    processed_data: Dict[str, Any],
    key: str,
):
    """
    Fetches Prepared By and Prepared For information from the table.
    :param str key: The key to check for.
    :param Dict[str, Any] processed_data: The dictionary where processed data is stored.
    :param List[Dict[str, str]] table_data: The table data to process.

    """
    if "Prepared by" in key:
        logger.info("Processing Prepared By")
        processed_data["prepared_by"] = process_prepared_by(table_data)
    if "Prepared for" in key:
        logger.info("Processing Prepared By")
        processed_data["prepared_for"] = process_prepared_by(table_data)


def fetch_ssp_info(
    merged_dict: Dict[str, str],
    table_data: List[Dict[str, str]],
    processed_data: Dict[str, Any],
    key: str,
):
    """
    Fetches SSP information from the table.
    :param str key: The key to check for.
    :param Dict[str, Any] processed_data: The dictionary where processed data is stored.
    :param List[Dict[str, str]] table_data: The table data to process.
    :param Dict[str, str] merged_dict: The merged dictionary of the table data.

    """
    if "CSP Name:" in merged_dict:
        logger.info("Processing SSP Doc")
        processed_data["ssp_doc"] = process_ssp_info(table_data)
    if "Document Revision History" in key:
        logger.info("Processing Version")
        processed_data["version"] = get_max_version(entries=table_data)
        if processed_data["ssp_doc"]:
            processed_data["ssp_doc"].version = processed_data.get("version")
        logger.info(f"Version: {processed_data['version']}")


def fetch_services(
    merged_dict: Dict[str, str],
    table_data: List[Dict[str, str]],
    processed_data: Dict[str, Any],
):
    """
    Fetches services data from the table.
    :param Dict[str, Any] processed_data: The dictionary where processed data is stored.
    :param List[Dict[str, str]] table_data: The table data to process.
    :param Dict[str, str] merged_dict: The merged dictionary of the table data.

    """
    if "CSP/CSO Name (Name on FedRAMP Marketplace)" in merged_dict:
        logger.info("Processing Leveraged Services")
        processed_data["services"] = build_leveraged_services(table_data)


def fetch_stakeholders(
    merged_dict: Dict[str, str],
    table_data: List[Dict[str, str]],
    processed_data: Dict[str, Any],
    key: str,
):
    """
    Fetches stakeholders data from the table.
    :param str key: The key to check for.
    :param Dict[str, Any] processed_data: The dictionary where processed data is stored.
    :param List[Dict[str, str]] table_data: The table data to process.
    :param Dict[str, str] merged_dict: The merged dictionary of the table data.

    """
    if "Name" in merged_dict and "Company / Organization" in table_data[0]:
        logger.info("Processing Organization and Stakeholders")
        process_organization_and_stakeholders(table_data, processed_data)
    if ("ISSO (or Equivalent) Point of Contact" in key) or ("Table 4.1" in key):
        logger.info("Processing Stakeholders")
        person = process_person_info(table_data)
        processed_data["stakeholders"].append(person)


def fetch_ports(
    key: str,
    processed_data: Dict[str, Any],
    table_data: List[Dict[str, str]],
    merged_dict: Dict[str, str],
):
    """
    Fetches ports and protocols data from the table.
    :param str key: The key to check for.
    :param Dict[str, Any] processed_data: The dictionary where processed data is stored.
    :param List[Dict[str, str]] table_data: The table data to process.
    :param Dict[str, str] merged_dict: The merged dictionary of the table data.

    """
    if "Services, Ports, and Protocols" in key and "Port #" in merged_dict:
        logger.info("Processing Ports and Protocols")
        processed_data["ports_and_protocols"] = process_ports_and_protocols(table_data)


def process_prepared_by(table: List[Dict[str, str]]) -> PreparedBy:
    """
    Processes the prepared by information from the table.
    :param List[Dict[str, str]] table: The table to process.
    :return: A PreparedBy object representing the prepared by information.
    :rtype: PreparedBy
    """
    prepared_by = merge_dicts(table, True)
    return PreparedBy(
        name=prepared_by.get("Organization Name"),
        street=prepared_by.get("Street Address"),
        building=prepared_by.get("Suite/Room/Building"),
        city_state_zip=prepared_by.get("City, State, Zip"),
    )


def process_version(table: List[Dict[str, str]]) -> str:
    """
    Processes the version information from the table.
    :param List[Dict[str, str]] table: The table to process.
    :return: The version number.
    :rtype: str
    """
    # Assuming the version is stored under a key named "Version" in one of the table rows
    return get_max_version(table)


def process_organization_and_stakeholders(table: List[Dict[str, str]], processed_data: Dict[str, Any]):
    """
    Processes organization and stakeholders information from the table.
    :param List[Dict[str, str]] table: The table to process.
    :param Dict[str, Any] processed_data: The dictionary where processed data is stored.
    """
    processed_data["org"] = process_company_info(table)
    person = process_person_info(table)
    processed_data["stakeholders"].append(person)


def process_fedramp_docx_v5(
    file_name: str,
    base_fedramp_profile_id: int,
    save_data: bool,
    add_missing: bool,
    appendix_a_file_name: str,
):
    """
    Processes a FedRAMP document and loads it into RegScale.
    :param str file_name: The path to the FedRAMP document.
    :param int base_fedramp_profile_id: The name of the RegScale FedRAMP profile to use.
    :param bool save_data: Whether to save the data as a JSON file.
    :param bool add_missing: Whether to create missing controls from profile in the SSP.
    :param str appendix_a_file_name: The path to the Appendix A document.

    """
    logger.info(f"Processing FedRAMP Document: {file_name}")
    logger.info(f"Appendix A File: {appendix_a_file_name}")
    ssp_parser = SSPDocParser(file_name)
    profile = Profile.get_object(object_id=base_fedramp_profile_id)
    logger.info(f"Profile: {profile.name}" if profile else "No Profile Found")
    profile_mappings = ProfileMapping.get_by_profile(profile_id=profile.id)

    logger.info(f"Found {len(profile_mappings)} controls in profile")
    logger.info(f"Using the following values: save_data: {save_data} and add_missing: {add_missing}")

    tables = ssp_parser.parse()
    doc_text_dict = ssp_parser.text
    app = Application()
    config = app.config
    user_id = config.get("userId")

    processed_data = identify_and_process_tables(tables)
    parent_id = processing_data_from_ssp_doc(processed_data, user_id, doc_text_dict)
    if appendix_a_file_name:
        logger.info(f"Processing Appendix A File: {appendix_a_file_name}")

        parser = AppendixAParser(filename=appendix_a_file_name)
        controls_implementation_dict = parser.fetch_controls_implementations()

        process_appendix_a(
            parent_id=parent_id,
            mappings=profile_mappings,
            add_missing=add_missing,
            controls_implementation_dict=controls_implementation_dict,
        )
    extract_and_upload_images(file_name, parent_id)


def log_dictionary_items(dict_items: Dict[str, str]):
    """
    Logs the items in a dictionary.
    :param Dict[str, str] dict_items: The dictionary to log.
    """
    for key, value in dict_items.items():
        if value:
            logger.info(f"{key}: {value}")


def handle_implemented(row_data: Dict, status: str) -> str:
    """
    Handles the implemented status of a control.
    :param Dict row_data: The data from the row.
    :param str status: The current status of the control.
    :return: The updated status of the control.
    :rtype: str
    """
    log_dictionary_items(row_data)
    for key, value in row_data.items():
        if key == "Implemented" and value:
            status = ControlImplementationStatus.FullyImplemented.value
    return status


def handle_service_provider_corporate(row_data: Dict, responsibility: str) -> str:
    """
    Handles the service provider corporate responsibility of a control.
    :param Dict row_data:
    :param str responsibility:
    :return: fetched responsibility
    :rtype: str
    """
    log_dictionary_items(row_data)
    for key, value in row_data.items():
        if value:
            responsibility = key
    return responsibility


def handle_parameter(row_data: Dict, parameters: Dict, control_id: int):
    """
    Handles the parameters of a control.
    :param Dict row_data: The data from the row.
    :param Dict parameters: The parameters dictionary.
    :param int control_id: The control ID.
    """
    log_dictionary_items(row_data)
    for key, value in row_data.items():
        if value:
            if parameters.get(control_id):
                parameters[control_id].append(value)
            else:
                parameters[control_id] = [value]


def handle_row_data(
    row: Dict,
    control: ControlImplementation,
    status: str,
    responsibility: str,
    parameters: Dict,
    key: str,
    alternative_key: str,
) -> Tuple[str, str, Dict]:
    """
    Handles the data from a row.
    :param Dict row: The row to process.
    :param ControlImplementation control:
    :param str status:
    :param str responsibility:
    :param Dict parameters:
    :param str key:
    :param str alternative_key:
    :return: A tuple containing the updated status, responsibility, and parameters.
    :rtype: Tuple[str, str, Dict]
    """
    row_data = row.get(key, row.get(alternative_key))
    logger.info(f"Row Data: {row_data}")

    if "Implemented" in row_data:
        status = handle_implemented(row_data, status)
    elif "Service Provider Corporate" in row_data:
        responsibility = handle_service_provider_corporate(row_data, responsibility)
    elif "Parameter" in row_data:
        handle_parameter(row_data, parameters, control.id)

    return status, responsibility, parameters


def process_fetch_key_value(summary_data: Dict) -> Optional[str]:
    """
    Extracts key information from the summary data.
    :param Dict summary_data: The summary data from the row.
    :return: str: The key from the summary data.
    :rtype: Optional[str]
    """
    for key, value in summary_data.items():
        if value:
            logger.info(f"{key}: {value}")
            return key
    return None


def process_parameter(summary_data: Dict, control_id: int, current_parameters: List[Dict]):
    """
    Processes the parameters from the summary data.
    :param Dict summary_data: The summary data from the row.
    :param int control_id: The control ID.
    :param List[Dict] current_parameters: The current parameters.
    """
    for key, value in summary_data.items():
        if value:
            parameter_name = key.replace("Parameter ", "").strip()
            param = {
                "control_id": control_id,
                "parameter_name": parameter_name if parameter_name else None,
                "parameter_value": value,
            }
            if param not in current_parameters:
                current_parameters.append(param)


def process_row_data(row: Dict, control: SecurityControl, control_dict: Dict) -> Tuple[str, str, List[Dict]]:
    """
    Processes a single row of data, updating status, responsibility, and parameters based on control summary information.
    :param Dict row: The row to process.
    :param SecurityControl control: The control to process.
    :param Dict control_dict: The dictionary containing the control data.
    :return: A tuple containing the updated status, responsibility, and parameters.
    :rtype: Tuple[str, str, List[Dict]]
    """
    control_id_key = f"{control.controlId} Control Summary Information"
    alternate = format_alternative_control_key(control.controlId) or control.controlId
    alternative_control_id_key = f"{alternate} Control Summary Information"

    summary_data = row.get(control_id_key, row.get(alternative_control_id_key))
    if summary_data:
        logger.info(f"Row Data: {summary_data}")

        if "Implemented" in summary_data:
            status = process_fetch_key_value(summary_data)
            control_dict["status"] = "Fully Implemented" if status == "Implemented" else status

        if "Service Provider Corporate" in summary_data:
            control_dict["responsibility"] = process_fetch_key_value(summary_data)

        if "Parameter" in summary_data:
            process_parameter(summary_data, control.id, control_dict.get("parameters", []))

    return (
        control_dict.get("status"),
        control_dict.get("responsibility"),
        control_dict.get("parameters"),
    )


def process_fetch_key_if_value(summary_data: Dict) -> str:
    """
    Extracts key information from the summary data.
    :param Dict summary_data: The summary data from the row.
    :return: str: The key from the summary data.
    :rtype: str
    """
    for key, value in summary_data.items():
        if value is True or value == "☒":
            logger.info(f"{key}: {value}")
            return key


def _find_statement(control: any, alternative_control_id: str, row: Dict, control_dict: Dict) -> str:
    """
    Find the statement for the control.
    :param any control:
    :param str alternative_control_id:
    :param Dict row:
    :param Dict control_dict:
    :return: str: The statement for the control.
    :rtype: str
    """
    key_statment = f"{control.controlId} What is the solution and how is it implemented?"
    key_alt_statment = f"{alternative_control_id} What is the solution and how is it implemented?"
    statement_dict = row.get(key_statment) or row.get(key_alt_statment)

    if isinstance(statement_dict, dict):
        control_dict["statement"] = " ".join(f"{key} {value}" for key, value in statement_dict.items() if value)
    elif isinstance(statement_dict, str):
        control_dict["statement"] = statement_dict
    return ""


def process_appendix_a(
    parent_id: int,
    mappings: List[ProfileMapping],
    add_missing: bool = False,
    controls_implementation_dict: Dict = None,
):
    """
    Processes the Appendix A data.
    :param int parent_id: The parent ID.
    :param List[ProfileMapping] mappings: The mappings to process.
    :param bool add_missing: Whether to add missing controls.
    :param Dict controls_implementation_dict: The controls implementation dictionary.
    """
    data_dict = controls_implementation_dict
    existing_controls = ControlImplementation.get_all_by_parent(parent_id=parent_id, parent_module="securityplans")
    logger.info(f"Found {len(existing_controls)} existing controls")
    logger.info(f"{existing_controls}")
    existing_control_dict = {c.controlID: c for c in existing_controls if c and c.controlID}

    for mapping in mappings:
        control = SecurityControl.get_object(object_id=mapping.controlID)

        if not control:
            logger.debug(f"Control not found in mappings: {mapping.controlID}")
            continue
        alternate = control.controlId
        try:
            alternate = format_alternative_control_key(control.controlId)
        except ValueError:
            logger.debug(f"Error formatting alternative control key: {control.controlId}")
        alternative_control_id = alternate
        control_dict = data_dict.get(control.controlId)
        if not control_dict:
            control_dict = data_dict.get(alternative_control_id)
        if not control_dict:
            logger.debug(f"Control not found in parsed controls: {control.controlId}")
            continue

        process_control_implementations(
            existing_control_dict,
            control,
            control_dict,
            parent_id,
            add_missing,
        )


def process_control_implementations(
    existing_control_dict: Dict,
    control: SecurityControl,
    control_dict: Dict,
    parent_id: int,
    add_missing: bool = False,
):
    """
    Processes the control implementations.
    :param Dict existing_control_dict: The existing control dictionary.
    :param SecurityControl control: The control implementation object.
    :param Dict control_dict: The control dictionary.
    :param int parent_id: The parent ID.
    :param bool add_missing: Whether to add missing controls.
    """
    if existing_control := existing_control_dict.get(control.id):
        update_existing_control(
            existing_control,
            control_dict.get("status"),
            control_dict.get("statement"),
            control_dict.get("responsibility"),
        )
        if params := control_dict.get("parameters"):
            handle_params(
                params,
                control=control,
                control_implementation=existing_control,
            )
        if parts := control_dict.get("parts"):
            handle_parts(
                parts=parts,
                status=map_implementation_status(control_dict.get("status")),
                control=control,
                control_implementation=existing_control,
            )
    else:
        implementation = create_implementations(
            control,
            parent_id,
            control_dict.get("status"),
            control_dict.get("statement"),
            control_dict.get("responsibility"),
            control_dict.get("parameters"),
            add_missing,
        )
        if implementation:
            if parts := control_dict.get("parts"):
                handle_parts(
                    parts=parts,
                    status=map_implementation_status(control_dict.get("status")),
                    control=control,
                    control_implementation=implementation,
                )
            if params := control_dict.get("parameters"):
                handle_params(
                    parameters=params,
                    control=control,
                    control_implementation=implementation,
                )


def create_implementations(
    control: SecurityControl,
    parent_id: int,
    status: str,
    statement: str,
    responsibility: str,
    parameters: List[Dict],
    add_missing: bool = False,
) -> ControlImplementation:
    """
    Creates the control implementations.
    :param SecurityControl control: The control object.
    :param int parent_id: The parent ID.
    :param str status: The status of the implementation.
    :param str statement: The statement of the implementation.
    :param str responsibility: The responsibility of the implementation.
    :param List[Dict] parameters: The parameters of the implementation.
    :param bool add_missing: Whether to add missing controls.
    :return: The created control implementation.
    :rtype: ControlImplementation
    """
    if status and status.lower() == "implemented":
        status = "Fully Implemented"
    if control and (status == DEFAULT_STATUS and add_missing) or (status != DEFAULT_STATUS):
        logger.info(f"Creating Control: {control.controlId} - {control.id} - {status} - {statement} - {responsibility}")
        logger.info(f"params: {parameters}")
        control_implementation = ControlImplementation(
            parentId=parent_id,
            parentModule="securityplans",
            controlID=control.id,
            status=map_implementation_status(status),
            implementation=" ".join(statement) if isinstance(statement, list) else "",
        ).create()
        return control_implementation
        # handle_params(parameters, control, control_implementation)


def find_matching_parts(part: str, other_ids: List[str]) -> List[str]:
    """
    Find and return the otherId values that contain the specified part (e.g., "Part a"),
    by directly checking for the presence of a substring like '_obj.a'.
    :param str part: The part to look for.
    :param List[str] other_ids: The list of otherId values to search.
    :return: A list of otherId values that contain the specified part.
    :rtype: List[str]
    """
    # Extract the letter part (e.g., "a") from the input string.
    part_letter = part[-1].lower()  # Assuming the format "Part X" where X is the part letter.

    # Construct the substring to look for in otherId values.
    part_pattern = f"_obj.{part_letter}"

    # Collect and return all matching otherId values.
    matches = [other_id for other_id in other_ids if part_pattern in other_id.lower()]

    return matches


def handle_parts(
    parts: Dict,
    status: str,
    control: SecurityControl,
    control_implementation: ControlImplementation,
):
    """
    Handle the parts for the given control and control implementation.
    :param Dict parts: The parts to handle.
    :param str status: The status of the implementation.
    :param SecurityControl control: The security control object.
    :param ControlImplementation control_implementation: The control implementation object.
    """
    control_objectives = ControlObjective.get_by_control(control_id=control.id)

    existing_objectives = ImplementationObjective.get_by_control(implementation_id=control_implementation.id)
    existing_options = ImplementationOption.get_by_control(
        security_control_id=control.id, security_plan_id=control_implementation.parentId
    )
    option_dict = {f"{o.name}-{o.securityControlId}": o for o in existing_options}
    for existing_objective in existing_objectives:
        existing_objective.delete()
    for existing_option in existing_options:
        existing_option.delete()
    for index, part in enumerate(parts):
        logger.info(f"Part: {part}")
        if part.get("value") == "":
            continue
        logger.info(f"Control: {control.controlId} Part: {part.get('name')} - {part.get('value')}")
        part_name = part.get("name", "Default Name")
        matching_objectives = get_matching_objectives(control_objectives, part_name)
        option_key = f"{part_name}-{control.id}"
        matching_option = option_dict.get(option_key)
        if matching_option:
            try:
                option = matching_option
                option.name = part_name
                option.description = part.get("value", "")
                option.acceptability = status
                option.save()
                handle_control_objectives(
                    matching_objectives,
                    control,
                    control_implementation,
                    option,
                    status,
                    part_name,
                    index,
                    control_objectives,
                )
            except Exception as e:
                logger.warning(f"Error handling parts: {e}")
        else:
            try:
                option = ImplementationOption(
                    name=part_name,
                    description=part.get("value", ""),
                    acceptability=status,
                    securityControlId=control.id,
                ).create()

                handle_control_objectives(
                    matching_objectives,
                    control,
                    control_implementation,
                    option,
                    status,
                    part_name,
                    index,
                    control_objectives,
                )
            except Exception as e:
                logger.warning(f"Error handling parts: {e}")


def handle_control_objectives(
    matching_objectives: List[ControlObjective],
    control: SecurityControl,
    control_implementation: ControlImplementation,
    option: ImplementationOption,
    status: str,
    part_name: str,
    index: int,
    control_objectives: List[ControlObjective],
):
    """
    Handle the control objectives for the given control and control implementation.
    :param List[ControlObjective] matching_objectives: The list of matching control objectives.
    :param SecurityControl control: The security control object.
    :param ControlImplementation control_implementation: The control implementation object.
    :param ImplementationOption option: The implementation option object.
    :param str status: The status of the implementation.
    :param str part_name: The name of the part.
    :param int index: The index of the part.
    :param List[ControlObjective] control_objectives: The list of control objectives.

    """
    if not matching_objectives and len(control_objectives) > 1:
        for cindex, control_objective in enumerate(control_objectives):
            if cindex == index:
                ImplementationObjective(
                    securityControlId=control.id,
                    implementationId=control_implementation.id,
                    optionId=option.id,
                    status=status,
                    statement=option.description,
                    objectiveId=control_objective.id,
                ).create()
    if part_name == "Default Part" and len(control_objectives) == 1:
        ImplementationObjective(
            securityControlId=control.id,
            implementationId=control_implementation.id,
            optionId=option.id,
            status=status,
            statement=option.description,
            objectiveId=control_objectives[0].id,
        ).create()
    for matching_objective in matching_objectives:
        ImplementationObjective(
            securityControlId=control.id,
            implementationId=control_implementation.id,
            optionId=option.id,
            status=status,
            statement=option.description,
            objectiveId=matching_objective.id,
        ).create()


def get_matching_objectives(control_objectives: List[ControlObjective], part_name: str) -> List[ControlObjective]:
    """
    Find and return the control objectives that match the specified part name.
    :param List[ControlObjective] control_objectives: The list of control objectives to search.
    :param str part_name: The part name to match.
    :return: A list of control objectives that match the specified part name.
    :rtype: List[ControlObjective]
    """
    matching_objectives = []
    try:
        matching_objective_other_ids = find_matching_parts(part_name, [o.otherId for o in control_objectives])

        matching_objectives = [o for o in control_objectives if o.otherId in matching_objective_other_ids]
    except Exception as e:
        logger.warning(f"Error finding matching objectives: {e}")
    return matching_objectives


def handle_params(
    parameters: List[Dict],
    control: SecurityControl,
    control_implementation: ControlImplementation,
):
    """
    Handle the parameters for the given control and control implementation.
    :param List[Dict] parameters: The parameters to handle.
    :param SecurityControl control: The security control object.
    :param ControlImplementation control_implementation: The control implementation object.

    """
    # Log the initial handling of parameters for the given control.
    logger.info(f"Handling Parameters for Control: {control.id} - {len(parameters)}")
    base_control_params = ControlParameter.get_by_control(control_id=control.id)
    parameters = build_params(base_control_params, parameters)
    existing_params = Parameter.get_all_by_parent(parent_id=control_implementation.id, parent_module="")
    logger.info(
        f"Existing Params count: {len(existing_params)} for control implementation with id: {control_implementation.id}"
    )
    if parameters and not existing_params:
        for param in parameters:
            logger.debug(f"Param: {param}")
            create_parameter_for_control(param, control_implementation)
    else:
        for existing_param in existing_params:
            existing_param.delete()

        for param in parameters:
            logger.debug(f"Param: {param}")
            create_parameter_for_control(param, control_implementation)


def build_params(base_control_params: List[ControlParameter], parameters: List[Dict]) -> List[Dict]:
    """
    Builds the parameters for the control implementation.
    :param List[ControlParameter] base_control_params: The base control parameters.
    :param List[Dict] parameters: The parameters to build.
    :return: List[Dict]: The built parameters.
    :rtype: List[Dict]
    """
    new_params = []
    if len(base_control_params) >= len(parameters):
        for index, base_param in enumerate(base_control_params):
            if len(parameters) >= index + 1:
                new_param_dict = {}
                new_param_dict["name"] = base_param.parameterId
                new_param_dict["value"] = parameters[index].get("value") if parameters[index] else base_param.default
                new_params.append(new_param_dict)
    return new_params


def create_parameter_for_control(param: Dict, control_implementation: ControlImplementation):
    """
    Creates a parameter for the control implementation.
    :param Dict param: The parameter to create.
    :param ControlImplementation control_implementation: The control implementation object.

    """
    new_param = Parameter(
        controlImplementationId=control_implementation.id,
        name=param.get("name"),
        value=param.get("value"),
    )
    logger.debug(f"Creating Param: {new_param}")
    new_param.create()


def process_each_parameter(
    params_for_control: List,
    control_implementation: ControlImplementation,
    control_param: ControlParameter,
    existing_param: Optional[Parameter],
):
    """
    Processes each parameter for the control implementation.
    :param List params_for_control: The parameters for the control.
    :param ControlImplementation control_implementation: The control implementation object.
    :param ControlParameter control_param: The control parameter object.
    :param Optional[Parameter] existing_param: The existing parameter object.

    """
    for param in params_for_control:
        if existing_param:
            # Update the existing parameter.
            logger.info(f"Updating Param: {existing_param.id} - {param}")
            existing_param.value = param
            existing_param.dataType = ParameterDataTypes.STRING.value
            existing_param.save()
            break  # Exit after updating the single parameter.
        else:
            # Create a new parameter if none exists.
            logger.info("Creating new param")
            new_param = Parameter(
                controlImplementationId=control_implementation.id,
                name=control_param.parameterId if control_param else "No Param Name",
                value=param,
                dataType=ParameterDataTypes.STRING.value,
            )
            new_param.create()
            break  # Exit after creating the single parameter.


def map_implementation_status(status: str) -> str:
    """
    Maps the implementation status to the appropriate value.
    :param str status: The status to map.
    :return: The mapped status.
    :rtype: str
    """
    if status and status.lower() == "implemented":
        return ControlImplementationStatus.FullyImplemented.value
    elif status and status.lower() == "fully implemented":
        return ControlImplementationStatus.FullyImplemented.value
    elif status and status.lower() == "partially implemented":
        return ControlImplementationStatus.PartiallyImplemented.value
    elif status and status.lower() == "planned":
        return ControlImplementationStatus.Planned.value
    elif status and status.lower() == "not applicable":
        return ControlImplementationStatus.NA.value
    elif status and status.lower() == "alternative implementation":
        return ControlImplementationStatus.FullyImplemented.value
    else:
        return ControlImplementationStatus.NA.value


def update_existing_control(control: ControlImplementation, status: str, statement: str, responsibility: str):
    """
    Updates an existing control with new information.
    :param ControlImplementation control: The control implementation object.
    :param str status: The status of the implementation.
    :param str statement: The statement of the implementation.
    :param str responsibility: The responsibility of the implementation.

    """
    state_text = " ".join(statement) if isinstance(statement, list) else ""
    justify = (
        state_text or "Unknown" if map_implementation_status(status) == ControlImplementationStatus.NA.value else None
    )
    control.status = map_implementation_status(status)
    control.exclusionJustification = justify
    control.implementation = state_text
    control.responsibility = responsibility
    control.save()


def format_alternative_control_key(control_id: str) -> str:
    """
    Formats the key for the alternative control information.
    :param str control_id: The control ID to format.
    :return: The formatted control ID.
    :rtype: str
    """
    # Unpack the control_family and the rest (assumes there's at least one '-')
    control_family, *rest = control_id.split("-")
    rest_joined = "-".join(rest)  # Join the rest back in case there are multiple '-'

    # Check for '(' and split if needed, also handling the case without '(' more cleanly
    if "(" in rest_joined:
        control_num, control_ending = rest_joined.split("(", 1)  # Split once
        control_ending = control_ending.rstrip(")")  # Remove trailing ')' if present
        alternative_control_id = f"{control_family}-{format_int(int(control_num))}({control_ending})"
    else:
        control_num = rest_joined
        alternative_control_id = f"{control_family}-{format_int(int(control_num))}"

    return alternative_control_id


def format_int(n: int) -> str:
    """
    Formats an integer to a string with a leading zero if it's a single digit.
    :param int n: The integer to format.
    :return: The formatted integer as a string.
    :rtype: str
    """
    # Check if the integer is between 0 and 9 (inclusive)
    if 0 <= n <= 9:
        # Prepend a "0" if it's a single digit
        return f"0{n}"
    else:
        # Just convert to string if it's not a single digit
        return str(n)


def build_data_dict(tables: List) -> Dict:
    """
    Builds a dictionary from a list of tables.

    :param List tables: A list of tables.
    :return: A dictionary containing the tables.
    :rtype: Dict
    """
    table_dict = {}
    for table in tables:
        k_parts = list(table.keys())[0].split()
        if k_parts:
            key_control = k_parts[0]
            if key_control in table_dict:
                table_dict[key_control].append(table)
            else:
                table_dict[key_control] = [table]
    return table_dict


def processing_data_from_ssp_doc(processed_data, user_id, doc_text_dict: Dict) -> int:
    """
    Finalizes the processing of data by creating necessary records in the system.
    :param Dict[str, Any] processed_data: The processed data.
    :param str user_id: The ID of the user performing the operation.
    :param Dict[str, str] doc_text_dict: The dictionary containing the text from the document.
    :return: The ID of the parent object.
    :rtype: int
    """
    processed_data["doc_text_dict"] = doc_text_dict
    # Process SSP Document if present
    if not processed_data.get("ssp_doc"):
        logger.warning("No SSP Document found")
        sys.exit(1)
    ssp = process_ssp_doc(
        processed_data.get("ssp_doc"),
        processed_data,
        user_id,
    )
    parent_id = ssp.id
    logger.info(f"Parent ID: {parent_id}")
    parent_module = "securityplans"
    approval_date = ssp.approvalDate

    # Create stakeholders
    if processed_data.get("stakeholders"):
        create_stakeholders(processed_data.get("stakeholders"), parent_id, parent_module)
    # Process services if present
    if processed_data.get("services"):
        create_leveraged_authorizations(
            processed_data["services"], user_id, parent_id, approval_date
        )  # Assuming parent_id is the ssp_id for simplicity

    # Process ports and protocols if present
    if processed_data.get("ports_and_protocols"):
        create_ports_and_protocols(
            processed_data["ports_and_protocols"], parent_id
        )  # Assuming parent_id is the ssp_id for simplicity
    return parent_id


def create_stakeholders(stakeholders: List[Person], parent_id: int, parent_module: str) -> None:
    """
    Creates stakeholders in RegScale.
    :param List[Person] stakeholders: A list of Person objects representing the stakeholders.
    :param int parent_id: The ID of the parent object.
    :param str parent_module: The parent module.

    """
    logger.info(f"Creating Stakeholders: {parent_id} - {parent_module}")
    existing_stakeholders: List[StakeHolder] = StakeHolder.get_all_by_parent(
        parent_id=parent_id, parent_module=parent_module
    )
    for person in stakeholders:
        existing_stakeholder = next(
            (s for s in existing_stakeholders if s.name == person.name and s.email == person.email),
            None,
        )
        if existing_stakeholder:
            logger.debug(existing_stakeholder.model_dump())
            existing_stakeholder.name = person.name
            existing_stakeholder.email = person.email
            existing_stakeholder.phone = person.phone
            existing_stakeholder.title = person.title
            existing_stakeholder.save()
        else:
            StakeHolder(
                name=person.name,
                email=person.email,
                phone=person.phone,
                title=person.title,
                parentId=parent_id,
                parentModule=parent_module,
            ).create()


def process_cloud_info(ssp_doc: SSPDoc) -> Dict:
    """
    Processes the cloud information from the SSP document.
    :param SSPDoc ssp_doc: The SSP document object.
    :return: A dictionary containing the cloud deployment model information.
    :rtype: Dict
    """
    return {
        "saas": "SaaS" in ssp_doc.service_model,
        "paas": "PaaS" in ssp_doc.service_model,
        "iaas": "IaaS" in ssp_doc.service_model,
        "other_service_model": not any(service in ssp_doc.service_model for service in ["SaaS", "PaaS", "IaaS"]),
        "deploy_gov": "gov" in ssp_doc.deployment_model.lower() or "government" in ssp_doc.deployment_model.lower(),
        "deploy_hybrid": "hybrid" in ssp_doc.deployment_model.lower(),
        "deploy_private": "private" in ssp_doc.deployment_model.lower(),
        "deploy_public": "public" in ssp_doc.deployment_model.lower(),
        "deploy_other": not any(
            deploy in ssp_doc.deployment_model.lower()
            for deploy in ["gov", "government", "hybrid", "private", "public"]
        ),
    }


def process_ssp_doc(
    ssp_doc: SSPDoc,
    data: Dict,
    user_id: str,
) -> SecurityPlan:
    """
    Processes the SSP document.
    :param SSPDoc ssp_doc: The SSP document object.
    :param Dict[str, Any] data: The processed data.
    :param str user_id: The ID of the user performing the operation.
    :return: The security plan object.
    :rtype: SecurityPlan
    """
    if ssp_doc:
        cloud_info = process_cloud_info(ssp_doc)
        plans = SecurityPlan.get_list()
        plan_count = len(plans)
        logger.info(f"Found SSP Count of: {plan_count}")
        ssp = None
        for plan in plans:
            if plan.systemName == ssp_doc.name:
                ssp = SecurityPlan.get_object(object_id=plan.id)
                logger.info(f"Found SSP: {plan.systemName}")
                break
        if not ssp:
            ssp = create_ssp(ssp_doc, cloud_info, user_id, data)
        else:
            ssp = save_security_plan_info(ssp, cloud_info, ssp_doc, user_id, data)
        return ssp


def get_expiration_date(dt_format: Optional[str] = "%Y-%m-%d %H:%M:%S") -> str:
    """
    Return the expiration date, which is 3 years from today

    :param Optional[str] dt_format: desired format for datetime string, defaults to "%Y-%m-%d %H:%M:%S"
    :return: Expiration date as a string, 3 years from today
    :rtype: str
    """
    expiration_date = datetime.datetime.now() + relativedelta(years=3)
    return expiration_date.strftime(dt_format)


def create_ssp(ssp_doc: SSPDoc, cloud_info: Dict, user_id: str, data: Dict) -> SecurityPlan:
    """
    Creates a security plan in RegScale.
    :param SSPDoc ssp_doc: The SSP document object.
    :param Dict cloud_info: A dictionary containing cloud deployment model information.
    :param str user_id: The ID of the user creating the security plan.
    :param Dict[str, Any] data: The processed data.
    :return: The security plan object.
    :rtype: SecurityPlan
    """
    doc_text_dict = data.get("doc_text_dict")
    owner, isso = data.get("owner"), data.get("isso")
    prepared_by: PreparedBy = data.get("prepared_by")
    prepared_for: PreparedBy = data.get("prepared_for")
    ssp = SecurityPlan(
        systemName=ssp_doc.name,
        fedrampId=ssp_doc.fedramp_id,
        systemOwnerId=owner.id if owner else user_id,
        planInformationSystemSecurityOfficerId=isso.id if isso else user_id,
        status="Operational",
        description=ssp_doc.description,
        authorizationBoundary=ssp_doc.authorization_path,
        tenantsId=1,
        overallCategorization=ssp_doc.fips_199_level,
        bModelSaaS=cloud_info.get("saas", False),
        bModelPaaS=cloud_info.get("paas", False),
        bModelIaaS=cloud_info.get("iaas", False),
        bModelOther=cloud_info.get("other_service_model", False),
        bDeployGov=cloud_info.get("deploy_gov", False),
        bDeployHybrid=cloud_info.get("deploy_hybrid", False),
        bDeployPrivate=cloud_info.get("deploy_private", False),
        bDeployPublic=cloud_info.get("deploy_public", False),
        bDeployOther=cloud_info.get("deploy_other", False),
        deployOtherRemarks=ssp_doc.deployment_model,
        dateSubmitted=ssp_doc.date_submitted,
        approvalDate=ssp_doc.approval_date,
        expirationDate=get_expiration_date(),
        fedrampAuthorizationLevel=ssp_doc.fips_199_level,
        defaultAssessmentDays=365,
        version=data.get("version", "1.0"),
        executiveSummary="\n".join(doc_text_dict.get("Introduction", [])),
        purpose="\n".join(doc_text_dict.get("Purpose", [])),
        cspOrgName=prepared_by.name if prepared_by else None,
        cspAddress=prepared_by.street if prepared_by else None,
        cspOffice=prepared_by.building if prepared_by else None,
        cspCityState=prepared_by.city_state_zip if prepared_by else None,
        prepOrgName=prepared_for.name if prepared_for else None,
        prepAddress=prepared_for.street if prepared_for else None,
        prepOffice=prepared_for.building if prepared_for else None,
        prepCityState=prepared_for.city_state_zip if prepared_for else None,
    ).create()
    return ssp


def save_security_plan_info(
    ssp: SecurityPlan, cloud_info: Dict, ssp_doc: SSPDoc, user_id: str, data: Dict
) -> SecurityPlan:
    """
    Saves the security plan information to the database.
    :param SecurityPlan ssp: The security plan object.
    :param Dict cloud_info: A dictionary containing cloud deployment model information.
    :param SSPDoc ssp_doc: The SSP document object.
    :param str user_id: The ID of the user performing the operation.
    :param Dict[str, Any] data: The processed data.
    :return: The updated security plan object.
    :rtype: SecurityPlan
    """
    prepared_by: PreparedBy = data.get("prepared_by")
    prepared_for: PreparedBy = data.get("prepared_for")
    doc_text_dict: Dict = data.get("doc_text_dict")
    owner, isso = data.get("owner"), data.get("isso")

    logger.info(f"Updating SSP: {ssp.systemName}")
    ssp.fedrampId = ssp_doc.fedramp_id
    ssp.systemName = ssp_doc.name
    ssp.status = "Operational"
    ssp.description = ssp_doc.description
    ssp.authorizationBoundary = ssp_doc.authorization_path
    ssp.systemOwnerId = owner.id if owner else user_id
    ssp.planInformationSystemSecurityOfficerId = isso.id if isso else user_id
    ssp.overallCategorization = ssp_doc.fips_199_level
    ssp.bModelSaaS = cloud_info.get("saas", False)
    ssp.bModelPaaS = cloud_info.get("paas", False)
    ssp.bModelIaaS = cloud_info.get("iaas", False)
    ssp.bModelOther = cloud_info.get("other_service_model", False)
    ssp.bDeployGov = cloud_info.get("deploy_gov", False)
    ssp.bDeployHybrid = cloud_info.get("deploy_hybrid", False)
    ssp.bDeployPrivate = cloud_info.get("deploy_private", False)
    ssp.bDeployPublic = cloud_info.get("deploy_public", False)
    ssp.bDeployOther = cloud_info.get("deploy_other", False)
    ssp.deployOtherRemarks = ssp_doc.deployment_model
    ssp.dateSubmitted = ssp_doc.date_submitted
    ssp.approvalDate = ssp_doc.approval_date
    ssp.expirationDate = get_expiration_date()  # ssp_doc.expiration_date
    ssp.fedrampAuthorizationLevel = ssp_doc.fips_199_level
    ssp.version = data.get("version", "1.0")
    if prepared_by:
        ssp.cspOrgName = prepared_by.name
        ssp.cspAddress = prepared_by.street
        ssp.cspOffice = prepared_by.building
        ssp.cspCityState = prepared_by.city_state_zip
    if prepared_for:
        ssp.prepOrgName = prepared_for.name
        ssp.prepAddress = prepared_for.street
        ssp.prepOffice = prepared_for.building
        ssp.prepCityState = prepared_for.city_state_zip

    ssp.executiveSummary = "\n".join(doc_text_dict.get("Introduction", []))
    ssp.purpose = "\n".join(doc_text_dict.get("Purpose", []))
    ssp.save()
    return ssp


def create_leveraged_authorizations(services: List[LeveragedService], user_id: str, ssp_id: int, approval_date: str):
    """
    Creates leveraged authorization records for each service.

    :param List[LeveragedService] services: A list of services to be created.
    :param str user_id: The ID of the user creating the services.
    :param int ssp_id: The ID of the security plan these services are associated with.
    :param str approval_date: The date of approval.

    """
    existing_authorizations: List[LeveragedAuthorization] = LeveragedAuthorization.get_all_by_parent(parent_id=ssp_id)
    logger.info(f"Found {len(existing_authorizations)} existing LeveragedAuthorizations")
    for service in services:
        existing_service = next(
            (a for a in existing_authorizations if a.fedrampId == service.auth_type_fedramp_id),
            None,
        )

        if existing_service:
            logger.debug(existing_service.model_dump())
            existing_service.title = service.fedramp_csp_name
            existing_service.fedrampId = service.auth_type_fedramp_id
            existing_service.ownerId = user_id
            existing_service.securityPlanId = ssp_id
            existing_service.dateAuthorized = approval_date or get_current_datetime()
            existing_service.description = service.cso_name
            existing_service.dataTypes = service.data_types or "unknown"
            existing_service.authorizedUserTypes = service.authorized_user_authentication or "unknown"
            existing_service.impactLevel = service.impact_level
            existing_service.natureOfAgreement = service.agreement_type or "unknown"
            existing_service.tenantsId = 1
            existing_service.save()
        else:
            LeveragedAuthorization(
                title=service.fedramp_csp_name,
                fedrampId=service.auth_type_fedramp_id or "unknown",
                ownerId=user_id,
                securityPlanId=ssp_id,
                dateAuthorized=approval_date or get_current_datetime(),
                servicesUsed="unknown",
                description=service.cso_name,
                dataTypes=service.data_types or "unknown",
                authorizationType="SSO",
                authorizedUserTypes=service.authorized_user_authentication or "unknown",
                authenticationType="unknown",
                impactLevel=service.impact_level or "Low",
                natureOfAgreement=service.agreement_type or "unknown",
                tenantsId=1,
            ).create()
            logger.debug(f"LeveragedAuthorization: {service.fedramp_csp_name}")


def create_ports_and_protocols(ports_and_protocols: List[PortsAndProtocolData], ssp_id: int):
    """
    Creates port and protocol records for each entry.

    :param List[PortsAndProtocolData] ports_and_protocols: A list of ports and protocols to be created.
    :param int ssp_id: The ID of the security plan these ports and protocols are associated with.

    """
    existing_ports: List[PortsProtocol] = PortsProtocol.get_all_by_parent(
        parent_id=ssp_id, parent_module="securityplans"
    )
    logger.info(f"Found {len(existing_ports)} existing Ports & Protocols")
    created_count = 0
    for port in ports_and_protocols:
        port_to_create = PortsProtocol(
            service=port.service,
            startPort=port.start_port,
            endPort=port.end_port,
            protocol=port.protocol,
            purpose=port.purpose,
            usedBy=port.used_by,
            parentId=ssp_id,
            parentModule="securityplans",
        )
        existing = False
        for existing_port in existing_ports:
            if (
                existing_port.startPort == port_to_create.startPort
                and existing_port.endPort == port_to_create.endPort
                and existing_port.protocol == port_to_create.protocol
                and existing_port.service == port_to_create.service
                and existing_port.purpose == port_to_create.purpose
                and existing_port.usedBy == port_to_create.usedBy
                and existing_port.parentId == port_to_create.parentId
                and existing_port.parentModule == port_to_create.parentModule
            ):
                existing = True
                break

        if not existing:
            port_to_create.create()
            created_count += 1
    logger.info(f"Created {created_count} Port & Protocols")


def extract_and_upload_images(file_name: str, parent_id: int) -> None:
    """
    Extracts embedded images from a document and uploads them to RegScale with improved filenames.

    :param str file_name: The path to the document file.
    :param int parent_id: The parent ID in RegScale to associate the images with.

    """
    logger.debug(f"Processing embedded images in {file_name} for parent ID {parent_id}...")
    existing_files = fetch_existing_files(parent_id)
    extracted_files_path = extract_embedded_files(file_name)
    upload_files(extracted_files_path, existing_files, parent_id)


def fetch_existing_files(parent_id: int) -> list:
    """
    Fetches existing files for a given parent ID from RegScale.

    :param int parent_id: The parent ID whose files to fetch.
    :return: A list of existing files.
    :rtype: list
    """
    return File.get_files_for_parent_from_regscale(parent_id=parent_id, parent_module="securityplans")


def extract_embedded_files(file_name: str) -> str:
    """
    Extracts embedded files from a document and returns the path where they are stored.

    :param str file_name: The path to the document file.
    :return: The path where embedded files are extracted to.
    :rtype: str
    """
    file_dump_path = os.path.join(gettempdir(), "imagedump")
    with zipfile.ZipFile(file_name, mode="r") as archive:
        for file in archive.filelist:
            logger.debug(f"Extracting file: {file.filename}")
            if file.filename.startswith("word/media/") and file.file_size > 200000:  # 200KB filter
                archive.extract(file, path=file_dump_path)
    return file_dump_path


def upload_files(extracted_files_path: str, existing_files: list, parent_id: int) -> None:
    """
    Uploads files from a specified path to RegScale, avoiding duplicates.

    :param str extracted_files_path: The path where files are stored.
    :param list existing_files: A list of files already existing in RegScale to avoid duplicates.
    :param int parent_id: The parent ID in RegScale to associate the uploaded files with.

    """
    media_path = os.path.join(extracted_files_path, "word", "media")
    if not os.path.exists(media_path):
        os.makedirs(media_path)

    for filename in os.listdir(media_path):
        full_file_path = os.path.join(media_path, filename)
        if os.path.isfile(full_file_path):
            if not file_already_exists(filename, existing_files):
                logger.info(f"Uploading embedded image to RegScale: {filename}")
                upload_file_to_regscale(full_file_path, parent_id)


def file_already_exists(filename: str, existing_files: list) -> bool:
    """
    Checks if a file already exists in RegScale.

    :param str filename: The name of the file to check.
    :param list existing_files: A list of files already existing in RegScale.
    :return: True if the file exists, False otherwise.
    :rtype: bool
    """
    return any(f.trustedDisplayName == filename for f in existing_files)


def upload_file_to_regscale(
    file_path: str,
    parent_id: int,
) -> None:
    """
    Uploads a single file to RegScale.

    :param str file_path: The full path to the file to upload.
    :param int parent_id: The parent ID in RegScale to associate the file with.
    """
    api = Api()
    File.upload_file_to_regscale(
        file_name=file_path,
        parent_id=parent_id,
        parent_module=SecurityPlan.get_module_slug(),
        api=api,
    )


def safe_get_first_key(dictionary: dict) -> Optional[str]:
    """Safely get the first key of a dictionary.
    :param dict dictionary: The dictionary to get the first key from.
    :return: The first key of the dictionary, or None if the dictionary is empty.
    :rtype: Optional[str]
    """
    try:
        return next(iter(dictionary))
    except StopIteration:
        return None


def parse_version(version_str: str) -> float:
    """Parse version string to a float, safely.
    :param str version_str: The version string to parse.
    :return: The version number as a float, or 0 if the version string is not a valid number.
    :rtype: float
    """
    try:
        if not version_str:
            return 0
        return float(version_str)
    except ValueError:
        return 0


def get_max_version(entries: List[Dict]) -> Optional[str]:
    """Find the maximum version from a list of entries.
    :param List[Dict] entries: The list of entries to find the maximum version from.
    :return: The maximum version from the entries, or None if no valid versions are found.
    :rtype: Optional[str]
    """
    max_version = None
    for entry in entries:
        version_str = entry.get("Version", "")
        version_num = parse_version(version_str)
        if version_num is not None:
            max_version = max(max_version, version_str, key=parse_version)
    logger.debug(f"Version: {max_version}")
    return max_version
