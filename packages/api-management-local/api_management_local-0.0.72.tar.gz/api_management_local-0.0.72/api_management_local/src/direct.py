import http
import json

import requests
from logger_local.MetaLogger import MetaLogger
from star_local.star_local import StarsLocal

from .Exception_API import PassedTheHardLimitException
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

    def try_to_call_api(self, *, api_type_id: int, user_external_id: int = None, endpoint: str, outgoing_body: dict,
                        outgoing_header: dict) -> dict:
        action_id = self.api_type_local.get_action_id_by_api_type_id(api_type_id)
        self.stars_local.verify_profile_star_before_action(action_id)
        self.api_management_local.sleep_per_interval(api_type_id)

        user_external_id = user_external_id or self.utils.get_user_external_id_by_api_type_id(api_type_id)

        http_status_code, response_body, outgoing_body_significant_fields_hash = self.api_management_local.check_cache(
            api_type_id=api_type_id, outgoing_body=outgoing_body)
        if response_body is None:
            check = self.api_management_local.check_limit(
                user_external_id=user_external_id, api_type_id=api_type_id)
            self.logger.info("check= " + str(check))
            if check == APILimitStatus.BETWEEN_SOFT_LIMIT_AND_HARD_LIMIT:
                self.logger.warn("You excced the soft limit")
            if check != APILimitStatus.GREATER_THAN_HARD_LIMIT:
                output = requests.post(url=endpoint, data=outgoing_body, headers=outgoing_header)
                status_code = output.status_code
                # text = output.text
                incoming_message = output.content.decode('utf-8')
                response_body = output.json()
                response_body_str = json.dumps(response_body)
                if http.HTTPStatus.OK == status_code:
                    self.stars_local.api_executed(api_type_id=api_type_id)
                is_network = True
                api_call_dict = {
                    'api_type_id': api_type_id, 'user_external_id': user_external_id,
                    'endpoint': endpoint, 'outgoing_header': str(outgoing_header),
                    'outgoing_body': str(outgoing_body),
                    'outgoing_body_significant_fields_hash': outgoing_body_significant_fields_hash,
                    'incoming_message': incoming_message, 'http_status_code': status_code,
                    'response_body': response_body_str,
                    'is_network': is_network
                }
                api_call_id = self.api_call_local.insert_api_call_dict(api_call_dict)

            else:
                self.logger.error("you passed the hard limit")
                raise PassedTheHardLimitException
        else:
            is_network = 0
            incoming_message = ""
            api_call_dict = {'api_type_id': api_type_id, 'user_external_id': user_external_id,
                             'endpoint': endpoint, 'outgoing_header': str(outgoing_header),
                             'outgoing_body': str(outgoing_body),
                             'outgoing_body_significant_fields_hash': outgoing_body_significant_fields_hash,
                             'incoming_message': incoming_message, 'http_status_code': http_status_code,
                             'response_body': response_body, 'is_network': is_network
                             }
            self.stars_local.api_executed(api_type_id=api_type_id)
            api_call_id = self.api_call_local.insert_api_call_dict(api_call_dict)

        # return request("post", url=endpoint, data=outgoing_body, json=json, **kwargs)
        # note that response_body used to be `text` and http_status_code used to be `status_code`
        try_to_call_api_result = {'http_status_code': http_status_code, 'response_body': response_body, 'api_call_id': api_call_id}
        self.logger.end(object=try_to_call_api_result)
        return try_to_call_api_result