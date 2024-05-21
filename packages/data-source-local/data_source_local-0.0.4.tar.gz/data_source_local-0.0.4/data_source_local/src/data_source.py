from database_mysql_local.generic_crud import GenericCRUD
from language_remote.lang_code import LangCode
from logger_local.MetaLogger import MetaLogger

from .data_source_constants import data_source_logger_code_obj


class DataSources(GenericCRUD, metaclass=MetaLogger, object=data_source_logger_code_obj):

    def __init__(self):
        super().__init__(default_schema_name='data_source',
                         default_table_name='data_source_type_table',
                         default_view_table_name='data_source_type_ml_en_view')

    def insert_fields(self, data_source_name: str, lang_code: LangCode = LangCode.ENGLISH) -> int:
        data_source_type_id = self.insert(data_dict={})
        data_source_ml_dict = {
            'data_source_type_id': data_source_type_id,
            'lang_code': lang_code.value,
            'title': data_source_name
        }
        data_source_ml_id = self.insert(table_name='data_source_type_ml_table', data_dict=data_source_ml_dict)
        self.logger.info(object={"data_source_ml_id": data_source_ml_id, "data_source_type_id": data_source_type_id})
        return data_source_type_id

    def get_data_source_type_id_by_name(self, data_source_name: str) -> int or None:
        data_source_type_id = self.select_one_value_by_column_and_value(
            select_clause_value='data_source_type_id',
            column_name='name',
            column_value=data_source_name)
        return data_source_type_id

    def get_data_source_name_by_id(self, data_source_type_id: int) -> str or None:
        data_source_name = self.select_one_value_by_column_and_value(
            select_clause_value='name',
            column_name='data_source_type_id',
            column_value=data_source_type_id)
        return data_source_name
