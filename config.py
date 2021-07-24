import os, psycopg2

STARTUP_APPS = [

]

PG_HOST = os.getenv('POSTGRES_HOST')
PG_DB = os.getenv('POSTGRES_DB'),
PG_USR = os.getenv('POSTGRES_USER'),
PG_PWD = os.getenv('POSTGRES_PWD'),
PG_PORT = os.getenv('POSTGRES_PORT')

EMAIL_UID = os.getenv('EMAIL_UID')
EMAIL_PWD = os.getenv('EMAIL_PWD')
EMAIL_SMTP = os.getenv('EMAIL_SMTP')
EMAIL_SMTP_PORT = int(os.getenv('EMAIL_SMTP_PORT'))
EMAIL_IMAP = os.getenv('EMAIL_IMAP')
EMAIL_IMAP_PORT = int(os.getenv('EMAIL_IMAP_PORT'))

ACCEPTED_DOMAIN = ['arizonapipeline.com']