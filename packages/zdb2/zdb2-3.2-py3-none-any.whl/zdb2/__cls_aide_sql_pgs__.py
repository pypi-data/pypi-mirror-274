class __cls_aide_sql_pgs:
    # noinspection PyMissingConstructor
    def __init__(self):
        pass

    @staticmethod
    def Chk(s: str):
        if s[0] != '"' and s[-1] != '"':
            return f'"{s}"'
        elif s[0] == '"' and s[-1] != '"':
            return f'{s}"'
        elif s[0] != '"' and s[-1] == '"':
            return f'"{s}'
        else:
            return s

    @property
    def _system_schemas(self):
        return "'pg_toast','pg_catalog','information_schema'"

    @property
    def _sql_list_activity_count(self):
        return "SELECT " \
               + " count(*) FROM pg_stat_activity"

    def _sql_list_schemas(self, no_system_schemas: bool = True):
        sql = 'SELECT nspname AS schema_name ' + ' FROM pg_catalog.pg_namespace'

        if no_system_schemas is True:
            sql = f" {sql} WHERE nspname NOT IN ({self._system_schemas})"
        else:
            pass

        return sql

    def _sql_list_tables(self, schema_name: str):

        sql = 'SELECT nspname AS ' + self.Chk(schema_name) + ' FROM pg_catalog.pg_namespace;'

        return sql

    def _sql_list_all_tables(self, split_schema_table: bool = False, no_system_schemas: bool = True):
        if split_schema_table is True:
            sql = "SELECT " \
                  + " '\"' || table_schema || '\"' as table_schema ,'\"' || table_name || '\"'  as table_name " \
                  + " FROM information_schema.tables"
        else:
            sql = "SELECT " \
                  + " '\"' || table_schema || '\".\"'  || table_name || '\"'  as table_name " \
                  + " FROM information_schema.tables"

        if no_system_schemas is True:
            sql = f" {sql} WHERE table_schema NOT IN ({self._system_schemas})"
        else:
            pass

        return sql

    @staticmethod
    def _sql_list_table_structure(table_name: str):
        table_name = table_name.replace('"', '')

        if table_name.find("."):
            arr_table_name = table_name.split(".")
            table_schema = arr_table_name[0]
            table_name = arr_table_name[1]
        else:
            table_schema = None
            table_name = table_name

        sql = "SELECT *" \
              + " FROM information_schema.columns " \
              + f" WHERE table_name = '{table_name}'"

        if table_schema is None:
            pass
        else:
            sql = f"{sql} AND table_schema = '{table_schema}'"

        return sql

    @staticmethod
    def _sql_alter_index(table_name: str, column_name: str, restart_index: int, use_max_id: bool = False):

        if use_max_id is True:
            restart_index = "SELECT MAX(" + column_name + ") FROM " + table_name
        else:
            pass

        sql = f'ALTER TABLE ' + table_name + f' ALTER {column_name} RESTART WITH {restart_index}'

        return sql
