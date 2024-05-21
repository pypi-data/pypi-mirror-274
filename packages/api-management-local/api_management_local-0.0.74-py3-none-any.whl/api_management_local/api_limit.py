from database_mysql_local.generic_crud import GenericCRUD
from logger_local.MetaLogger import MetaLogger

from .constants import API_MANAGEMENT_CODE_LOGGER_OBJECT
from .utils import ApiManagementLocalUtils


class APILimitsLocal(GenericCRUD, metaclass=MetaLogger, object=API_MANAGEMENT_CODE_LOGGER_OBJECT):
    def __init__(self, is_test_data: bool = False) -> None:
        super().__init__(default_schema_name="api_limit",
                         default_table_name="api_limit_table",
                         default_view_table_name="api_limit_view",
                         is_test_data=is_test_data)
        self.utils = ApiManagementLocalUtils(is_test_data=is_test_data)

    # The logic is that the limit can be in the level of api_type and user_external if provided / found.
    #   Otherwise, on the level of api_type.
    # TODO: add tests for both cases.
    def get_api_limit_dict_by_api_type_id_user_external_id(
            self, *, api_type_id: int, user_external_id: int = None) -> dict:
        """Returns a dict with the following keys:
        - soft_limit_value (int)
        - soft_limit_unit (str)
        - hard_limit_value (int)
        - hard_limit_unit (str)
        """
        self.utils.validate_api_type_id(api_type_id)
        try:
            user_external_id = user_external_id or self.utils.get_user_external_id_by_api_type_id(api_type_id)
        except Exception as e:
            self.logger.warning("user_external_id not found", object={"api_type_id": api_type_id})

        select_clause = "soft_limit_value, soft_limit_unit, hard_limit_value, hard_limit_unit"
        where = "api_type_id = %s AND user_external_id " + ("= %s" if user_external_id else "IS NULL")
        params = (api_type_id, user_external_id) if user_external_id else (api_type_id,)
        api_limit_result = self.select_one_dict_by_where(
            select_clause_value=select_clause, where=where, params=params)
        if not api_limit_result:  # TODO: can we do it with a single query?
            where = "api_type_id = %s AND user_external_id IS NULL"
            params = (api_type_id,)
            api_limit_result = self.select_one_dict_by_where(
                select_clause_value=select_clause, where=where, params=params)
            if not api_limit_result:
                raise Exception(f"no api_limit found for "
                                f"api_type_id={api_type_id} and user_external_id={user_external_id}")
        return api_limit_result
