import psycopg2

con = psycopg2.connect(
    database='test',
    user='slava',
    password='7548',
    host="127.0.0.1",
    port='5432'
    )

cur = con.cursor()


cur.execute('''CREATE TABLE IF NOT EXISTS artist(
                id SERIAL PRIMARY KEY,
                title VARCHAR(40) NOT NULL);''')

cur.execute('''CREATE TABLE IF NOT EXISTS genre(
                id SERIAL PRIMARY KEY,
                title VARCHAR(40) NOT NULL);''')

cur.execute('''CREATE TABLE IF NOT EXISTS artist_genre(
                artist_id INTEGER REFERENCES artist(id),
                genre_id INTEGER REFERENCES genre(id),
                CONSTRAINT ag PRIMARY KEY (artist_id, genre_id));''')

cur.execute('''CREATE TABLE IF NOT EXISTS album(
                id SERIAL PRIMARY KEY,
                title VARCHAR(40) NOT NULL,
                release INTEGER,
                artist_id INTEGER REFERENCES artist(id));''')

cur.execute('''CREATE TABLE IF NOT EXISTS track(
                id SERIAL PRIMARY KEY,
                title VARCHAR(40) NOT NULL,
                duration INTEGER,
                album_id INTEGER REFERENCES album(id));''')

con.commit()

#
# cur.execute('''INSERT INTO genre(title) VALUES ('hiphop')
#             ''')
#
# con.commit()

# cur.execute('''DELETE FROM genre WHERE id=8;
#
#             ''')
#
# con.commit()

# cur.execute('''ALTER TABLE artist RENAME TO artists;
#
#             ''')
#
# con.commit()

# cur.execute('''ALTER TABLE track RENAME title TO titles;
#
#             ''')
#
# con.commit()

cur.execute('''SELECT title FROM genre;''')
# for item in cur.fetchall():
#     print(item[0])

print([item[0] for item in cur.fetchall()])
