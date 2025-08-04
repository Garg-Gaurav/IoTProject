import sqlite3
import datetime
import random
import time





DB_FILE='MarvelMindTracking.db'
connect_sql=sqlite3.connect(DB_FILE)

command_cre="""CREATE TABLE IF NOT EXISTS readings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp datetime NOT NULL,
                hedge_id Integer NOT NULL, 
                x REAL NOT NULL,
                y REAL NOT NULL,
                z REAL NOT NULL
            )"""

sql_cursor=connect_sql.cursor()

sql_cursor.execute(command_cre)

connect_sql.commit()
connect_sql.close()
