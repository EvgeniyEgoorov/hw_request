import sqlalchemy


db = 'postgresql://postgres:********@localhost:5432/postgres'
engine = sqlalchemy.create_engine(db)
connection = engine.connect()

# 1
res = connection.execute("""
SELECT title, COUNT(artist_id) FROM genre g
JOIN ArtistGenre a ON g.id = a.genre_id
GROUP BY g.id, g.title
ORDER BY g.id;
""").fetchall()
print(res)

# 2
res = connection.execute("""
SELECT a.title, COUNT(t.id) FROM album a
JOIN track t ON a.id = t.album_id
WHERE released BETWEEN 2018 AND 2020
GROUP BY a.title;
""").fetchall()
print(res)

# 3
res = connection.execute("""
SELECT a.title, AVG(duration) FROM album a
JOIN track t ON a.id = t.album_id
GROUP BY a.id, a.title
ORDER BY a.id;
""").fetchall()
print(res)

# 4
res = connection.execute("""
SELECT name FROM artist
WHERE name NOT IN (
    SELECT name FROM artist ar
    JOIN ArtistAlbum aa ON ar.id = aa.artist_id
    JOIN album al ON aa.album_id = al.id
    WHERE released = 2018
)
ORDER BY id;
""").fetchall()
print(res)

# 5
res = connection.execute("""
SELECT c.title FROM collection c
JOIN TrackCollection tc ON c.id = tc.collection_id
JOIN track t ON tc.track_id = t.id
JOIN album al ON t.album_id = al.id
JOIN ArtistAlbum aa ON al.id = aa.album_id
JOIN artist ar ON aa.artist_id = ar.id
WHERE name IN ('Queen')
ORDER BY c.id;
""").fetchall()
print(res)

# 6
res = connection.execute("""
SELECT c.title, COUNT(genre_id) FROM collection c
JOIN TrackCollection tc ON c.id = tc.collection_id
JOIN track t ON tc.track_id = t.id
JOIN album al ON t.album_id = al.id
JOIN ArtistAlbum aa ON al.id = aa.album_id
JOIN artist ar ON aa.artist_id = ar.id
JOIN ArtistGenre ag ON ar.id = ag.artist_id
GROUP BY c.id, c.title
HAVING COUNT(genre_id) > 1
ORDER BY c.id;
""").fetchall()
print(res)

# 7
res = connection.execute("""
SELECT title FROM track t
LEFT JOIN TrackCollection tc ON t.id = tc.track_id
WHERE tc.track_id IS NULL
ORDER BY t.id;
""").fetchall()
print(res)

# 8
res = connection.execute("""
SELECT name FROM artist ar
JOIN ArtistAlbum aa ON ar.id = aa.artist_id
JOIN album al ON aa.album_id = al.id
JOIN track t ON al.id = t.album_id
WHERE duration IN (
    SELECT MIN(duration) FROM track
)
ORDER BY ar.id;
""").fetchall()
print(res)

# 9
res = connection.execute("""
SELECT a.title FROM album a
JOIN track t ON a.id = t.album_id
WHERE t.album_id IN (
    SELECT album_id FROM track
    GROUP BY album_id
    HAVING COUNT(id) IN (
        SELECT COUNT(id) FROM track
        GROUP BY album_id
        ORDER BY COUNT(id)
        LIMIT 1
    )
)
GROUP BY a.id, a.title
ORDER BY a.id
""").fetchall()
print(res)
