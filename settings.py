from pathlib import Path

API_URL_HH_1 = 'https://api.hh.ru/employers'
API_URL_HH_2 = 'https://api.hh.ru/vacancies'

USE_LOCAL_DATA = True
ROOT_PATH = Path().resolve().parent
DATA_PATH = Path.joinpath(ROOT_PATH, 'data')
DATABASE_INI_PATH = ROOT_PATH.joinpath('database.ini')
