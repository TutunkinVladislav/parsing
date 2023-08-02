import time

from bs4 import BeautifulSoup
from selenium import webdriver
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import DeclarativeBase, Session

driver = webdriver.Edge()
url = 'https://www.avito.ru/moskva/kvartiry/sdam/na_dlitelnyy_srok-ASgBAgICAkSSA8gQ8AeQUg'
driver.get(url)
driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
time.sleep(5)
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
prices = soup.find_all('strong', class_='styles-module-root-LIAav')
apartments = soup.find_all('h3',
                           class_='styles-module-root-TWVKW styles-module-root-_KFFt styles-module-size_l-_oGDF styles-module-size_l-hruVE styles-module-ellipsis-LKWy3 styles-module-weight_bold-Kpd5F stylesMarningNormal-module-root-OSCNq stylesMarningNormal-module-header-l-qvNIS')

engine = create_engine('sqlite:///apartments.db')


class Base(DeclarativeBase):
    pass


class Flat(Base):
    __tablename__ = 'flats'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    price = Column(String)


Base.metadata.create_all(bind=engine)

with Session(autoflush=False, bind=engine) as db:
    for apartment, price in zip(apartments, prices):
        m = apartment.get_text()
        p = price.get_text()
        flat = Flat(title=m, price=p)
        db.add(flat)

    db.commit()
    print('Данные добавлены')
