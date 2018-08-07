#Import statemrnts
import time
import sqlite3
import json
from tsl2561 import TSL2561

#Declaration of global variables whose value coming from configuratin file
global conf_LuminosityInterval
global conf_LuminosityDeviceId

global conf_LuminosityCorrection

global conf_InfoLogTypeDescriptor
global conf_ErrorLogTypeDescriptor
global conf_WarningLogTypeDescriptor

#time.sleep(30)#Initialization delay


def correctionValidation(correctionValues):
    try:
        c=correctionValues[0]
        new_correctionValues=str(correctionValues)
        new_correctionValues=new_correctionValues.replace(" ","")
        new_correctionValues=new_correctionValues.replace("[","")
        new_correctionValues=new_correctionValues.replace("]","")
        items_in_string = new_correctionValues.split(",")
        m=float(correctionValues[1])
        b=float(correctionValues[2])
        
        if( (c==0 or c==1) and len(items_in_string)==3 ):
            return(1)
        else:
            raise 
        
    except:
        return(0)


#Opening json configuration file, and setting variable values by key-pair from json file
with open('/home/pi/transfer/Final_init_ControlEnv.py/myconfig.json') as data_file:
        #Specifying that we are using global variables
	global conf_LuminosityInterval
	global conf_LuminosityDeviceId

	global conf_LuminosityCorrection

	global conf_InfoLogTypeDescriptor
	global conf_ErrorLogTypeDescriptor
	global conf_WarningLogTypeDescriptor
	
	jsonData = json.load(data_file)#Loding json data
	#setting variable values by key-pair
        conf_LuminosityInterval = int( jsonData["LuminosityInterval"] )
	conf_LuminosityDeviceId = jsonData["LuminosityDeviceId"]

	conf_LuminosityCorrection = jsonData["LuminosityCorrection"]

	conf_InfoLogTypeDescriptor = jsonData["InfoLogTypeDescriptor"]
	conf_ErrorLogTypeDescriptor = jsonData["ErrorLogTypeDescriptor"]
	conf_WarningLogTypeDescriptor = jsonData["WarningLogTypeDescriptor"]

while(True):#infinite loop for contineous execution of script
    try:
        print"\n-------------------------------------------------------------------------"
        tsl = TSL2561(debug=1)
        light=int(tsl.lux())
        print "\nLight: %s " %light

        l=correctionValidation(conf_LuminosityCorrection)

        if( l==1):
            print "correct syntax for correction"
            if( int(conf_LuminosityCorrection[0])==1):
                print "\n" + str(conf_LuminosityCorrection)
                light= ( int(light) * float(conf_LuminosityCorrection[1]))  + float(conf_LuminosityCorrection[2])
                print("Corrected Light Value=%s"%light )

        else:
            print "\nIncorrect syntax for correction"
            #Maintaining log
            #Opening log file,writting log,closing log file
            logFileName="/home/pi/transfer/Final_init_ControlEnv.py/IshaanLogFiles/Log_"+ str(time.strftime("%Y%m%d")) # Log file name
            Log_File = open("%s.txt" % logFileName,"a+") #Opening log file in append mode

            #Log for error
            logdata =str("| LogType=") + str(conf_ErrorLogTypeDescriptor) + str(" |  ") + str("DeviceId=6") + str("  |SensorName=Luminosity|  ") + str ("Value=")+ str("incorrect syntax for linear correction in config.json") + str("  |Timestamp=") + str(time.strftime("%Y-%m-%d %H:%M:%S")) + str(" |")
            Log_File .write (str(logdata) + "\n") #Writing log to file
            
            Log_File.close() #Log file closed
            print("Error log created.")

        
        
        #Maintaining log
        #Opening log file,writting log,closing log file
        logFileName="/home/pi/transfer/Final_init_ControlEnv.py/IshaanLogFiles/Log_"+ str(time.strftime("%Y%m%d")) # Log file name
        Log_File = open("%s.txt" % logFileName,"a+") #Opening log file in append mode

        #Log for Luminosity sensor
        logdata =str("| LogType=") + str(conf_InfoLogTypeDescriptor) + str("  |  ") + str("DeviceId=6") + str("  |SensorName=Luminosity|  ") + str ("Light=")+ str(light) + str("  |Timestamp=") + str(time.strftime("%Y-%m-%d %H:%M:%S")) + str(" |")
        Log_File .write (str(logdata) + "\n") #Writing log to file

        Log_File.close() #Log file closed
        print("\nInformation log created.")

        #Inserting data in database
        #Connecting database,inserting data, commit changes and closing database connection
        db = sqlite3.connect('/home/pi/transfer/Final_init_ControlEnv.py/DatabaseControlled.db') #Connecting database
        cursor = db.cursor() #Creating cursor object

        #Executing insert queries       
        cursor.execute("INSERT INTO SensorData ( SensorDeviceId, SensorName, ValueTag, value , ValueTag1, value1 , ValueTag2, value2 , ValueTag3, value3 , IsActive , CreatedDate, ModifiedDate ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
    		 ( str(conf_LuminosityDeviceId), str("Luminosity") ,str("light"),  str(light),str("NA") , str("NA") ,str("NA") , str("NA") ,str("NA") , str("NA") , str("1") , str(time.strftime("%Y-%m-%d %H:%M:%S")), str(time.strftime("%Y-%m-%d %H:%M:%S"))   ))

        db.commit() #Commit changes
        db.close() #closing database
        print"Data inserted in table  " + str(time.strftime("%Y-%m-%d %H:%M:%S"))

    except:
        print"Exception occurs  "+ str(time.strftime("%Y-%m-%d %H:%M:%S"))
        #Maintaining log
        #Opening log file,writting log,closing log file
        logFileName="/home/pi/transfer/Final_init_ControlEnv.py/IshaanLogFiles/Log_"+ str(time.strftime("%Y%m%d")) # Log file name
        Log_File = open("%s.txt" % logFileName,"a+") #Opening log file in append mode

        #Log for error
        logdata =str("| LogType=") + str(conf_ErrorLogTypeDescriptor) + str(" |  ") + str("DeviceId=6") + str("  |SensorName=Luminosity|  ") + str ("Value=")+ str("Error") + str("  |Timestamp=") + str(time.strftime("%Y-%m-%d %H:%M:%S")) + str(" |")
        Log_File .write (str(logdata) + "\n") #Writing log to file
        
        Log_File.close() #Log file closed
        print("Error log created.")

    time.sleep(conf_LuminosityInterval) #wait for specified interval of time



