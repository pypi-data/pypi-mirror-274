# https://pypi.org/project/ibm-db/
# pip install ibm-db

from ibm_db_dbi import *
from .__cls_aide_rst_base__ import __cls_aide_rst_base
from .__cls_aide_sql_pgs__ import __cls_aide_sql_pgs


class __cls_conn(__cls_aide_rst_base, __cls_aide_sql_pgs):
    # noinspection PyMissingConstructor

    @property
    def connection(self):
        return self.__connState

    def set_connection(self, connState=False):
        self.__connState = connState

    # noinspection PyMissingConstructor
    def __init__(self, database=None, host=None, port=None, user=None, password=None):
        self.rst = self._cls_aide_rst_base("cls_db2_conn")

        if database is None:
            pass
        else:
            self.conn = None
            self.database = database
            self.host = host
            self.port = port
            self.user = user
            self.password = password
            self.__connState = False
            self.connect()

            self.rst.set_process("DB2")

    def connect(self):
       self.rst.process_start("connect")

        try:
            self.set_connection(False)
            self.conn = ibm_db.connect(
                'DATABASE=' + self.database
                + ';HOSTNAME=' + self.host
                + ';PORT=' + self.port
                + ';PROTOCOL=TCPIP;UID=' + self.user
                + ';PWD=' + self.password,
                '', '')
            self.set_connection(True)
            self.rst.set(self.connection, self.rst.now() + ',' + 'Connected!' + ',Cost:' + self.rst.process_cost, self.host)
        except Exception as e:
            if e:
                self.rst.set(False, self.rst.now() + ',Exception:' + 'Connection failed!' + ',Cost:' + self.rst.process_cost,
                             'Exception:' + e.__str__())
            else:
                self.rst.set(False, self.rst.now() + ',DB ERROR:' + 'Connection failed!' + ',Cost:' + self.rst.process_cost,
                             'DB error_log:' + ibm_db.conn_errormsg())

    def disconnect(self):
        self.rst.process_start("disconnect")
        if self.connection is True:
            if ibm_db.active(self.conn):
                ibm_db.close(self.conn)
                self.set_connection(False)

    def select(self, sql):
        self.rst.process_start("select")

        # self.DEBUG_PRINT("SQL", sql)

        start_time = self.now0.now

        # print("##### DB2 select!")

        if self.connection is True:
            pass
        else:
            # print("##### DB connection reconnect!")
            self.connect()
            if self.rst.state is False:
                return None

        if sql[0:6] == 'SELECT':
            try:
                __stmt = ibm_db.exec_immediate(self.conn, sql)
                __rst = ibm_db.fetch_assoc(__stmt)
                __row_index = 0
                __rst0 = {}
                while (__rst):
                    __rst0[__row_index] = __rst
                    __rst = ibm_db.fetch_assoc(__stmt)
                    __row_index = __row_index + 1
                self.rst.set(True, self.now0.date_timestamp + ',' + 'Selected ' + str(
                    len(__rst0)) + ' row(s)' + ',Cost:' + self.rst.process_cost, __rst0)
                return __rst0
            except Exception as e:
                if e:
                    self.rst.set(False, self.now0.date_timestamp
                                 + ',Exception:' + e.__str__().replace("'", "") + ',Cost:' + self.rst.process_cost,
                                 sql)
                else:
                    self.rst.set(False,
                                 self.now0.date_timestamp + ',DB ERROR:' + ibm_db.stmt_errormsg() + ',Cost:' + self.rst.process_cost,
                                 sql)
        else:
            cost = self.diff(start_time, self.now0.now)
            self.rst.set(False, self.now0.date_timestamp + ',' + 'Only Select SQL can be execute!' + ',Cost:' + self.rst.process_cost,
                         sql)

        if self.rst.state is True:
            return self.rst.data
        else:
            return None

    def exec_sql(self, sql, sql_type):
        self.rst.process_start("exec_sql")

        # self.DEBUG_PRINT("SQL", sql)

        if self.connection is True:
            pass
        else:
            print("##### DB connection reconnect!")
            self.connect()
            if self.rst.state is False:
                return None

        self.rst.set(False, None, None)
        try:
            stmt = ibm_db.exec_immediate(self.conn, sql)
            rows = ibm_db.num_rows(stmt)
            self.rst.set(True, self.now0.date_timestamp + ',' + sql_type + ' Successful' + ',Cost:' + self.rst.process_cost, rows)
        except Exception as e:
            if e:
                self.rst.set(False,
                             self.now0.date_timestamp + ',Exception:' + e.__str__().replace("'", "") + ',Cost:' + self.rst.process_cost,
                             sql)
            else:
                self.rst.set(False, self.now0.date_timestamp + ',DB ERROR:' + ibm_db.stmt_errormsg() + ',Cost:' + self.rst.process_cost,
                             sql)
        return self.rst.state

    def insert(self, sql):
        self.rst.process_start("insert")

        if sql[0:6] == 'INSERT':
            self.exec_sql(sql, "INSERT")
        else:
            self.rst.set(False, self.now0.date_timestamp + ',' + 'Only Insert SQL can be execute!', sql)

    def update(self, sql):
        self.rst.process_start("update")
        if sql[0:6] == 'UPDATE':
            self.exec_sql(sql, 'UPDATE')
        else:
            self.rst.set(False, self.now0.date_timestamp + ',' + 'Only Update SQL can be execute!', sql)

    def data_clear(self, sql):
        self.rst.process_start("data_clear")
        if sql[0:6] == 'DELETE':
            self.exec_sql(sql, 'DELETE')
        else:
            self.rst.set(False, self.now0.date_timestamp + ',' + 'Only Delete SQL can be execute!', sql)

    @property
    def is_error_unique(self):
        str_err = "SQLCODE=-803"
        if self.rst.msg.find(str_err) < 0:
            return False
        else:
            return True
