from logger_local.LoggerComponentEnum import LoggerComponentEnum
from python_sdk_remote.utilities import get_brand_name


BRAND_NAME = get_brand_name()
# TODO Please use/create AUTHENTICATION_API_VERSION_DICT[environment_name] in url-remote-python-package
AUTHENTICATION_API_VERSION = 1
API_MANAGEMENT_LOCAL_PYTHON_COMPONENT_ID = 212
API_MANAGEMENT_LOCAL_PYTHON_COMPONENT_NAME = "api-management-local-python-package"
DEVELOPER_EMAIL = "heba.a@circ.zone"


API_MANAGEMENT_CODE_LOGGER_OBJECT = {
    'component_id': API_MANAGEMENT_LOCAL_PYTHON_COMPONENT_ID,
    'component_name': API_MANAGEMENT_LOCAL_PYTHON_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
    'developer_email': DEVELOPER_EMAIL
}
