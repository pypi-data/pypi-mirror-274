from database_mysql_local.generic_crud_ml import GenericCRUDML
from language_remote.lang_code import LangCode


class DataSources(GenericCRUDML):

    def __init__(self):
        GenericCRUDML.__init__(self, default_schema_name='data_source',
                               default_table_name='data_source_type_table',
                               default_view_table_name='data_source_type_ml_en_view',
                               default_ml_view_table_name='data_source_type_ml_en_view')

    # TODO Why do we return two ints?
    # TODO insert_fields() per our Python Class methods naming conventions https://docs.google.com/document/d/1QtCVak8f9rOtZo9raRhYHf1-7-Sfs8rru_iv3HjTH6E/edit?usp=sharing
    def insert_data_source_type(self, data_source_type_name: str, lang_code: LangCode = LangCode.ENGLISH,
                                system_id: int = None, subsystem_id: int = None,
                                data_source_category_id: int = None) -> tuple[int, int]:
        # TODO Both are not needed if using the MetaLogger
        METHOD_NAME = 'insert_data_source_type'
        self.logger.start(METHOD_NAME, object={
            'data_source_type_name': data_source_type_name,
            'lang_code': lang_code})
        try:
            data_source_type_dict = {
                'name': data_source_type_name,
                'system_id': system_id,
                'subsystem_id': subsystem_id,
                'data_source_category_id': data_source_category_id
            }
            data_source_type_ml_dict = {
                'title': data_source_type_name,
            }
            data_source_type_id, data_source_type_ml_id = self.add_value(
                data_dict=data_source_type_dict,
                data_ml_dict=data_source_type_ml_dict,
                lang_code=lang_code,
                is_main=None,
                table_name='data_source_type_table',
                ml_table_name='data_source_type_ml_table'
            )
            # TODO Why do we need to return the data_source_ml_id?
            self.logger.end(METHOD_NAME, object={
                'data_source_type_id': data_source_type_id,
                'data_source_type_ml_id': data_source_type_ml_id})
            return data_source_type_id, data_source_type_ml_id

        except Exception as exception:
            self.logger.exception(
                log_message="faild to insert data_source " + METHOD_NAME + str(exception), object={"exception": exception})
            self.logger.end(METHOD_NAME, object={
                'data_source_name': data_source_type_name, 'lang_code': lang_code})
            raise exception

    '''
    # Old version
    def get_data_source_type_id_by_name(self, data_source_type_name: str) -> int or None:
        METHOD_NAME = 'get_data_source_type_id_by_name'
        try:
            self.logger.start(log_message=METHOD_NAME, object={
                'data_source_type_name': data_source_type_name})
            data_source_type_id = self.select_one_value_by_id(
                select_clause_value='data_source_type_id',
                id_column_name='name',
                id_column_value=data_source_type_name)
            if data_source_type_id:
                self.logger.end(METHOD_NAME, object={
                    'data_source_type_id': data_source_type_id})
                return data_source_type_id
            else:
                self.logger.end(METHOD_NAME, object={
                    'data_source_type_id': data_source_type_id})
                return None
        except Exception as exception:
            self.logger.exception(
                log_message="faild to get data_source_type_id " + METHOD_NAME + str(exception), object={"exception": exception})
            self.logger.end(METHOD_NAME, object={
                'data_source_type_name': data_source_type_name})
            raise exception

    def get_data_source_type_name_by_id(self, data_source_type_id: int) -> str or None:
        METHOD_NAME = 'get_datasource_type_name_by_id'
        try:
            self.logger.start(log_message=METHOD_NAME, object={
                'data_source_type_id': data_source_type_id})
            data_source_type_name = self.select_one_value_by_id(
                view_table_name='data_source_type_ml_en_view',
                select_clause_value='name',
                id_column_name='data_source_type_id',
                id_column_value=data_source_type_id)
            if data_source_type_name:
                self.logger.end(METHOD_NAME, object={
                    'data_source_type_name': data_source_type_name})
                return data_source_type_name
            else:
                self.logger.end(METHOD_NAME, object={
                    'data_source_type_name': data_source_type_name})
                return None
        except Exception as exception:
            self.logger.exception(
                log_message="faild to get data_source_type_name " + METHOD_NAME + str(exception),
                object={"exception": exception})
            self.logger.end(METHOD_NAME, object={
                'data_source_type_id': data_source_type_id})
            raise exception
    '''

    def get_data_source_type_id_by_name(self, data_source_type_name: str) -> int or None:
        data_source_type_id = self.select_one_value_by_column_and_value(
            select_clause_value='data_source_type_id',
            column_name='name',
            column_value=data_source_type_name)
        return data_source_type_id

    def get_data_source_name_by_id(self, data_source_type_id: int) -> str or None:
        data_source_name = self.select_one_value_by_column_and_value(
            select_clause_value='name',
            column_name='data_source_type_id',
            column_value=data_source_type_id)
        return data_source_name
