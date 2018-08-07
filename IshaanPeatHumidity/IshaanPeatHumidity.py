
#Import statemrnts
import time
import sqlite3
import json
import ADS1x15 #Import the ADS1x15 module


#Declaration of global variables whose value coming from configuratin file
global conf_PeatHumidityInterval
global conf_PeatHumidityDeviceId


global conf_InfoLogTypeDescriptor
global conf_ErrorLogTypeDescriptor
global conf_WarningLogTypeDescriptor

global conf_PeatHumidityCorrection


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
        global conf_PeatHumidityInterval
        global conf_PeatHumidityDeviceId
        global conf_PeatHumidityCorrection
        global conf_InfoLogTypeDescriptor
        global conf_ErrorLogTypeDescriptor
        global conf_WarningLogTypeDescriptor
	
	jsonData = json.load(data_file)#Loding json data
	#setting variable values by key-pair
        conf_PeatHumidityInterval = int( jsonData["PeatHumidityInterval"] )

	conf_PeatHumidityDeviceId= jsonData["PeatHumidityDeviceId"]


	conf_PeatHumidityCorrection = jsonData["PeatHumidityCorrection"]
	

	conf_InfoLogTypeDescriptor = jsonData["InfoLogTypeDescriptor"]
	conf_ErrorLogTypeDescriptor = jsonData["ErrorLogTypeDescriptor"]
	conf_WarningLogTypeDescriptor = jsonData["WarningLogTypeDescriptor"]

while(True):#infinite loop for contineous execution of script
    try:
        print"\n-------------------------------------------------------------------------"
        # Create an ADS1115 ADC instance.
        adc = ADS1x15.ADS1115()

        #Now reading soil moisture values from ADC(A0) to ADS(A3)
        PeatHumidityValue= adc.read_adc(0)



        print("\nSoil Moisture Value=%s"%PeatHumidityValue)


        
        

        #Maintaining log
        #Opening log file,writting log,closing log file
        logFileName="/home/pi/transfer/Final_init_ControlEnv.py/IshaanLogFiles/Log_"+ str(time.strftime("%Y%m%d")) # Log file name
        Log_File = open("%s.txt" % logFileName,"a+") #Opening log file in append mode

        #Log for PeatHumidity sensor
        logdata =str("| LogType=") + str(conf_InfoLogTypeDescriptor) + str("  |  ") + str("DeviceId=3") + str("  |SensorName=PeatHumidity|  ") + str ("Value=")+ str(PeatHumidityValue) + str("  |Timestamp=") + str(time.strftime("%Y-%m-%d %H:%M:%S")) + str(" |")
        Log_File .write (str(logdata) + "\n") #Writing log to file

        Log_File.close() #Log file closed
        print("\nInformation log created.")

        #Inserting data in database
        #Connecting database,inserting data, commit changes and closing database connection
        db = sqlite3.connect('/home/pi/transfer/Final_init_ControlEnv.py/DatabaseControlled.db') #Connecting database
        cursor = db.cursor() #Creating cursor object
        
        #Executing insert queries
	cursor.execute("INSERT INTO SensorData ( SensorDeviceId, SensorName, ValueTag, value , ValueTag1, value1 , ValueTag2, value2 , ValueTag3, value3 , IsActive , CreatedDate, ModifiedDate ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
    		 ( str(conf_PeatHumidityDeviceId), str("PeatHumidity") ,str("PeatHumidityValue"),  str(PeatHumidityValue),str("NA") , str("NA") ,str("NA") , str("NA") ,str("NA") , str("NA") , str("1") , str(time.strftime("%Y-%m-%d %H:%M:%S")), str(time.strftime("%Y-%m-%d %H:%M:%S"))   ))

	
        db.commit() #Commit changes
        db.close() #closing database
        print"Data inserted in table  " + str(time.strftime("%Y-%m-%d %H:%M:%S"))

    except:
        print"\nException occurs "+ str(time.strftime("%Y-%m-%d %H:%M:%S"))

        #Maintaining log
        #Opening log file,writting log,closing log file
        logFileName="/home/pi/transfer/Final_init_ControlEnv.py/IshaanLogFiles/Log_"+ str(time.strftime("%Y%m%d")) # Log file name
        Log_File = open("%s.txt" % logFileName,"a+") #Opening log file in append mode

        #Log for error
        logdata =str("| LogType=") + str(conf_ErrorLogTypeDescriptor) + str(" |  ") + str("DeviceId=3") + str("  |SensorName=PeatHumidity|  ") + str ("Value=")+ str("Error") + str("  |Timestamp=") + str(time.strftime("%Y-%m-%d %H:%M:%S")) + str(" |")
        Log_File .write (str(logdata) + "\n") #Writing log to file
        
        Log_File.close() #Log file closed
        print("Error log created.")
        
    time.sleep(conf_PeatHumidityInterval) #wait for specified interval of time

