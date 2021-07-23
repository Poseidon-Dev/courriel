from imap_tools import MailBox, A, O, N, H, U

from apps.parser import EmailTable

from core.config import EMAIL_IMAP, EMAIL_UID, EMAIL_PWD
from core.shared.utils import binary_pickle

class EmailLogger:

    def __init__(self, sender: str=None, subject: str=None):
        self.sender = sender
        self.subject = subject

    def pull_email(self):
        with MailBox(EMAIL_IMAP).login(EMAIL_UID, EMAIL_PWD) as mailbox:
            if self.sender:
                email_pull = mailbox.fetch(A(sender=self.sender,seen=False), mark_seen=True)
            elif self.subject:
                email_pull = mailbox.fetch(A(subject=self.subject,seen=False), mark_seen=True)
            else:
                email_pull = mailbox.fetch(seen=False, mark_seen=True)

            for e in email_pull:
                e_pickle = binary_pickle(e)
                EmailTable().insert(
                    ['id', 'email', 'subject', 'sender'],
                    [e.uid, e_pickle, e.subject, e.from_]
                )



    def log_email(self):
        email = self.pull_email()
        
    


