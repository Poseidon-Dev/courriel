from pickle import loads
from apps import emailtests
from apps.emailtests import EmailTests

email_tests = EmailTests().fetch()
for e in email_tests:
    print(e)