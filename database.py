from datetime import datetime
import sqlite3

def init(c: sqlite3.Cursor) -> None:
    c.execute('''CREATE TABLE IF NOT EXISTS temperature (
    time TIMESTAMP NOT NULL,
    temp REAL NOT NULL,
    PRIMARY KEY (time)
);''')

    c.execute('''CREATE TABLE IF NOT EXISTS state (
    time TIMESTAMP NOT NULL,
    device TEXT NOT NULL,
    state TEXT NOT NULL,
    PRIMARY KEY (time)
);''')


def saveTemperature(c: sqlite3.Cursor, temp: float) -> None:
    c.execute(f'''INSERT INTO temperature
    values("{datetime.now()}", "{temp}");
''')


'''
device: 'furnace'
state:  'on', 'off'
'''
def saveState(c: sqlite3.Cursor, device: str, state: str) -> None:
    c.execute(f'''INSERT INTO state
    values("{datetime.now()}", "{device}", "{state}");
''')


def getLatestTemp(c: sqlite3.Cursor) -> float:
    c.execute('''SELECT *
    FROM temperature
    ORDER BY time DESC
    LIMIT 1;
''')

    res = c.fetchone()
    if res == []:
        return None
    else:
        return res[1]
