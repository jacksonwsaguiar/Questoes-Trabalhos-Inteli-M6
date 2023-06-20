import sqlite3

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

conn = get_db_connection()
conn.executescript('DELETE FROM images;')
conn.executescript('VACUUM;')
conn.commit()
conn.close()