from psycopg2 import errors

FailedSqlTransaction = errors.lookup('25P02')
UndefinedTable = errors.lookup('42P01')
UndefinedColumn = errors.lookup('42703')
NoDataFound = errors.lookup('P0002')
UndefinedFunction = errors.lookup('42883')
PsqlSyntaxError = errors.lookup('42601')
NonUniqueError  = errors.lookup('23505')