from typing import Any

import psycopg2


class DBCreate:
    """Создает и заполняет базы данных"""

    def __init__(self, database_name: str, params: dict) -> None:
        self.database_name = database_name
        self.params = params

    def create_database(self):
        """Создание базы данных и таблиц для сохранения данных о работодателях и вакансиях."""
        conn = psycopg2.connect(dbname='postgres', **self.params)
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute(f"DROP DATABASE IF EXISTS {self.database_name}")
        cur.execute(f"CREATE DATABASE {self.database_name}")

        cur.close()
        conn.close()

        conn = psycopg2.connect(dbname=self.database_name, **self.params)

        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE employers (
                    id_employer INT PRIMARY KEY,
                    name_employer VARCHAR(255) NOT NULL,
                    open_vacancies VARCHAR,
                    url_employer TEXT
                )
            """)

        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE vacancies (
                    id_vacancy INT PRIMARY KEY,
                    name_vacancy VARCHAR(255) NOT NULL,
                    id_employer INT REFERENCES employers(id_employer),
                    name_employer VARCHAR NOT NULL,
                    salary_from INT,
                    salary_to INT,
                    salary_avg INT,
                    city VARCHAR(255),
                    experience TEXT,
                    requirement TEXT,
                    url TEXT
                )
            """)

        conn.commit()
        conn.close()

    def save_employers_to_database(self, data: list[dict[str, Any]]):
        """Сохранение данных о работодателях в базу данных."""

        conn = psycopg2.connect(dbname=self.database_name, **self.params)

        with conn.cursor() as cur:
            for employer in data:
                cur.execute(
                    """
                    INSERT INTO employers (id_employer, name_employer, open_vacancies, url_employer)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (id_employer) DO NOTHING
                    RETURNING id_employer
                    """,
                    (employer['id'], employer['name'], employer['open_vacancies'], employer['alternate_url']))
        conn.commit()
        conn.close()

    def save_vacancies_to_database(self, data: list[dict[str, Any]]):
        """Сохранение данных о вакансиях в базу данных."""
        conn = psycopg2.connect(dbname=self.database_name, **self.params)
        with conn.cursor() as cur:
            for vacancy in data:
                cur.execute(
                    """
                    INSERT INTO vacancies (id_vacancy, name_vacancy, id_employer, name_employer, city, salary_from, 
                    salary_to, salary_avg, experience, requirement, url)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (vacancy['id_vacancy'], vacancy['name_vacancy'], vacancy['id_employer'], vacancy['name_employer'],
                     vacancy['city'], vacancy['salary_from'], vacancy['salary_to'], vacancy['salary_avg'],
                     vacancy['experience'],
                     vacancy['requirement'], vacancy['url']))

        conn.commit()
        conn.close()
