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

            for page in range(0, 10):
                params = {
                    "employer_id": f"{self.id_employer}",
                    "page": page,
                    'per_page': 20,
                }
                data = requests.get(API_URL_HH_2, params=params).json()
                vacancy.extend(data.get('items'))
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

        vacancies = self.get_vacancy

        for i in range(len(vacancies)):
            salary_from = 0 if (vacancies[i]['salary'] is None or vacancies[i]['salary']['from'] == 0 or
                                vacancies[i]['salary']['from'] is None) else vacancies[i]['salary'][
                'from']
            salary_to = 0 if (vacancies[i]['salary'] is None or vacancies[i]['salary']['to'] == 0 or
                              vacancies[i]['salary']['to'] is None) else vacancies[i]['salary']['to']
            info = {
                'id_vacancy': vacancies[i].get('id'),
                'name_vacancy': vacancies[i].get('name'),
                'id_employer': 0 if vacancies[i]['employer']['id'] is None else vacancies[i]['employer'][
                    'id'],
                'name_employer': "Не указано" if vacancies[i]['employer']['name'] is None else
                self.get_vacancy[i]['employer']['name'],
                'city': "Не указано" if vacancies[i]['area']['name'] is None else vacancies[i]['area'][
                    'name'],
                'salary_from': salary_from,
                'salary_to': salary_to,
                'salary_avg': (salary_from if salary_to == 0 else (salary_from + salary_to) / 2) or (
                    salary_to if salary_from == 0 else (salary_to + salary_to) / 2),
                'experience': vacancies[i]['experience'].get('name'),
                'url': vacancies[i].get('alternate_url'),
                "requirement": "Не указано" if vacancies[i]['snippet']['requirement'] else
                vacancies[i]['snippet']['requirement'],
            }

            list_vacancy.append(info)
        return list_vacancy
