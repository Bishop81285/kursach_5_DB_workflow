import psycopg2

from db.db_creator import DBCreate


class DBManager(DBCreate):
    """Работает с базами данных"""

    def get_companies_and_vacancies_count(self):
        """Получает список всех компаний и количество вакансий у каждой компании."""
        conn = psycopg2.connect(dbname=self.database_name, **self.params)
        list_companies_and_vacancies_count = []
        with conn.cursor() as cur:
            cur.execute("SELECT name_employer, open_vacancies FROM employers")
            rows = cur.fetchall()
            for row in rows:
                list_companies_and_vacancies_count.append(row)
            return list_companies_and_vacancies_count

    def get_all_vacancies(self):
        """Получает список всех вакансий с указанием названия компании, названия вакансии
        и зарплаты, и ссылки, на вакансию."""
        conn = psycopg2.connect(dbname=self.database_name, **self.params)
        list_all_vacancies = []
        with conn.cursor() as cur:
            cur.execute("SELECT name_employer, name_vacancy, salary_from, salary_to, url FROM vacancies")
            rows = cur.fetchall()
            for row in rows:
                list_all_vacancies.append(row)
            return list_all_vacancies

    def get_avg_salary(self):
        """ Получает среднюю зарплату по вакансиям."""
        conn = psycopg2.connect(dbname=self.database_name, **self.params)
        with conn.cursor() as cur:
            cur.execute("SELECT ROUND(AVG(salary_avg)) as avg_salary FROM vacancies")
            return cur.fetchall()

    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        conn = psycopg2.connect(dbname=self.database_name, **self.params)
        list_with_higher_salary_vacancies = []
        with conn.cursor() as cur:
            cur.execute(
                "SELECT name_employer, name_vacancy, salary_avg, url FROM vacancies"
                " WHERE salary_avg > (SELECT AVG(salary_avg) FROM vacancies)"
            )
            rows = cur.fetchall()
            for row in rows:
                list_with_higher_salary_vacancies.append(row)
            return list_with_higher_salary_vacancies

    def get_vacancies_with_keyword(self, word: str):
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например “python”."""
        conn = psycopg2.connect(dbname=self.database_name, **self.params)
        list_with_keyword_vacancies = []
        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM vacancies"
                f" WHERE name_vacancy LIKE '%{word}%'"
            )
            rows = cur.fetchall()
            for row in rows:
                list_with_keyword_vacancies.append(row)
            return list_with_keyword_vacancies
