import re
import apps.base.exceptions as BaseErr
from apps.base.conn import DBConnection, TableBuilder
from psycopg2 import sql

class ExecuteMixin:
    """
    Establish connection with psqldb and create a standard execute/commit method
    """
    def __init__(self):
        self.conn = None
        self.cur = None
        
    def execute(self, command, values=None):
        """
        Simple cursor execution
        """
        self.conn = DBConnection().conn()
        self.cur = self.conn.cursor()
        try:
            response = ''
            if values:
                self.cur.execute(command, values)
            else:
                self.cur.execute(command)
            try:
                response = self.cur.fetchall()
            except Exception as err:
                pass
            self.conn.commit()
        except (
            BaseErr.UndefinedTable,
            BaseErr.UndefinedColumn,
            BaseErr.UndefinedFunction,
            BaseErr.PsqlSyntaxError,
            BaseErr.NonUniqueError
            ) as err:
            self.conn.rollback()
            response = ''
            print(err)
            return err
        except Exception as e:
            print(f'uncaught exeception: {e}')
        finally:
            self.conn.close()
            self.cur.close()
            return response

class QueryBase(ExecuteMixin):

    def __init__(self, table=''):
        super().__init__()
        self.table = table
        self.base_command = ''
        self.command = ''

    def filter(self, col: str = 'id', val: str = '', op: str = "="):
        """
        Adds a where/and clause to the SQL command
        Defaults to ID column with = operator
        """
        if val:
            command = ''
            if 'WHERE' in self.command:
                command += f" AND {col} {op} '{val}'"
            else:
                command += f" WHERE {col} {op} '{val}'"
            self.statement_helper(command)
        return self

    def filter_like(self, col: str='id', val: str='', op: str="like", like=''):
        """
        Filters like values, defaults to id column
            : Default operator is %val%
            : 'End' searches for %val
            : Else val%
        """
        if val:
            if not like:
                val = f'{val}%'
            elif like == 'end':
                val = f'%{val}'
            else:
                val = f'%{val}%'
            self.filter(col, val, op)
        return self

    def columns(self, columns="*"):
        """
        Replaces the default * columns with user selected columns
        Takes in either a list or string
        """
        if type(columns) is list:
            columns = ', '.join(columns)
        if "*" in self.command:
            self.command = self.command.replace('*', f'{columns}')
        else:
            self.command = self.base_command.replace('*', f'{columns}')
        return self

    def order(self, by: str = 'id', order: str = ''):
        """
        Adds an 'ORDER' clause to the base statement
        Defaults to column ID in ascending order
        """
        command = f' ORDER BY {by} {order} '
        self.statement_helper(command)
        return self

    def join(self, table='', current_tbl_field='', join_tbl_field='id'):
        """
        Adds a full outer join clause to the base statement
        defaults to joining on foreign.id field
        """
        command = f'JOIN {table} ON {table}.{join_tbl_field} = {self.table}.{current_tbl_field}'
        if self.command:
            self.command.replace(f'{self.table}', f'{self.table} {command}')
        else:
            self.command = self.base_command.replace(f'{self.table}', f'{self.table} {command}')
        return self

    def limit(self, amount=1):
        """
        Adds a 'LIMIT' clause to the base statement
        defaults to 1
        """
        command = f' LIMIT {amount};'
        if self.command:
            self.command += command
        else:
            self.command = self.base_command + command
        return self

    def all(self):
        """
        Writes over current command with a select all clause
        """
        self.command = f'SELECT * FROM {self.table}'
        return self
        
    def query(self, command=''):
        """
        If a command arugment is entered, accepts that and runs the query adding a ; to the end
        Otherwise takes the generated base statement and executes, adding a ; to the end
        """
        if not command:
            return self.execute(self.command + ';')
        else:
            return self.execute(command + ';')

    def statement_helper(self, command):
        """
        Adds the base command to the running command
        """
        if not self.command:
            self.command += self.base_command
        self.command += command

class QueryMixin(QueryBase):

    def __init__(self, table=''):
        self.table = table
        super().__init__(self.table)
        self.base_command = f'SELECT * FROM {self.table}'
        self.command = ''

    def select_last(self): 
        """
        Returns the last item in a table as a QueryBase object based on ID
        """
        return self.order(order='DESC').limit()

    def select_first(self): 
        """
        Returns the first item in a table as a QueryBase object based on ID
        """
        return self.order().limit()

    def insert(self, columns: list, values: list):
        """
        Accepts list of column names and list of values 
        and inserts into self.table
        """
        try:
            col_names = sql.SQL(', ').join(sql.Identifier(c) for c in columns)
            vals_placeholder = sql.SQL(', ').join(sql.Placeholder() * len(columns))
            command = sql.SQL(
                """
                INSERT INTO {table_name} ({cols}) VALUES ({values})
                ON CONFLICT ON CONSTRAINT {table_contraint} DO NOTHING
                """).format(
                    table_name=sql.Identifier(self.table),
                    cols=col_names,
                    values=vals_placeholder,
                    table_contraint=sql.Identifier(self.table + '_pkey'))
            self.execute(command, values)
            return True
        except Exception as e:
            print(e)
            return False

    def manual(self, command):
        """
        A manualy query execution
        """
        return self.execute(command)

    def column_names(self):
        """
        Returns the column names of self.table
        """
        command = f"""
        SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS 
        WHERE TABLE_NAME = '{self.table}'
        ORDER BY ordinal_position;
        """
        return self.execute(command)

    def column_names_to_string(self):
        """
        Returns the column names of self.columns_names into a string
        """
        results = ' '.join([f'{idx},' for tup in self.column_names() for idx in tup])
        return results[:-1]

    def delete_table(self):
        command = f"""
        DELETE FROM {self.table}
        """
        self.execute(command)
        

class Query(QueryMixin):

    def __init__(self, table, cols=None):
        self.table = table
        self.columns = cols
        super().__init__(self.table)

    def build(self):
        TableBuilder(self.table, self.columns).build()