import time
import sys
import json
import requests
import sqlite3

try:
    db = sqlite3.connect('/home/pi/transfer/Final_init_ControlEnv.py/DatabaseControlled.db')
    cursor = db.cursor()

    cursor.execute(''' DELETE FROM SensorData ''')
    cursor.execute(''' DELETE FROM PiSensorData ''')
    cursor.execute(''' DELETE FROM SensorControl ''')


    db.commit()
    db.close()
    print " Truncate script executed successfully\n"

except:
    print"Exception Occurs"
