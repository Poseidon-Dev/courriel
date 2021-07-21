from apps.base import Query

class EmailTable(Query):
    """
    DB table storing all relevant email information 
    """
    def __init__(self):
        self.table = 'email_table'
        self.columns = [
            ('id', 'INT PRIMARY KEY'),
            ('email', 'BYTEA'),           
        ]
        Query.__init__(self, self.table, self.columns)