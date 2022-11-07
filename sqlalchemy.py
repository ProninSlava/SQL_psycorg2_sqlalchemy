from pprint import pprint

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, PrimaryKeyConstraint, Table, func

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import sessionmaker, relationship

# Класс Base
Base = declarative_base()

DSN = 'postgresql+psycopg2://slava:7548@localhost:5432/music_bd'

# Создание движка
engine = create_engine(DSN)

# Для получения соединения нужно использовать метод connect() объекта Engine, который возвращает объект типа Connection
connection = engine.connect()


#1
class Musician(Base):
    __tablename__ = 'musician'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    style = relationship("Style", secondary='musician_style', backref="musician")
    album = relationship("Album", secondary='musician_album', backref="musician")


#2
class Album(Base):
    __tablename__ = 'album'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    years = Column(Integer)
    # musician = relationship("Musician", secondary='musician_album', backref="musician")
    track = relationship("Track", backref='musician_album')

#3
class Track(Base):
    __tablename__ = 'track'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    times = Column(Integer, unique=True)
    album_id = Column(Integer, ForeignKey('album.id', ondelete='CASCADE'))
    collection = relationship("Collection", secondary='track_collection', backref="track")

#4
class Style(Base):
    __tablename__ = 'style'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)

#5
class Collection(Base):
    __tablename__ = 'collection'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    years = Column(Integer, unique=True)


#6
musician_style = Table(
    'musician_style', Base.metadata,
     Column('musician_id', Integer, ForeignKey('musician.id')),
     Column('style_id', Integer, ForeignKey('style.id')),
)

#7
track_collection = Table(
    'track_collection', Base.metadata,
     Column('track_id', Integer, ForeignKey('track.id')),
     Column('collection_id', Integer, ForeignKey('collection.id')),
)

#8
musician_album = Table(
    'musician_album', Base.metadata,
     Column('musician_id', Integer, ForeignKey('musician.id')),
     Column('album_id', Integer, ForeignKey('album.id')),
)

# Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# #dz1
print()
print(f'1. Название альбомов, которые вышли в 2018г.:')
albums = session.query(Album).filter(Album.years == 2010).all()
print(f''' "{', '.join([album.name for album in albums])}" ''')

# #dz2
print()
print(f'2. Самый короткий трек:')
tracks = session.query(Track).order_by(Track.times).limit(1)
for track in tracks:
    print(f'"{track.name}" - {track.times}сек')

#dz3
print()
print(f'3. Название треков, продолжительность которых не менее 3,5 минуты:')
tracks = session.query(Track).filter(Track.times > 210).order_by(Track.times.desc())
for track in tracks:
    print(f'"{track.name}" - {track.times}сек')

#dz4
print()
print(f'4. Названия сборников, вышедших в период с 2010 по 2020 год включительно:')
collections = session.query(Collection).filter(Collection.years > 2010, Collection.years < 2020).order_by(Collection.years.desc())
for collection in collections:
    print(f'"{collection.name}" - {collection.years}г.')

#dz5
print()
print(f'5. Исполнители, чье имя состоит из 1 слова:')
musicians = session.query(Musician).filter(Musician.name.notlike('%% %%'))
for musician in musicians:
    print(f'"{musician.name}" ')

#dz6
print()
print(f'6. Название треков, которые содержат слово «my»:')
tracks = session.query(Track).filter(Track.name.ilike('%%my%%'))
for track in tracks:
    print(f'"{track.name}" ')
#
# #dz1
# print()
# print(f'1. Количество исполнителей в каждом жанре:')
# styles = session.query(Style, func.count(Musician.id)).join(Style.musician).order_by(func.count(Musician.id)).group_by(Style.id)
# for style in styles:
#     print(f'"{style.Style.name}" - {style[1]}')
#
# #dz2
# print()
# print(f'2. Количество треков, вошедших в альбомы 2005-2020 годов:')
# al_trs = session.query(Album, func.count(Track.id)).join(Track).filter(Album.years > 2005, Album.years < 2020).order_by(func.count(Track.id)).group_by(Album.id)
# for al_tr in al_trs:
#     print(f'"{al_tr.Album.name}" - {al_tr[1]}')
#
# #dz3
# print()
# print(f'3. Средняя продолжительность треков по каждому альбому:')
# album_tracks = session.query(Album, func.avg(Track.times)).join(Track).order_by(func.avg(Track.times).desc()).group_by(Album.id)
# for item in album_tracks:
#     print(f' "{item.Album.name}" - {round(item[1])}сек.')