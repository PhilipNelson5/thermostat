from typing import List, Set, Dict, Tuple, Optional
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

    c.execute('''CREATE TABLE IF NOT EXISTS schedule (
    start REAL NOT NULL,
    end REAL NOT NULL,
    temp REAL NOT NULL,
    days REAL NOT NULL,
    PRIMARY KEY (start, end)
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


def newSchedule(c: sqlite3.Cursor, start: int, end: int, temp: float, days: int) -> None:
    c.execute(f'''INSERT INTO schedule
    values("{start}", "{end}", "{temp}", "{days}");
''')


def getLatestTemp(c: sqlite3.Cursor) -> Optional[float]:
    c.execute(f'''SELECT *
    FROM temperature
    ORDER BY time DESC
    LIMIT 1;
''')

    res = c.fetchone()
    if res == []:
        return None
    else:
        return float(res[1])


def getHistory(c: sqlite3.Cursor, days) -> Optional[List[any]]:
    c.execute(f'''SELECT time, temp
    FROM temperature
    WHERE datetime(time) > date('now','-{days} day')
    ORDER BY datetime(time) asc
''')

    res = c.fetchall()
    if res == []:
        return None
    else:
        return res


def getSchedules(c: sqlite3.Cursor) -> Optional[List[Tuple[float, float, float, int]]]:
    c.execute('''SELECT *
    FROM schedule
''')

    res = c.fetchall()
    if res == []:
        return None
    else:
        return list(map(lambda args:
            (float(args[0]), float(args[1]), float(args[2]), int(args[3])), res))


