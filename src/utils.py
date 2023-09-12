from config import config
from db.db_creator import DBCreate
from parser.hh_parser import HhParser
from parser.vacancy_parser import Vacancy


def user_interaction(db: DBCreate):
    i = 1
    list_emp = []

    while i <= 10:
        customers_word = input("Напишите название работодателя, чьи вакансии мы будем искать: ")

        list_emp.append(customers_word)

        hh = HhParser(customers_word)
        data = hh.get_request

        for number in range(len(data)):
            id_emp = data[number]["id"]
            vac = Vacancy(id_emp)
            vacancy_list = vac.put_vacancies_in_list()

            db.save_employers_to_database(data)
            db.save_vacancies_to_database(vacancy_list)

        i += 1
