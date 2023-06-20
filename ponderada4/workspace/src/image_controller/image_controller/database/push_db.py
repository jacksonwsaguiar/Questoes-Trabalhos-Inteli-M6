import sqlite3
import os
connection = sqlite3.connect('./database.db')


print(os.path.abspath("."))
with open('database/schema.sql') as f:
    connection.executescript(f.read())


connection.commit()
connection.close()