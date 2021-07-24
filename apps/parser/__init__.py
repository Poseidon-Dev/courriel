from apps.parser.models import EmailTable
from apps.parser.parser import EmailLogger
from apps.parser.utils import binary_pickle, check_domain

EmailTable().build()