from imap_tools import MailBox, A, O, N, H, U

from core.config import EMAIL_IMAP, EMAIL_UID, EMAIL_PWD
from apps.parser import EmailTable, EmailLogger

from pickle import loads

from core.shared.utils import Timer, binary_pickle

# email_test = EmailLogger(subject='Test').pull_email()

draw_email = EmailTable().all().query()
for email in draw_email:
    email_class = loads(email[1])
    print(f'{email[0]}: {email_class.text} {email[2]}')

# def populate_email():
#     with MailBox(EMAIL_IMAP).login(EMAIL_UID, EMAIL_PWD) as mailbox:
#         test_output = mailbox.fetch(A(subject='test'))
#         for email in test_output:
#             pickle_email = binary_pickle(email)
#             EmailTable().insert(
#                 ['id', 'email', 'subject', 'sender'],
#                 [email.uid, pickle_email, email.subject, email.from_]
#                 )

# for i in range(1000):
#     populate_email()
#     print(i)
# for i in range(15):
#     r_timer = Timer('Pull from Table')
#     r_timer.start()
#     email_table = EmailTable().all().query()
#     for e in email_table:
#         email = loads(e[1])
#         if email.subject.lower() == 'test':
#             True
#     r_timer.stop()

#     r_timer = Timer('Sort Before Parse')
#     r_timer.start()
#     email_table = EmailTable().filter('subject', 'Test').query()
#     for e in email_table:
#         True
#     r_timer.stop()
