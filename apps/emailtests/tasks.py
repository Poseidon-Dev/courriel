from apps.parser import EmailTable, EmailLogger

class EmailTests(EmailLogger):

    def __init__(self, folder: str='INBOX'):
        super().__init__(folder)

    def fetch(self):
        return EmailTable().filter('recipient', 't').query()