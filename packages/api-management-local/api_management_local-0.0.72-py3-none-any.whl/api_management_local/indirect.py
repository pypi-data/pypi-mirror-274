import http
import json

from logger_local.MetaLogger import MetaLogger
from star_local.star_local import StarsLocal

from .api_call import APICallsLocal
from .api_limit_status import APILimitStatus
from .api_management_local import APIManagementsLocal
from .api_type import ApiTypesLocal
from .constants import API_MANAGEMENT_CODE_LOGGER_OBJECT
from .utils import ApiManagementLocalUtils


class InDirect(APICallsLocal, metaclass=MetaLogger, object=API_MANAGEMENT_CODE_LOGGER_OBJECT):
    def __init__(self, is_test_data: bool = False) -> None:
        super().__init__(is_test_data=is_test_data)
        self.api_type_local = ApiTypesLocal(is_test_data=is_test_data)
        self.api_management_local = APIManagementsLocal(is_test_data=is_test_data)
        self.stars_local = StarsLocal()
        self.utils = ApiManagementLocalUtils(is_test_data=is_test_data)

    def before_call_api(self, *, api_type_id: int, user_external_id: int = None, endpoint: str,
                        outgoing_body: dict or json, outgoing_header: dict or json) -> (
            APILimitStatus or None, int, int or None, str or None):
        """:param outgoing_body: {"user_identifier": "test", "password": "test"}
        :param outgoing_header: {'Content-Type': 'application/json'}"""
        outgoing_body = self.__to_json(outgoing_body)
        outgoing_header = self.__to_json(outgoing_header)
        action_id = self.api_type_local.get_action_id_by_api_type_id(api_type_id)
        self.stars_local.verify_profile_star_before_action(action_id)
        self.api_management_local.sleep_per_interval(api_type_id)
        user_external_id = user_external_id or self.utils.get_user_external_id_by_api_type_id(api_type_id)
        http_status_code, response_body, outgoing_body_significant_fields_hash = self.api_management_local.check_cache(
            api_type_id=api_type_id, outgoing_body=outgoing_body)

        if response_body is None:
            is_network = None
            api_limit_status = self.api_management_local.check_limit(
                user_external_id=user_external_id, api_type_id=api_type_id)
        else:
            is_network = False
            api_limit_status = None

        api_call_dict = {'api_type_id': api_type_id, 'user_external_id': user_external_id,
                         'endpoint': endpoint, 'outgoing_header': str(outgoing_header),
                         'outgoing_body': str(outgoing_body),
                         'outgoing_body_significant_fields_hash': outgoing_body_significant_fields_hash,
                         'is_network': is_network}
        api_call_id = self.insert_api_call_dict(api_call_dict=api_call_dict)

        return api_limit_status, api_call_id, http_status_code, response_body

    # TODO api_type_id to Enum?
    def after_call_api(self, *, api_type_id: int, user_external_id: int = None, endpoint: str,
                       outgoing_body: dict or json, outgoing_header: dict or json,
                       response_body: dict or json, incoming_message: dict or json,
                       api_call_id: int, http_status_code: int, used_cache: bool = None) -> None:
        """:param outgoing_body: {"user_identifier": "test", "password": "test"}
        :param outgoing_header: {'Content-Type': 'application/json'}
        :param response_body: {"message": "hander.ts login: Recived login from ...",
                "userDetails": {"firstName": "Test", "lastName": "Test",
                "userId": "1", "profileId": "1"}}
        :param incoming_message: same as response_body"""
        # TODO shall we add _json suffix (both in database and here)?
        outgoing_body = self.__to_json(outgoing_body)
        outgoing_header = self.__to_json(outgoing_header)
        response_body = self.__to_json(response_body)
        incoming_message = self.__to_json(incoming_message)
        self.utils.validate_api_type_id(api_type_id=api_type_id)
        if http_status_code == http.HTTPStatus.OK:
            self.stars_local.api_executed(api_type_id=api_type_id)

        is_network = not used_cache
        user_external_id = user_external_id or self.utils.get_user_external_id_by_api_type_id(api_type_id)
        # where="api_call_id= {}".format(api_call_id)
        update_data = {'user_external_id': user_external_id, 'endpoint': endpoint, 'outgoing_body': outgoing_body,
                       'outgoing_header': outgoing_header, 'http_status_code': http_status_code,
                       'response_body': response_body, 'incoming_message': incoming_message,
                       'is_network': is_network}
        super().update_by_column_and_value(column_value=api_call_id, data_dict=update_data)

    # TODO Move to Python SDK?
    def __to_json(self, data_dict: dict) -> json:
        if isinstance(data_dict, dict):
            return json.dumps(data_dict)
        else:
            return data_dict
