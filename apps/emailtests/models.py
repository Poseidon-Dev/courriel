from apps.parser import EmailTable

class EmailTests:

    def fetch(self):
        return EmailTable().filter('recipient', 't').query()