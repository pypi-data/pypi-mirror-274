from .version import __version__

class AwsGateway:
    API_GATEWAY = 1,
    PRIVATE_API_GATEWAY = 2,
    GOV_API_GATEWAY = 3,
    GOV_PRIVATE_API_GATEWAY = 4

def request_account_privileges(privileges: [str]) -> None:
    pass

def request_reference(reference: str) -> None:
    pass

def request_aws_api_integration(id: str, allowed_prefixes: [str], gateway: AwsGateway,
                                aws_role_arn: str,
                                api_key: str = None, name: str = None,
                                comment: str = None) -> None:
    pass

def request_azure_api_integration(id: str, allowed_prefixes: [str], tenant_id: str, application_id: str,
                                  api_key: str = None, name: str = None,
                                  comment: str = None) -> None:
    pass

def request_google_api_integration(id: str, allowed_prefixes: [str], audience: str, name: str = None,
                                   comment: str = None, api_key: str = None) -> None:
    pass

def request_share(share_name: str, db_name: str, db_role: str, accounts: [str]) -> None:
    pass

def get_held_account_privileges(privilege_names: [str]) -> [str]:
    return []

def get_missing_account_privileges(privilege_names: [str]) -> [str]:
    return privilege_names

def get_reference_associations(reference_name: str) -> [str]:
    return []

def request_event_sharing() -> None:
    pass

def is_event_sharing_enabled() -> bool:
    return False

def is_application_local_to_package() -> bool:
    return False

def is_application_authorized_for_telemetry_event_sharing() -> bool:
    return False

def is_application_all_mandatory_telemetry_event_definitions_enabled() -> bool:
    return False

def request_external_data() -> None:
    pass

def is_external_data_enabled() -> bool:
    return False
