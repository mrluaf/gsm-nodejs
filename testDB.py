import sqlite3
from datetime import datetime
conn = sqlite3.connect('modem.db')
c = conn.cursor()
c.execute('SELECT * FROM COMS WHERE name=?', (ser.port,))
if c.fetchone() == None:
    isReady_Time = datetime.timestamp(datetime.now())
    c.execute("INSERT INTO COMS (name, isReady, isReady_Time) VALUES (?, ?, ?)",
        (ser.port, True, isReady_Time)
    )
else:
    isReady_Time = datetime.timestamp(datetime.now())
    c.execute("UPDATE COMS SET isReady = ?, isReady_Time =? WHERE name = ?",
        (True, isReady_Time, ser.port)
    )
