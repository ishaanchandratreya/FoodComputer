import time
import json
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import sqlite3

global conf_GDM_URL

#time.sleep(40)#Initialization delay

with open('/home/pi/transfer/Final_init_ControlEnv.py/myconfig.json') as data_file:
        global conf_GDM_URL
        jsonData = json.load(data_file)
        conf_GDM_URL = jsonData["GDM_URL"]
print conf_GDM_URL

c=1
while True:
           try:
		
                log_file = open("/home/pi/transfer/Final_init_ControlEnv.py/Ishaan_Upload_Db_log.dat","a+")
                db = sqlite3.connect('/home/pi/transfer/Final_init_ControlEnv.py/DatabaseControlled.db') #Connecting database
               
                
                cursor = db.cursor() #Creating cursor object
                
                sql = "SELECT COUNT(*),max(ID) FROM SENSORDATA"
                cursor.execute(sql);
                count,max_id = cursor.fetchone()
                print "\nMaxID",max_id
                print "Count",count
                time.sleep(3)
                
                if (count == 0):
                    print ("Empty Database")
                    db.close()

                    if (c == 1):
                         data = str("Empty Database , ") + str(time.strftime("%Y-%m-%d %H:%M:%S"))
                         log_file.write (str(data) + "\n")
                         c=0
                    time.sleep(30)# Check After every interval
                    continue
                c=1
                SQL = "SELECT * FROM SENSORDATA WHERE ID <= %s" % max_id;
                cursor.execute(SQL);
                list = cursor.fetchall()

                print list[0]
                print list[len(list)-1]

                for x in list:
                    ID= str(x[0])
                    print "\nID =%s" %ID

                    DEVICE_ID = str(x[1])
                    #print "Device Id= %s"% DIVICE_ID

                    SENSOR_NAME = str(x[2])
                    #print SENSOR_NAME

                    VALUE_TAG = str(x[3])
                    #print  VALUE_TAG
                    VALUE = str(x[4])
                    #print VALUE

                    VALUE_TAG1 = str(x[5])
                    #print VALUE_TAG1
                    VALUE1 = str(x[6])
                    #print VALUE1

                    VALUE_TAG2 = str(x[7])
                    #print VALUE_TAG2
                    VALUE2 = str(x[8])
                    #print VALUE2

                    VALUE_TAG3 = str(x[9])
                    VALUE3 = str(x[10])

                    ACTIVITY_DATE = str(x[12])
                    #print "date= %s" %ACTIVITY_DATE

                    try:
                            #tempjson = '{"'+ str(SENSOR_NAME)+'":"' +str(VALUE)+ '","Date_time":"' +str(ACTIVITY_DATE)+ '"}'
                            if ( str(VALUE_TAG1) == "NA" ):
                                query = {str(VALUE_TAG):str(VALUE),"Date_time":str(ACTIVITY_DATE)}

                            elif ( str(VALUE_TAG2) == "NA" ):
                                query = {str(VALUE_TAG):str(VALUE), str(VALUE_TAG1):str(VALUE1), "Date_time":str(ACTIVITY_DATE)}

                            elif ( str(VALUE_TAG3) == "NA" ):
                                query = {str(VALUE_TAG):str(VALUE), str(VALUE_TAG1):str(VALUE1), str(VALUE_TAG2):str(VALUE2), "Date_time":str(ACTIVITY_DATE)}
                            else:
                                query = {str(VALUE_TAG):str(VALUE), str(VALUE_TAG1):str(VALUE1), str(VALUE_TAG2):str(VALUE2), str(VALUE_TAG3):str(VALUE3), "Date_time":str(ACTIVITY_DATE)}

                            tempjson = json.dumps(query)
                            #print tempjson

                            publish.single("/api/dump", payload=tempjson, qos=0, retain=True, hostname=conf_GDM_URL, port=1883, client_id=DEVICE_ID)

                            qwry = "DELETE FROM SENSORDATA WHERE ID = %s" % ID
                            cursor.execute(qwry);
                            db.commit()
                            print "Sent and Deleted Row: %s" % ID
                            data =str( "sent row = %s" % ID )+ str(" , ") +  str(time.strftime("%Y-%m-%d %H:%M:%S"))
                            log_file.write (str(data) + "\n")

                    except:
                            print("Id %s: Upload failed.. check network connections or incorrect Device ID or GDM URL" % ID)
                            data =str(ID) + str( ": Upload failed, check network connections or incorrect Device ID or incorrect GDM URL" )+ str(" , ")
                            log_file.write (str(data) + "\n")
                            time.sleep(5)#if upload failed then wait 
                            continue
                            break

                db.close()
                time.sleep(5)
                continue

           except:
               	   print"Exception occurs."
              	   data =str( "Exception occurs in main loop while uploading") + str(" , ") +  str(time.strftime("%Y-%m-%d %H:%M:%S"))
              	   log_file.write (str(data) + "\n")
              	   time.sleep(10)
              	   continue
