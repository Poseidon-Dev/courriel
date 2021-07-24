import psycopg2
import config

import apps.base.exceptions as BaseErr

class DBConnection:

    def __init__(self):
        self.host = config.PG_HOST
        self.db_name = config.PG_DB[0]
        self.user = config.PG_USR[0]
        self.pwd = config.PG_PWD[0]
        self.port = config.PG_PORT


    def conn(self):
        """
        Creates a connection object to the localDB
        """
        conn = psycopg2.connect(
            host=self.host,
            database=self.db_name,
            user=self.user,
            password=self.pwd,
            port=self.port
        )
        return conn

    def close(self):
        """
        Closes postgres connections
        """
        self.conn.close()

class ExecuteMixin:

    def __init__(self):
        self.conn = None
        self.cur = None
        

    def execute(self, command):
        """
        Simple cursor execution
        """
        self.conn = DBConnection().conn()
        self.cur = self.conn.cursor()
        try:
            response = ''
            self.cur.execute(command)
            try:
                response = self.cur.fetchall()
            except Exception as err:
                pass
            self.conn.commit()
            self.conn.close()
        except (
            BaseErr.UndefinedTable,
            BaseErr.UndefinedColumn,
            BaseErr.UndefinedFunction,
            BaseErr.PsqlSyntaxError
            ) as err:
            self.conn.rollback()
            self.conn.close()
            response = ''
            return err
        except Exception as e:
            print(f'uncaught exeception: {e}')
        finally:
            return response

class TableBuilder(ExecuteMixin):

    def __init__(self, table, columns):
        super().__init__()
        self.table = table
        self.columns = columns

    def build(self):
        columns = ',\n'.join(map(
            lambda x: str(x[0]) + ' ' + str(x[1]),
            self.columns))
        command = f"""
        CREATE TABLE IF NOT EXISTS {self.table}(
            {columns}
        );
        """
        self.execute(command)
