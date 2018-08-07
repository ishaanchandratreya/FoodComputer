import sqlite3
import requests
import sys
import time
import json
import RPi.GPIO as GPIO

global conf_GDM_URL
global conf_InfoLogTypeDescriptor
global conf_ErrorLogTypeDescriptor
global conf_WarningLogTypeDescriptor

#time.sleep(40)#Initialization delay

with open('/home/pi/transfer/Final_init_ControlEnv.py/myconfig.json') as data_file:
        global conf_GDM_URL
        global conf_InfoLogTypeDescriptor
        global conf_ErrorLogTypeDescriptor
        global conf_WarningLogTypeDescriptor

        jsonData = json.load(data_file)
        conf_GDM_URL = jsonData["GDM_URL"]
        conf_InfoLogTypeDescriptor = jsonData["InfoLogTypeDescriptor"]
        conf_ErrorLogTypeDescriptor = jsonData["ErrorLogTypeDescriptor"]
        conf_WarningLogTypeDescriptor = jsonData["WarningLogTypeDescriptor"]

print conf_GDM_URL

GPIO.setmode(GPIO.BCM)

# init list with pin numbers    
pinList =[23,24,22,27]

for i in pinList:
  GPIO.setup(i, GPIO.OUT)
  GPIO.output(i, GPIO.HIGH)

#time.sleep(30)
l=0
f=0
h=0
p=0

command_text=1
executionFlag=0

while True:
           try:
                db = sqlite3.connect('/home/pi/transfer/Final_init_ControlEnv.py/DatabaseControlled.db') #Connecting database
                cursor = db.cursor() #Creating cursor object

                sql = "SELECT COUNT(*),max(ID) FROM SensorControl"
                cursor.execute(sql);
                count,max_id = cursor.fetchone()
                print""
                print "MaxID",max_id
                print "Count",count
                time.sleep(5)

                if (count == 0):
                    print ("Empty Database")
                    db.close()
                    continue

                SQL = "SELECT * FROM SensorControl WHERE ID <= %s" % max_id;
                cursor.execute(SQL);
                list = cursor.fetchall()

                #print list[0]
                #print list[len(list)-1]

                for x in list:
                    ID= str(x[0])
                    print "\nID =%s" %ID
                    DIVICE_ID = str(x[1])
                    AlertAction = str(x[2])
                    ACTIVITY_DATE = str(x[4])

                    if(AlertAction == str("FAN=ON")):
                        if(f == 0):
                          print"Executing FAN=ON"
                          GPIO.output(22, GPIO.HIGH)
                          f=1
                          executionFlag=1
                        else:
                          print("FAN is already in ON state")
                    elif(AlertAction == str("FAN=OFF")):
                        if(f == 1):
                          print"Executing FAN=OFF"
                          GPIO.output(22, GPIO.LOW)
                          f=0
                          executionFlag=1
                        else:
                          print("FAN is already is in OFF state")

                    elif(AlertAction == str("PUMP=ON")):
                        if(p == 0):
                          print"Executing PUMP=ON"
                          GPIO.output(27, GPIO.HIGH)
                          p=1
                          executionFlag=1
                        else:
                          print("PUMP is already is in ON state")
                    elif(AlertAction == str("PUMP=OFF")):
                        if(p == 1):
                          print"Executing PUMP=OFF"
                          GPIO.output(27, GPIO.LOW)
                          p=0
                          executionFlag=1
                        else:
                          print("PUMP is already is in OFF state")
                    elif(AlertAction == str("LIGHT=ON")):
                        if(l == 0):
                          print"Executing LIGHT=ON"
                          GPIO.output(24, GPIO.HIGH)
                          l=1
                          executionFlag=1
                        else:
                          print("LIGHT is already is in ON state")
                    elif(AlertAction == str("LIGHT=OFF")):
                        if(l == 1):
                          print"Executing LIGHT=OFF"
                          GPIO.output(24, GPIO.LOW)
                          l=0
                          executionFlag=1
                        else:
                          print("LIGHT is already is in OFF state")
                    elif(AlertAction == str("HUMIDIFIER=ON")):
                        if(h == 0):
                          print"Executing HUMIDIFIER=ON"
                          GPIO.output(23, GPIO.HIGH)
                          h=1
                          executionFlag=1
                        else:
                          print("HUMIDIFIER is already is in ON state")
                    elif(AlertAction == str("HUMIDIFIER=OFF")):
                        if(h == 1):
                          print"Executing HUMIDiFIER=OFF"
                          GPIO.output(23, GPIO.LOW)
                          h=0
                          executionFlag=1
                        else:
                          print("HUMIDIFIER is already is in OFF state")


                    else:
                        print" '%s' is Invalid Trigger command, please make sure trigger message given at GDM is in correct format as per technical document" %AlertAction
                        command_text=0

                    #Maintaining log
                    #Opening log file,writting log,closing log file
                    logFileName="/home/pi/transfer/Final_init_ControlEnv.py/IshaanLogFiles/Log_"+ str(time.strftime("%Y%m%d")) # Log file name
                    Log_File = open("%s.txt" % logFileName,"a+") #Opening log file in append mode

                    if(executionFlag == 1):
                      logdata =str("| LogType=") + str(conf_InfoLogTypeDescriptor) + str("  |  ") + str("DeviceId=5") + str("  |SensorName=ControlSensor|  ") + str ("|Action : ")+ str(AlertAction) + str("  |Timestamp=") + str(time.strftime("%Y-%m-%d %H:%M:%S")) + str(" |")
                      Log_File .write (str(logdata) + "\n") #Writing log to file
                      Log_File.close() #Log file closed
                      print("Information log created.")
                      executionFlag=0

                    elif(command_text == 0):
                      logdata =str("| LogType=") + str(conf_ErrorLogTypeDescriptor) + str("  |  ") + str("DeviceId=5") + str("  |SensorName=ControlSensor|  ") + str ("|Action : ")+str("InvalidTrigger") + str("  |Timestamp=") + str(time.strftime("%Y-%m-%d %H:%M:%S")) + str(" |")
                      Log_File .write (str(logdata) + "\n") #Writing log to file
                      Log_File.close() #Log file closed
                      print("Error log created.")
                      command_text=1

                    qwry = "DELETE FROM SensorControl WHERE ID = %s" % ID
                    cursor.execute(qwry);
                    db.commit()

                db.close()
                time.sleep(5)
                continue

           except:
              print"Exception occurs."
              #Maintaining log
              #Opening log file,writting log,closing log file
              logFileName="/home/pi/transfer/Final_init_ControlEnv.py/IshaanLogFiles/Log_"+ str(time.strftime("%Y%m%d")) # Log file name
              Log_File = open("%s.txt" % logFileName,"a+") #Opening log file in append mode
              logdata =str("| LogType=") + str(conf_ErrorLogTypeDescriptor) + str("  |  ") + str("DeviceId=5") + str("  |SensorName=ControlSensor|  ") + str ("Value=")+ str("Error") + str("  |Timestamp=") + str(time.strftime("%Y-%m-%d %H:%M:%S")) + str(" |")
              Log_File .write (str(logdata) + "\n") #Writing log to file
              Log_File.close() #Log file closed
              print("Error log created.")
              time.sleep(10)
              continue

