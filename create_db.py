import sqlite3

conn = sqlite3.connect('urls.db')
c = conn.cursor()

c.execute('CREATE TABLE mappings (short_url TEXT, long_url TEXT)')
conn.commit()

conn.close()
