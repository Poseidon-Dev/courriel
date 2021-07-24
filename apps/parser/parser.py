import asyncio
from imap_tools import MailBox, A, O, N, H, U

from apps.parser import EmailTable
from apps.parser.utils import binary_pickle, check_domain, loop

from config import EMAIL_IMAP, EMAIL_UID, EMAIL_PWD

class EmailMixin:

    def __init__(self, folder: str='INBOX'):
        self.folder = folder
        self.mailbox = MailBox(EMAIL_IMAP).login(EMAIL_UID, EMAIL_PWD, initial_folder=self.folder)
        self.email = ''

    def _test_connection(self):
        return self.mailbox.login_result

    def log_email(self, email_objs):
        for e in email_objs:
            sender = check_domain(e.from_)
            recipient = check_domain(e.to[0])
            if sender and recipient:
                pickle_email = binary_pickle(e)
                EmailTable().insert(
                    ['id', 'email', 'subject', 'sender', 'recipient', 'local_read'],
                    [e.uid, pickle_email, e.subject.lower(), sender, recipient, 0]
                )
    
    def delete_email(self, sender:str=None, subject:str=None):
        self.mailbox.delete([msg.uid for msg in self.pull_email(sender, subject)])
        return True

class EmailLogger(EmailMixin):

    def __init__(self, folder: str='INBOX'):
        super().__init__(folder)

    @loop
    async def run(self):
        """
        Fetches all unread email from mailbox and store in local DB
        """
        while True:
            self.email = self.mailbox.fetch(A(seen=False), mark_seen=True)
            self.log_email(self.email)
            await asyncio.sleep(1)

