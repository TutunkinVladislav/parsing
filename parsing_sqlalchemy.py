from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import DeclarativeBase


engine = create_engine('sqlite:///apartments.db')

class Base(DeclarativeBase):
    pass


class Person(Base):
    __tablename__ = 'people'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    age = Column(Integer)

Base.metadata.create_all(bind=engine)

print("База данных и таблица созданы")
