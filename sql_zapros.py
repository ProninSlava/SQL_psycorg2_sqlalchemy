import sqlalchemy
from pprint import pprint
from functools import reduce

engine = sqlalchemy.create_engine('postgresql://slava:7548@localhost:5432/music_bd')
connection = engine.connect()

# 1 название и год выхода альбомов, вышедших в 2018 году
print('____________________________')
sel = connection.execute(
    '''
    SELECT name, years FROM album
    WHERE years = 2018;

    ''').fetchall()
pprint(sel)

# 2 название и продолжительность самого длительного трека
print('____________________________')
sel = connection.execute(
    '''
    SELECT name, times FROM track
    ORDER BY times DESC

    ''').fetchone()
pprint(sel)


# 3 название треков, продолжительность которых не менее 3,5 минуты
print('____________________________')
sel = connection.execute(
    '''
    SELECT name, times FROM track
    WHERE times > 230

    ''').fetchall()
pprint(sel)

# 4 названия сборников, вышедших в период с 2018 по 2020 год включительно
print('____________________________')
sel = connection.execute(
    '''
    SELECT name FROM collection
    WHERE years BETWEEN 2010 AND 2020;

    ''').fetchall()
pprint(sel)

# 5 исполнители, чье имя состоит из 1 слова
print('____________________________')
sel = connection.execute(
    '''
    SELECT name FROM musician
    WHERE name NOT LIKE'%% %%';

    ''').fetchall()
pprint(sel)

# 6 название треков, которые содержат слово "мой"/"my"
print('____________________________')
sel = connection.execute(
    '''
    SELECT name FROM track
    WHERE name  iLIKE'%%my%%';

    ''').fetchall()
pprint(sel)



#1 количество исполнителей в каждом жанре
print('1________________________________________________')
sel = connection.execute(
    '''
    SELECT s.name, COUNT(m.name) mn FROM style s
    JOIN musician_style ms ON s.id = ms.style_id
    JOIN musician m ON ms.style_id = m.id
    GROUP BY s.id
    ORDER BY mn DESC;
    
    ''').fetchall()
pprint(sel)

#2 количество треков, вошедших в альбомы 2019-2020 годов
print('2________________________________________________')
sel = connection.execute(
    '''
    SELECT a.name, COUNT(t.name) cn FROM album a
    JOIN track t ON a.id = t.album_id
    WHERE a.years BETWEEN 2010 AND 2020
    GROUP BY a.name
    ORDER BY cn DESC;

    ''').fetchall()
pprint(sel)

#3 средняя продолжительность трека по каждому альбому
print('3________________________________________________')
sel = connection.execute(
    '''
    SELECT a.name, ROUND(AVG(t.times)) at FROM album a
    JOIN track t ON a.id = t.album_id
    GROUP BY a.name
    ORDER BY at DESC;

    ''').fetchall()
pprint(sel)

#4 все исполнители, которые не выпустили альбомы в 2018 году
print('4________________________________________________')
sel = connection.execute(
    '''
    SELECT m.name FROM musician m
    WHERE m.name NOT IN
    (SELECT m.name FROM musician m
    JOIN musician_album ma ON m.id = ma.musician_id
    JOIN album a ON ma.album_id = a.id
    WHERE a.years = 2018)
    ORDER BY m.name;

    ''').fetchall()
pprint(sel)

#5 названия сборников, в которых присутствует конкретный исполнитель (выберите сами)
print('5________________________________________________')
sel = connection.execute(
    '''
    SELECT DISTINCT 
    c.name FROM collection c
    JOIN track_collection tc ON c.id = tc.collection_id
    JOIN track t ON tc.track_id = t.id
    JOIN album a ON t.album_id = a.id
    JOIN musician_album ma ON a.id = ma.album_id
    JOIN musician m ON ma.musician_id = m.id
    WHERE m.name  iLIKE '%%Стинг%%'
    ORDER BY c.name;

    ''').fetchall()
pprint(sel)


#6 название альбомов, в которых присутствуют исполнители более 1 жанра
print('6________________________________________________')
sel = connection.execute(
    '''
    SELECT a.name  FROM album a
    JOIN musician_album ma ON a.id = ma.album_id
    JOIN musician m ON ma.musician_id = m.id
    JOIN musician_style ms ON m.id = ms.musician_id
    JOIN style s ON ms.style_id = s.id
    GROUP BY a.name
    HAVING COUNT(s.name) > 1
    ORDER BY a.name;
    
    ''').fetchall()
pprint(sel)

#7 наименование треков, которые не входят в сборники
print('7________________________________________________')
sel = connection.execute(
    '''
    SELECT t.id, t.name  FROM track t
    LEFT JOIN track_collection tc ON t.id = tc.track_id
    WHERE tc.track_id IS NULL
    GROUP BY t.id
    ORDER BY t.id;
    
    ''').fetchall()
pprint(sel)

#8 исполнителя(-ей), написавшего самый короткий по продолжительности трек (теоретически таких треков может быть несколько)
print('8________________________________________________')
sel = connection.execute(
    '''
    SELECT m.name, t.times, t.name  FROM musician m
    JOIN musician_album ma ON m.id = ma.musician_id
    JOIN album a ON ma.album_id = a.id
    JOIN track t ON a.id = t.album_id
    GROUP BY m.name, t.times, t.name
    HAVING t.times = (SELECT MIN(t.times) FROM track t)
    ORDER BY m.name;   
  
    
    ''').fetchall()
pprint(sel)


#9 название альбомов, содержащих наименьшее количество треков!?
print('9________________________________________________')
sel = connection.execute(
    '''
    SELECT a.name FROM album a
    JOIN track t ON a.id = t.album_id
    GROUP BY a.id
    HAVING COUNT(t.name) = 
    (SELECT COUNT(t.name) FROM album a
    JOIN track t ON a.id = t.album_id
    GROUP BY a.id
    ORDER BY COUNT(t.name)
    LIMIT 1)
    

    ''').fetchall()
pprint(sel)


