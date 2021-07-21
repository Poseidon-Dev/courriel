from imap_tools import MailBox, A, O, N, H, U
import json
import pickle
import psycopg2

from core.config import EMAIL_IMAP, EMAIL_UID, EMAIL_PWD
from apps.parser import EmailTable

from core.shared.utils import Timer

email_conn_t = Timer('Email Connection')
email_conn_t.start()

with MailBox(EMAIL_IMAP).login(EMAIL_UID, EMAIL_PWD) as mailbox:
    test_output = mailbox.fetch(A(subject='test'))
    for email in test_output:
        pickle_email = psycopg2.Binary(pickle.dumps(email))
        EmailTable().insert(['id', 'email'], [email.uid, pickle_email])

email_objs = EmailTable().all().query()
for email in email_objs:
    email = pickle.loads(email[1])
    print('=' * 12 + 'new email' + '=' * 12)
    print(email.uid)
    print(email.subject)
    print(email.date)
    print(email.flags)
    print(json.dumps(email.from_values))
    print(email.to_values)
    print(email.text)



