import psycopg2, os

class Database:

    def __init__(self):
        self.conn = psycopg2.connect(
            host=os.getenv('POSTGRES_HOST'),
            database=os.getenv('POSTGRES_DB'),
            user=os.getenv('POSTGRES_USER'),
            password=os.getenv('POSTGRES_PWD'),
            port=os.getenv('POSTGRES_PORT')
        )
        self.cur = self.conn.cursor()
        self.table = ''
        self.columns = tuple()
        
    def execute(self, command):
        try:
            self.cur.execute(command)
            response = True
            try:
                response = self.cur.fetchall()
            except Exception as err:
                response = ''
            self.conn.commit()
        except Exception as err:
            response = err
            self.execute('rollback;')
        return response
    

    # Select Queries
    def select_all(self, table=None, where=''):
        if not table:
            table = self.table
        command = f"""SELECT * FROM {table} {where}"""
        return self.execute(command)

    def select_columns(self, columns=None, table=None, where=''):
        if not table:
            table = self.table
        if not columns:
            columns = self.columns
            columns = str(columns).replace('(', '')
            columns = str(columns).replace(')', '')
            columns = str(columns).replace("'", '')
        command = f""" SELECT {columns} FROM {table} {where} """
        return self.execute(command)

    def select_by_id(self, key, table=None):
        if not table:
            table = self.table
        command = f"""SELECT * FROM {table} WHERE ID = {key} """
        return self.execute(command)

    def select_top_row(self, columns, values, table=None, where='', order=''):
        if not table:
            table = self.table
        command = f"""SELECT * FROM {table} WHERE {columns} = {values} {order}"""
        self.cur.execute(command)
        try:
            response = self.cur.fetchone()
        except:
            response = ''
        self.conn.commit()
        return response

    def count_records(self, table=None, where=''):
        if not table:
            table = self.table
        command = f""" SELECT COUNT (*) FROM {table} {where} """
        return self.execute(command)

    # Delete Queries
    def delete_row_by_key(self, key, table=None):
        if not table:
            table = self.table
        command = f"""DELETE FROM {table} WHERE id = {key}"""
        return self.execute(command)

    def clear_table(self, table):
        command = f"""DROP TABLE IF EXISTS {table}"""
        self.execute(command)

    # Insert Queries
    def insert_or_replace(self, values, columns=None):
        if not columns:
            columns = self.columns
        command = f"""
        INSERT INTO {self.table} {columns}
        VALUES {values}
        ON CONFLICT ON CONSTRAINT {self.table}_pkey
            DO NOTHING;
        """
        return self.execute(command)

    def insert_single_record(self, values):
        command = f"""
        INSERT INTO {self.table} {self.columns}
        VALUES ({values})
        ON CONFLICT ON CONSTRAINT {self.table}_pkey
            DO NOTHING
        """

    # Update Queries
    def update_record(self, key, values, columns=None):
        if not columns:
            columns = self.columns
        detail = ', '.join(f"{c} = '{v}'" for c,v in zip(columns, values))
        command = f"""
        UPDATE {self.table} 
        SET {detail}
        WHERE 
        id = {key}
        """
        return self.execute(command)

    # Misc Queries
    def query(self, command):
        self.execute(command)

    def check_table_exists(self):
        command = f"""
        SELECT EXISTS (
            SELECT * FROM information_schema.tables
            WHERE
                table_name = '{self.table}'
        )
        """
        return self.execute(command)