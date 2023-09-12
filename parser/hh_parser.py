import json

import requests

from settings import API_URL_HH_1, DATA_PATH


class HhParser:
    """Возвращает работодателей с сайта HeadHunter по ключевому слову"""

    __file_path = str(DATA_PATH) + '/employers.json'

    def __init__(self, data: str):
        """Инициализирует класс где data - название по которому будет происходить поиск"""
        self.data = data

    @property
    def get_request(self):
        """Возвращает работодателей с сайта HeadHunter"""
        try:
            employers = []

            params = {
                "text": f"{self.data}",
                "area": 1,
                "only_with_vacancies": True,
                "pages": 1,
                "per_page": 20,
            }
            employers.extend(requests.get(API_URL_HH_1, params=params).json()["items"])

            with open(self.__file_path, "w", encoding="utf-8") as f:
                json.dump(employers, f, ensure_ascii=False, indent=4)

            return employers

        except requests.exceptions.ConnectTimeout:
            print('Oops. Connection timeout occurred!')

        except requests.exceptions.ReadTimeout:
            print('Oops. Read timeout occurred')
        except requests.exceptions.ConnectionError:
            print('Seems like dns lookup failed..')
        except requests.exceptions.HTTPError as err:
            print('Oops. HTTP Error occurred')
            print('Response is: {content}'.format(content=err.response.content))
