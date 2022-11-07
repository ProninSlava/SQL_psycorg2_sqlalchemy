import sys
from  pprint import pprint
import requests

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, PrimaryKeyConstraint, Table, func

from sqlalchemy.exc import IntegrityError, InvalidRequestError

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import sessionmaker, relationship


# Класс Base
Base = declarative_base()

DSN = 'postgresql+psycopg2://slava:7548@localhost:5432/hero'

# Создание движка
engine = create_engine(DSN)

# Для получения соединения нужно использовать метод connect() объекта Engine, который возвращает объект типа Connection
connection = engine.connect()

Session = sessionmaker(bind=engine)
session = Session()

#1
class Heroes(Base):
    __tablename__ = 'heroes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    power = Column(Integer)
    speed = Column(Integer)
    strength = Column(Integer)
    image = Column(String)

# Base.metadata.create_all(engine)


dict_heroes = {}

for id in range(1,6):
    response = requests.get('https://akabab.github.io/superhero-api/api/id/' + str(id) + '.json').json()
    if id not in dict_heroes:
        dict_heroes[id] =  {
            'name': response['name'],
            'power': response['powerstats']['power'],
            'speed': response['powerstats']['speed'],
            'strength': response['powerstats']['strength'],
            'image': response['images']['lg'],
            }
# pprint(dict_heroes)



# all_hero = session.query(Heroes).all()
# list_heroes = [heroes.name for heroes in all_hero]

# for hero in dict_heroes.values():
#     if hero['name'] not in list_heroes:
#
#         new_hero = Heroes(name=hero['name'], power=hero['power'], speed=hero['speed'], strength=hero['strength'], image=hero['image'])
#
#         session.add(new_hero)
#         session.commit()
#         print(f'''Добавлен новый герой: {hero['name']}''')
#     else:
#         print(f'''Герой "{hero['name']}" уже есть''')

print(f'Герои, чья сила больше 50:')
heros = session.query(Heroes).filter(Heroes.strength > 50).order_by(Heroes.strength.desc())
for hero in heros:

    print(f'"{hero.name}" - {hero.strength} - {hero.image}')