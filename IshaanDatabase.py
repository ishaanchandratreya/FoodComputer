mport time
import sys
import json
import requests
import sqlite3

try:

    db = sqlite3.connect('/home/pi/transfer/Final_init_ControlEnv.py/DatabaseControlled.db')
    cursor = db.cursor()
    cursor.execute(''' 
    CREATE TABLE IF NOT EXISTS SensorMaster ( 
            ID                   INTEGER PRIMARY KEY AUTOINCREMENT,
            DeviceId             text NOT NULL  ,
            Name                 text NOT NULL  ,
            Unit                 text   ,
            UpdateInterval       integer   ,
            Location             text   ,
            IsActive             text   ,
            CreatedDate          text   ,
            ModifiedDate         text   
     )
     ''')

    cursor.execute(''' 
    CREATE TABLE IF NOT EXISTS SensorData ( 
            ID                   INTEGER PRIMARY KEY AUTOINCREMENT,
            SensorDeviceId       text NOT NULL  ,
            SensorName           text NOT NULL  ,
            
            ValueTag             text   ,
            Value                text   ,
            ValueTag1            text   ,
            Value1               text   ,
            
            ValueTag2            text   ,
            Value2               text   ,
            
            ValueTag3            text   ,
            Value3               text   ,
            
            IsActive             text   ,
            CreatedDate          text   ,
            ModifiedDate         text   
     )
     ''')

    cursor.execute(''' 
    CREATE TABLE IF NOT EXISTS SensorControl ( 
            ID                   INTEGER PRIMARY KEY AUTOINCREMENT,
            SensorDeviceId       text NOT NULL  ,
            AlertAction          text NOT NULL  ,
            IsActive             text   ,
            CreatedDate          text   ,
            ModifiedDate         text  
     )
     ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS PiSensorData (
            ID                   INTEGER PRIMARY KEY AUTOINCREMENT,
            SensorDeviceId       text NOT NULL  ,
            SensorName           text NOT NULL  ,
            Value                text NOT NULL  ,
            Value1               text   ,
            Value2               text   ,
            Value3               text   ,
            IsActive             text   ,
            CreatedDate          text   ,
            ModifiedDate         text
     )

     ''')

    db.commit()
    db.close()
    print " Database script executed successfully\n"

except:
    print"Exception Occurs"


