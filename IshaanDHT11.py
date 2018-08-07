import RPi.GPIO as GPIO
import dht11
#import Adafruit_DHT as dht11
import httplib, urllib, json
import time
import sys
import json
import requests
import sqlite3


# initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

#Declaration of global variables whose value coming from configuratin file
global conf_DHT11Interval
global conf_DHT11DeviceId

global conf_InfoLogTypeDescriptor
global conf_ErrorLogTypeDescriptor
global conf_WarningLogTypeDescriptor

#time.sleep(30)#Initialization delay
#Opening json configuration file, and setting variable values by key-pair from json file
with open('/home/pi/transfer/Final_init_ControlEnv.py/myconfig.json') as data_file:
        #Specifying that we are using global variables
        global conf_DHT11Interval
        global conf_DHT11DeviceId
        global conf_InfoLogTypeDescriptor
        global conf_ErrorLogTypeDescriptor
        global conf_WarningLogTypeDescriptor

        jsonData = json.load(data_file)#Loding json data
        #setting variable values by key-pair
        conf_DHT11Interval = int( jsonData["DHT11Interval"] )

        conf_DHT11DeviceId = jsonData["DHT11DeviceId"]

        conf_InfoLogTypeDescriptor = jsonData["InfoLogTypeDescriptor"]
        conf_ErrorLogTypeDescriptor = jsonData["ErrorLogTypeDescriptor"]
        conf_WarningLogTypeDescriptor = jsonData["WarningLogTypeDescriptor"]
while True:

    try:
      flag=0
      err_count=0
      while flag==0 :

        # read data using pin 22
        instance = dht11.DHT11(pin = 17)
        result = instance.read()
       # SVP = (610.7)* (10^ ((7.5*(result.temperature))/(237.3+(result.temperature)))
       # VPD = ((100-(result.humidity))/100)* SVP
        if result.is_valid():


            print("###########################################################")
            print("Temperature: %d C" % result.temperature)
            print("Humidity: %d %%" % result.humidity)
	    #print("VPDValue: %d" % VPD)
            print str(time.strftime("%Y-%m-%d %H:%M:%S"))
            flag=1

            #Maintaining log
            #Opening log file,writting log,closing log file
            logFileName="/home/pi/transfer/Final_init_ControlEnv.py/IshaanLogFiles/Log_"+ str(time.strftime("%Y%m%d")) # Log file name
            Log_File = open("%s.txt" % logFileName,"a+") #Opening log file in append mode

            #Log for sensor
            logdata =str("| LogType=") + str(conf_InfoLogTypeDescriptor) + str("  |  ") + str("DeviceId=5") + str("  |SensorName=DHT11|  Temp=") + str (result.temperature)+ str("Humidity=")+ str(result.humidity) + str("  |Timestamp=") + str(time.strftime("%Y-%m-%d %H:%M:%S")) + str(" |")
            Log_File .write (str(logdata) + "\n") #Writing log to file

            Log_File.close() #Log file closed
            print("Information log created.")

            #Inserting data in database
            #Connecting database,inserting data, commit changes and closing database connection
            db = sqlite3.connect('/home/pi/transfer/Final_init_ControlEnv.py/DatabaseControlled.db') #Connecting database
            cursor = db.cursor() #Creating cursor object

            #Executing insert queries
            cursor.execute("INSERT INTO SensorData ( SensorDeviceId, SensorName, ValueTag, value , ValueTag1, value1 , ValueTag2, value2 , ValueTag3, value3 , IsActive , CreatedDate, ModifiedDate ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
                     ( str(conf_DHT11DeviceId), str("DHT11") ,str("temperature"),  str(result.temperature),str("humidity") , str(result.humidity) ,str("NA") , str("NA") ,str("NA") , str("NA") , str("1") , str(time.strftime("%Y-%m-%d %H:%M:%S")), str(time.strftime("%Y-%m-%d %H:%M:%S"))   ))

            db.commit() #Commit changes
            db.close() #closing database
            print"Data inserted in table  " + str(time.strftime("%Y-%m-%d %H:%M:%S"))



            time.sleep(conf_DHT11Interval)
            continue

        else:
            err_count += 1
            print err_count
            if err_count > 10 :
                print("Error >10 : %d" % result.error_code)
                err_count=0
                #Maintaining log
                #Opening log file,writting log,closing log file
                logFileName="/home/pi/transfer/Final_init_ControlEnv.py/IshaanLogFiles/Log_"+ str(time.strftime("%Y%m%d")) # Log file name
                Log_File = open("%s.txt" % logFileName,"a+") #Opening log file in append mode

                #Log for sensor
                logdata =str("| LogType=") + str(conf_ErrorLogTypeDescriptor) + str("  |  ") + str("DeviceId=5") + str("  |SensorName=DHT11|  Temp=") + str ("NA")+ str("Humidity=")+ str("NA") + str("VPDValue") + str("NA") + str("  |Timestamp=") + str(time.strftime("%Y-%m-%d %H:%M:%S")) + str(" |")
                Log_File .write (str(logdata) + "\n") #Writing log to file

                Log_File.close() #Log file closed
                print("Error log created.")

                time.sleep(conf_DHT11Interval)
                continue
            time.sleep(6)
            continue
    except:
            print "Exception Occurs."
            #continue
            #Maintaining log
            #Opening log file,writting log,closing log file
            logFileName="/home/pi/transfer/Final_init_ControlEnv.py/IshaanLogFiles/Log_"+ str(time.strftime("%Y%m%d")) # Log file name
            Log_File = open("%s.txt" % logFileName,"a+") #Opening log file in append mode

            #Log for sensor
            logdata =str("| LogType=") + str(conf_ErrorLogTypeDescriptor) + str("  |  ") + str("DeviceId=5") + str("  |SensorName=DHT11|  Temp=") + str ("NA")+ str("Humidity=")+  str("NA") + str("VPDValue") + str("NA") + str("  |Timestamp=") + str(time.strftime("%Y-%m-%d %H:%M:%S")) + str(" |")
 
            Log_File .write (str(logdata) + "\n") #Writing log to file

            Log_File.close() #Log file closed
            print("Error log created.")
            time.sleep(10)
    continue



