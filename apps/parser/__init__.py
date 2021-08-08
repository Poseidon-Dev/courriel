from psycopg2.extensions import TRANSACTION_STATUS_IDLE
from apps.parser.models import EmailTable
from apps.parser.parser import EmailLogger
from apps.parser.utils import binary_pickle, check_domain, loop


