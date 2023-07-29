import time
import psycopg2

from bs4 import BeautifulSoup
from selenium import webdriver

driver = webdriver.Edge()
url = 'https://www.avito.ru/moskva/kvartiry/sdam/na_dlitelnyy_srok-ASgBAgICAkSSA8gQ8AeQUg'
driver.get(url)
driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
time.sleep(5)
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
prices = soup.find_all('strong', class_='styles-module-root-LIAav')
apartments = soup.find_all('h3', class_='styles-module-root-TWVKW styles-module-root-_KFFt styles-module-size_l-_oGDF styles-module-size_l-hruVE styles-module-ellipsis-LKWy3 styles-module-weight_bold-Kpd5F stylesMarningNormal-module-root-OSCNq stylesMarningNormal-module-header-l-qvNIS')

conn = psycopg2.connect(dbname='parsing', user='postgres', password='postgres', host='127.0.0.1', port='5432')
conn.autocommit = True

with conn:
    with conn.cursor() as cursor:
        print('Подключение установлено')
        apartment_list = []
        price_list = []
        for apartment, price in zip(apartments, prices):
            m = apartment.get_text()
            p = price.get_text()
            apartment_list.append(m)
            price_list.append(p)
        data = zip(apartment_list, price_list)
        data_list = list(data)

        cursor.executemany("INSERT INTO flats (title, price) VALUES (%s, %s)", data_list)
        print('Данные добавлены')

print(cursor.closed)
conn.close()