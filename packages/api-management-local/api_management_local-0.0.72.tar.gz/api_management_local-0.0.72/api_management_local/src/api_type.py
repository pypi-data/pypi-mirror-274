from database_mysql_local.generic_crud import GenericCRUD
from logger_local.MetaLogger import MetaLogger

from .Exception_API import ApiTypeDisabledException, ApiTypeIsNotExistException
from .constants import API_MANAGEMENT_CODE_LOGGER_OBJECT
from .utils import ApiManagementLocalUtils


class ApiTypesLocal(GenericCRUD, metaclass=MetaLogger, object=API_MANAGEMENT_CODE_LOGGER_OBJECT):
    def __init__(self, is_test_data: bool = False) -> None:
        super().__init__(default_schema_name="api_type", default_table_name="api_type_table",
                         default_view_table_name="api_type_view", default_column_name="api_type_id",
                         is_test_data=is_test_data)

    def get_action_id_by_api_type_id(self, api_type_id: int) -> int:
        ApiManagementLocalUtils.validate_api_type_id(api_type_id)
        where = "api_type_id = %s AND is_enabled = TRUE"
        action_id = self.select_one_value_by_where(select_clause_value="action_id",
                                                   where=where, params=(api_type_id,))

        # if api_type_id does not exist in enabled api_type_table, try to get it from disabled api_type_table
        #   to decide which exception to raise
        if not action_id:
            action_id = self.select_one_value_by_column_and_value(select_clause_value="action_id",
                                                                  column_value=api_type_id)
            if not action_id:
                raise ApiTypeIsNotExistException
            else:
                raise ApiTypeDisabledException

        self.logger.end(object={"action_id": action_id})
        return action_id
