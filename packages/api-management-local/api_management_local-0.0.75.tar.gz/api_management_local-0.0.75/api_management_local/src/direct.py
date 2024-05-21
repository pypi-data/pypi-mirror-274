from http import HTTPStatus

import requests
from logger_local.MetaLogger import MetaLogger
from star_local.star_local import StarsLocal

from .exception_api import PassedTheHardLimitException
from .api_call import APICallsLocal
from .api_limit_status import APILimitStatus
from .api_management_local import APIManagementsLocal
from .api_type import ApiTypesLocal
from .constants import API_MANAGEMENT_CODE_LOGGER_OBJECT
from .utils import ApiManagementLocalUtils


class Direct(metaclass=MetaLogger, object=API_MANAGEMENT_CODE_LOGGER_OBJECT):
    def __init__(self, is_test_data: bool = False) -> None:
        self.api_type_local = ApiTypesLocal(is_test_data=is_test_data)
        self.api_call_local = APICallsLocal(is_test_data=is_test_data)
        self.api_management_local = APIManagementsLocal(is_test_data=is_test_data)
        self.stars_local = StarsLocal()
        self.utils = ApiManagementLocalUtils(is_test_data=is_test_data)

    # TODO if we got endpoint_url call logger.warning() as we prefer to get the endpoint_url from api_type.api_type_table
    def try_to_call_api(self, *, api_type_id: int, user_external_id: int = None, endpoint_url: str,
                        outgoing_body: dict, outgoing_header: dict) -> dict:
        action_id = self.api_type_local.get_action_id_by_api_type_id(api_type_id)
        self.stars_local.verify_profile_star_before_action(action_id)
        self.api_management_local.sleep_per_interval(api_type_id)

        user_external_id = user_external_id or self.utils.get_user_external_id_by_api_type_id(api_type_id)

        http_status_code, response_body_json, outgoing_body_significant_fields_hash = self.api_management_local.check_cache(
            api_type_id=api_type_id, outgoing_body=outgoing_body)
        outgoing_header_json = ApiManagementLocalUtils.to_json(outgoing_header)
        outgoing_body_json = ApiManagementLocalUtils.to_json(outgoing_body)
        api_call_dict = {'api_type_id': api_type_id, 'user_external_id': user_external_id, 'endpoint_url': endpoint_url,
                         'outgoing_header_json': outgoing_header_json, 'outgoing_body_json': outgoing_body_json,
                         'outgoing_body_significant_fields_hash': outgoing_body_significant_fields_hash,
                         'http_status_code': http_status_code, 'response_body_json': response_body_json}
        if response_body_json is None:
            check_limit = self.api_management_local.check_limit(
                user_external_id=user_external_id, api_type_id=api_type_id)
            self.logger.info(object={"check_limit": check_limit})
            if check_limit == APILimitStatus.BETWEEN_SOFT_LIMIT_AND_HARD_LIMIT:
                self.logger.warn("You excced the soft limit")
            if check_limit != APILimitStatus.GREATER_THAN_HARD_LIMIT:
                output_response = requests.post(url=endpoint_url, data=outgoing_body, headers=outgoing_header)
                http_status_code = output_response.status_code
                # text = output_response.text
                incoming_message_json = output_response.content.decode('utf-8')
                response_body_json = ApiManagementLocalUtils.to_json(output_response.json())
                if http_status_code == HTTPStatus.OK.value:
                    self.stars_local.api_executed(api_type_id=api_type_id)
                api_call_dict.update({"incoming_message_json": incoming_message_json, "http_status_code": http_status_code,
                                      "response_body_json": response_body_json, "is_network": True})

                api_call_id = self.api_call_local.insert_api_call_dict(api_call_dict)

            else:
                self.logger.error("you passed the hard limit")
                raise PassedTheHardLimitException
        else:
            api_call_dict.update({"is_network": False, "incoming_message_json": ""})
            self.stars_local.api_executed(api_type_id=api_type_id)
            api_call_id = self.api_call_local.insert_api_call_dict(api_call_dict)

        # return request("post", url=endpoint_url, data=outgoing_body, json=json, **kwargs)
        # note that response_body_json used to be `text` and http_status_code used to be `http_status_code`
        try_to_call_api_result = {'http_status_code': http_status_code, 'response_body_json': response_body_json,
                                  'api_call_id': api_call_id}
        return try_to_call_api_result