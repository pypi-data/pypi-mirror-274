from logger_local.MetaLogger import MetaLogger

from .api_management_local import APIManagementsLocal
from .constants import API_MANAGEMENT_CODE_LOGGER_OBJECT
from .utils import ApiManagementLocalUtils


class APIMangementManager(APIManagementsLocal, metaclass=MetaLogger, object=API_MANAGEMENT_CODE_LOGGER_OBJECT):
    def __init__(self, is_test_data: bool = False) -> None:
        super().__init__(is_test_data=is_test_data)

    def get_get_seconds_to_sleep_after_passing_the_hard_limit(self, api_type_id: int) -> int:
        ApiManagementLocalUtils.validate_api_type_id(api_type_id=api_type_id)
        hard_limit_dict = self.get_hard_limit_by_api_type_id(api_type_id=api_type_id)
        hard_limit_value = hard_limit_dict['hard_limit_value']
        hard_limit_unit = hard_limit_dict['hard_limit_unit']

        # we must use the subquery_alias because a subquery must have an alias
        query = f"""
        SELECT TIMESTAMPDIFF(SECOND, NOW(),
                 (SELECT TIMESTAMPADD({hard_limit_unit}, 1, MIN(start_timestamp))
                  FROM (SELECT start_timestamp
                        FROM api_call.api_call_view
                        WHERE api_type_id = %s
                          AND is_network = TRUE
                        ORDER BY api_call_id DESC
                        LIMIT %s) AS subquery_alias)"""

        self.cursor.execute(query, (api_type_id, hard_limit_value))
        get_seconds_to_sleep_after_passing_the_hard_limit = self.cursor.fetchone()[0]
        return get_seconds_to_sleep_after_passing_the_hard_limit
