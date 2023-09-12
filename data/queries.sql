-- SQL queries for PGadmin

-- Получает список всех компаний и количество вакансий у каждой компании.
SELECT name_employer, open_vacancies FROM employers

-- Получает список всех вакансий с указанием названия компании, названия вакансии
-- и зарплаты, и ссылки, на вакансию.
SELECT name_employer, name_vacancy, salary_from, salary_to, url FROM vacancies

-- Получает среднюю зарплату по вакансиям.
SELECT ROUND(AVG(salary_avg)) as avg_salary FROM vacancies

-- Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
SELECT name_employer, name_vacancy, salary_avg, url FROM vacancies"
WHERE salary_avg > (SELECT AVG(salary_avg) FROM vacancies)

-- Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например “python”.
SELECT * FROM vacancies"
WHERE name_vacancy LIKE '%{word}%'