from apps.parser import EmailLogger
from apps.parser import EmailTable, EmailLogger


if __name__ == "__main__":
    print('='*20 + ' Courriel Running... ' + '=' *20)
    EmailTable().build()
    EmailLogger().run()

