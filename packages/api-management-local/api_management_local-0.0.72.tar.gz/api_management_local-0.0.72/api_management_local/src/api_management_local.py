import http
import json
import random
import sys
import time

import requests
from database_mysql_local.generic_crud import GenericCRUD
from logger_local.MetaLogger import MetaLogger

from .Exception_API import ApiTypeDisabledException, ApiTypeIsNotExistException, PassedTheHardLimitException
from .api_limit import APILimitsLocal
from .api_limit_status import APILimitStatus
from .constants import API_MANAGEMENT_CODE_LOGGER_OBJECT
from .utils import ApiManagementLocalUtils


class APIManagementsLocal(GenericCRUD, metaclass=MetaLogger, object=API_MANAGEMENT_CODE_LOGGER_OBJECT):
    def __init__(self, is_test_data: bool = False) -> None:
        super().__init__(default_schema_name="api_type", default_column_name="api_type_id",
                         default_table_name="api_type_table", default_view_table_name="api_type_view",
                         is_test_data=is_test_data)
        self.api_limits = APILimitsLocal(is_test_data=is_test_data)
        self.utils = ApiManagementLocalUtils(is_test_data=is_test_data)

    def delete_api(self, *, api_type_id: int, user_external_id: int = None,
                   endpoint: str, data: dict) -> requests.Response or None:
        """Returns the response of the delete request"""
        return self.__send_request(api_type_id=api_type_id, user_external_id=user_external_id,
                                   endpoint=endpoint, data=data, method="delete")

    def get_api(self, *, api_type_id: int, user_external_id: int = None, endpoint: str,
                data: dict) -> requests.Response or None:
        """Returns the response of the get request"""
        return self.__send_request(api_type_id=api_type_id, user_external_id=user_external_id,
                                   endpoint=endpoint, data=data, method="get")

    def put_api(self, *, api_type_id: int, user_external_id: int = None, endpoint: str,
                data: dict) -> requests.Response or None:
        """Returns the response of the put request"""
        return self.__send_request(api_type_id=api_type_id, user_external_id=user_external_id,
                                   endpoint=endpoint, data=data, method="put")

    def __send_request(self, *, api_type_id: int, user_external_id: int, endpoint: str, data: dict,
                       method: str) -> requests.Response:
        """Returns the response of the request"""
        check_limit = self.check_limit(user_external_id=user_external_id, api_type_id=api_type_id)
        if check_limit == APILimitStatus.BELOW_SOFT_LIMIT:
            response = requests.request(method=method, url=endpoint, data=data)
            return response

        elif check_limit == APILimitStatus.BETWEEN_SOFT_LIMIT_AND_HARD_LIMIT:
            self.logger.warn("you passed the soft limit")

        else:
            self.logger.error("you passed the hard limit")
            raise PassedTheHardLimitException

    def _second_from_last_network_api(self, api_type_id: int) -> int:
        """Returns the number of seconds from the last network api call of the given api_type_id"""
        self.utils.validate_api_type_id(api_type_id)
        query = f"""
            SELECT TIMESTAMPDIFF(SECOND, start_timestamp, NOW())
            FROM api_call.api_call_view
            WHERE api_type_id = %s
              AND is_network = TRUE
            ORDER BY start_timestamp DESC
            LIMIT 1;"""
        self.cursor.execute(query, (api_type_id,))
        second_from_last_network_api = (self.cursor.fetchone() or [sys.maxsize])[0]
        return second_from_last_network_api

    def get_hard_limit_by_api_type_id(self, api_type_id: int) -> dict:
        """Returns the hard limit value and unit of the given api_type_id"""
        self.utils.validate_api_type_id(api_type_id)
        hard_limit_dict = self.select_one_dict_by_column_and_value(
            schema_name="api_limit", view_table_name="api_limit_view",
            column_name="api_type_id", column_value=api_type_id,
            select_clause_value="hard_limit_value, hard_limit_unit")

        return hard_limit_dict

    def get_actual_api_succ_network_by_api_type_id_last_x_units(
            self, *, api_type_id: int, user_external_id: int = None, value: int, unit: str) -> int:
        """Returns the number of successful network api calls of the given api_type_id in the last x units"""

        query = f"""
            SELECT COUNT(*) FROM api_call.api_call_view
            WHERE api_type_id = %s AND user_external_id = %s
                AND TIMESTAMPDIFF({unit}, created_timestamp, NOW()) <= %s
                AND http_status_code = %s AND is_network=TRUE
        """
        user_external_id = user_external_id or self.utils.get_user_external_id_by_api_type_id(api_type_id)
        self.cursor.execute(query, (api_type_id, user_external_id, value, http.HTTPStatus.OK.value))
        actual_succ_count = self.cursor.fetchone()
        if not actual_succ_count:
            raise Exception(f"no succ count found for api_type_id={api_type_id}, "
                            f"user_external_id={user_external_id}, value={value}, unit={unit}")

        return actual_succ_count[0]

    def sleep_per_interval(self, api_type_id: int) -> None:
        """Sleeps for a random interval between the min and max interval of the given api_type_id"""
        self.utils.validate_api_type_id(api_type_id)
        interval_min_seconds, interval_max_seconds = self.select_one_tuple_by_where(
            schema_name="api_type",
            view_table_name="api_type_view", where="is_enabled=TRUE AND api_type_id=%s",
            params=(api_type_id,), select_clause_value="interval_min_seconds, interval_max_seconds")
        self._verify_api_type_exists_and_enabled(api_type_id)
        random_interval = random.uniform(interval_min_seconds, interval_max_seconds)
        self.logger.info(f"Got {random_interval} from the interval range: "
                         f"[{interval_min_seconds}, {interval_max_seconds}]")
        second_from_last_network_api = self._second_from_last_network_api(api_type_id)
        if random_interval > second_from_last_network_api:
            sleep_second = random_interval - second_from_last_network_api
            self.logger.info(f"sleeping {sleep_second} seconds")
            time.sleep(sleep_second)
        else:
            self.logger.info("No sleep is needed")

    def check_cache(self, *, api_type_id: int, outgoing_body: dict) -> (int or None, str or None, int):
        """Returns the http_status_code, response_body and outgoing_body_significant_fields_hash
            of the cached api call of the given api_type_id and outgoing_body"""
        self.utils.validate_api_type_id(api_type_id)
        outgoing_body_significant_fields_hash = hash(
            self._get_json_with_only_sagnificant_fields_by_api_type_id(
                data_dict=outgoing_body, api_type_id=api_type_id))
        query = """
            SELECT http_status_code, response_body
                FROM api_call.api_call_view
                         JOIN api_type.api_type_view
                              ON api_type.api_type_view.api_type_id = api_call.api_call_view.api_type_id
                WHERE api_call_view.api_type_id = %s
                  AND http_status_code = %s
                  AND TIMESTAMPDIFF(MINUTE, api_call.api_call_view.start_timestamp, NOW())
                    <= api_type_view.expiration_value
                  AND outgoing_body_significant_fields_hash = %s
                  AND is_network = TRUE
                ORDER BY api_call_id DESC
                LIMIT 1"""
        self.cursor.execute(query, (api_type_id, http.HTTPStatus.OK.value, outgoing_body_significant_fields_hash))

        result = self.cursor.fetchone()
        if result is None:
            http_status_code, response_body = None, None
        else:
            http_status_code, response_body = result
        return http_status_code, response_body, outgoing_body_significant_fields_hash

    def check_limit(self, *, api_type_id: int, user_external_id: int = None) -> APILimitStatus:
        """Returns the APILimitStatus of the given user_external_id and api_type_id"""

        api_limits_dict = self.api_limits.get_api_limit_dict_by_api_type_id_user_external_id(
            api_type_id=api_type_id, user_external_id=user_external_id)
        soft_limit_value = api_limits_dict["soft_limit_value"]
        soft_limit_unit = api_limits_dict["soft_limit_unit"]
        hard_limit_value = api_limits_dict["hard_limit_value"]
        # hard_limit_unit = api_limits_dict["hard_limit_unit"]
        api_succ = self.get_actual_api_succ_network_by_api_type_id_last_x_units(
            user_external_id=user_external_id, api_type_id=api_type_id,
            value=soft_limit_value, unit=soft_limit_unit)

        # TODO if not GREATER_THAN_HARD_LIMIT check_money_budget()

        if api_succ < soft_limit_value:
            return APILimitStatus.BELOW_SOFT_LIMIT
        elif soft_limit_value <= api_succ < hard_limit_value:
            return APILimitStatus.BETWEEN_SOFT_LIMIT_AND_HARD_LIMIT
        else:
            return APILimitStatus.GREATER_THAN_HARD_LIMIT

    def _get_json_with_only_sagnificant_fields_by_api_type_id(self, *, data_dict: dict, api_type_id: int) -> json:
        """Returns the json with only the significant fields of the given data_dict and api_type_id"""
        self.utils.validate_api_type_id(api_type_id)
        result = self.select_multi_dict_by_where(
            schema_name="api_type", view_table_name="api_type_field_view",
            where="api_type_id=%s AND field_significant = TRUE",
            params=(api_type_id,), select_clause_value="field_name")

        # TODO Support hierarchy fields in json like we have in messages i.e. Body.Text.Data,
        #  please also add tests based on data we have in our api_call_table
        significant_fields = [row["field_name"] for row in result]
        filtered_data = {key: data_dict[key]
                         for key in significant_fields if key in data_dict}
        filtered_json = json.dumps(filtered_data)

        return filtered_json

    def _verify_api_type_exists_and_enabled(self, api_type_id: int) -> None:
        """Checks if the given api_type_id exists and enabled
            and raises ApiTypeIsNotExistException or ApiTypeDisabledException if not"""
        self.utils.validate_api_type_id(api_type_id)
        is_enabled = self.select_one_value_by_column_and_value(
            view_table_name="api_type_view", select_clause_value="is_enabled",
            column_value=api_type_id)
        if is_enabled is None:
            raise ApiTypeIsNotExistException
        elif is_enabled == 0:
            raise ApiTypeDisabledException

    # TODO Develop incoming_api
    # def incoming_api(self, api_call_dict: str):
    #     api_call.insert( api_call_dict )
