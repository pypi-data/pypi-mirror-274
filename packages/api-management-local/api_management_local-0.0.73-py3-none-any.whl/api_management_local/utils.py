from functools import lru_cache

from database_mysql_local.generic_crud import GenericCRUD


class ApiManagementLocalUtils(GenericCRUD):
    def __init__(self, is_test_data: bool = False) -> None:
        super().__init__(default_schema_name="api_type_user_external",
                         default_table_name="api_type_user_external_table",
                         default_view_table_name="api_type_user_external_view",
                         default_column_name="api_type_id", is_test_data=is_test_data)

    @staticmethod
    def validate_api_type_id(api_type_id: int) -> None:
        if api_type_id is None:
            raise ValueError("api_type_id cannot be None")
        if not isinstance(api_type_id, int):
            raise ValueError(f"api_type_id is not an integer ({api_type_id}, type: {type(api_type_id)})")
        if api_type_id < 0:
            raise ValueError(f"api_type_id is negative ({api_type_id})")

    @lru_cache
    def get_user_external_id_by_api_type_id(self, api_type_id: int) -> int:
        """We prefer to get the user_external_id as parameter.
        If user_external_id is None
        TODO: We should first search for user_external_id in user_external_table.
                In the case of Auth2, we only need the username
                Circlez.ai user might have different usernames in external systems.
                Example: google_contacts.pull_contacts_with_stored_token("play1@circ.zone")
        If not found, can search for default user_external_id in api_type_user_external_table"""
        self.validate_api_type_id(api_type_id)
        user_external_id = self.select_one_value_by_column_and_value(
            column_value=api_type_id, select_clause_value="user_external_id")
        if not user_external_id:
            raise Exception(f"no default user_external_id found for api_type_id={api_type_id}")
        return user_external_id
