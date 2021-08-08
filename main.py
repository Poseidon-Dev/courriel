from typing import final
from apps.parser import EmailLogger
from apps.parser import EmailTable, EmailLogger

import os, sys

if __name__ == "__main__":
    pid = str(os.getpid())
    pidfile = "couriel.pid"
    if os.path.isfile(pidfile):
        sys.exit()
    open(pidfile, 'w').write(pid)
    try:
        print('='*20 + ' Courriel Running... ' + '=' *20)
        EmailTable().build()
        EmailLogger().run()
    finally:
        os.unlink(pidfile)
