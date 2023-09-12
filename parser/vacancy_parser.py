import json
import time

import requests

from settings import API_URL_HH_2, DATA_PATH


class Vacancy:
    """Собирает с сайта HeadHunter вакансии по номеру айди работодателя"""

    __file_path = str(DATA_PATH) + '/vacancies.json'

    def __init__(self, id_employer):
        self.id_employer = id_employer
        self.get_vacancy = self.get_vacancy()

    def get_vacancy(self):
        """Возвращает вакансии по номеру айди работодателя"""
        try:
            vacancy = []

            while True:

                for page in range(0, 100):
                    params = {
                        "employer_id": f"{self.id_employer}",
                        "page": page,
                        'per_page': 50,
                    }
                    vacancy.extend(requests.get(API_URL_HH_2, params=params).json()['items'])
                    time.sleep(0.22)

                with open(self.__file_path, "w", encoding="utf-8") as f:
                    json.dump(vacancy, f, ensure_ascii=False, indent=4)

                return vacancy
        except requests.exceptions.ConnectTimeout:
            print('Oops. Connection timeout occurred!')
        except requests.exceptions.ReadTimeout:
            print('Oops. Read timeout occurred')
        except requests.exceptions.ConnectionError:
            print('Seems like dns lookup failed..')
        except requests.exceptions.HTTPError as err:
            print('Oops. HTTP Error occurred')
            print('Response is: {content}'.format(content=err.response.content))

    def put_vacancies_in_list(self):
        """Записывает найденные вакансии с нужными ключами в список словарей"""
        list_vacancy = []

        for i in range(len(self.get_vacancy)):
            salary_from = 0 if (self.get_vacancy[i]['salary'] is None or self.get_vacancy[i]['salary']['from'] == 0 or
                                self.get_vacancy[i]['salary']['from'] is None) else self.get_vacancy[i]['salary'][
                'from']
            salary_to = 0 if (self.get_vacancy[i]['salary'] is None or self.get_vacancy[i]['salary']['to'] == 0 or
                              self.get_vacancy[i]['salary']['to'] is None) else self.get_vacancy[i]['salary']['to']
            info = {
                'id_vacancy': self.get_vacancy[i].get('id'),
                'name_vacancy': self.get_vacancy[i].get('name'),
                'id_employer': 0 if self.get_vacancy[i]['employer']['id'] is None else self.get_vacancy[i]['employer'][
                    'id'],
                'name_employer': "Не указано" if self.get_vacancy[i]['employer']['name'] is None else
                self.get_vacancy[i]['employer']['name'],
                'city': "Не указано" if self.get_vacancy[i]['area']['name'] is None else self.get_vacancy[i]['area'][
                    'name'],
                'salary_from': salary_from,
                'salary_to': salary_to,
                'salary_avg': (salary_from if salary_to == 0 else (salary_from + salary_to) / 2) or (
                    salary_to if salary_from == 0 else (salary_to + salary_to) / 2),
                'experience': self.get_vacancy[i]['experience'].get('name'),
                'url': self.get_vacancy[i].get('alternate_url'),
                "requirement": "Не указано" if self.get_vacancy[i]['snippet']['requirement'] else
                self.get_vacancy[i]['snippet']['requirement'],
            }
            list_vacancy.append(info)
        return list_vacancy
