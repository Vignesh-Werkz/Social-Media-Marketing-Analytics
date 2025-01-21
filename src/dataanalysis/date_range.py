from enum import Enum
from datetime import datetime, timedelta

class DateRange(Enum):
    SIX_MONTHS = 180
    ONE_MONTH = 30
    NEW_MONTH = 30
    TWELVE_MONTHS = 365
    ONE_DAY = 0
