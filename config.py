import requests
from enum import Enum
qiwiop = '18d97b25e22a7cc07876d7fdbe1aeb22'
db_file = "database.vdb"

class States(Enum):

    S_START = "0"
    S_ENTER_SUM = "1"
    S_ENTER_SUM1 = "2"
    S_ENTER_CARD2 = "3"
    S_ENTER_CARD3 = "4"
    S_ENTER_MENU = "5"
    S_ENTER_4DIGIT = "6"

token = '1847082698:AAEj5zUxRXbAhARX2-tib_fQwdd203nUawQ'
#token = '860458112:AAE9jtvs6PGV8M4wQaDMmk9JKCddwUt524A'



