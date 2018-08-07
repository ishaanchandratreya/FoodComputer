import paho.mqtt.client as mqtt
import time
import sqlite3
import json

global conf_GDM_URL
global conf_PiIdentifier
global conf_ControlSensorForTriggerDeviceId


with open('/home/pi/transfer/Final_init_ControlEnv.py/myconfig.json') as data_file:
        global conf_GDM_URL
        global conf_PiIdentifier
        global conf_ControlSensorForTriggerDeviceId
        jsonData = json.load(data_file)
        conf_GDM_URL = jsonData["GDM_URL"]
        conf_PiIdentifier = jsonData["PiIdentifier"]
        conf_ControlSensorForTriggerDeviceId = jsonData["ControlSensorForTriggerDeviceId"]
print conf_GDM_URL
print conf_PiIdentifier

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, rc):
    try:
        print("Connected with result code "+str(rc))

        if(rc==0):
            print("Connection successfull")
            # Subscribing in on_connect() means that if we lose the connection and
            # reconnect then subscriptions will be renewed.
            client.subscribe(conf_PiIdentifier)
            print("Subsription to topic successfull,now waiting for trigger from GDM")
        else:
            print("Connection unsuccessfull,please check Device ID is correct to receive trigger")
            time.sleep(10)

    except:
        print("Exception occurs while connecting and scribing the topic")


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    try:
        print "\nTopic: "+ msg.topic+"\nMessage: "+str(msg.payload) + "\nTimestamp: " + str(time.strftime("%Y-%m-%d %H:%M:%S"))

        #Inserting data in database
        #Connecting database,inserting data, commit changes and closing database connection
        db = sqlite3.connect('/home/pi/transfer/Final_init_ControlEnv.py/DatabaseControlled.db') #Connecting database
        cursor = db.cursor() #Creating cursor object

        message = str(msg.payload)
        TriggerList=message.splitlines()

        for i in TriggerList:
            #Executing insert queries
            cursor.execute("INSERT INTO SensorControl( SensorDeviceId, AlertAction, IsActive , CreatedDate, ModifiedDate ) VALUES (?,?,?,?,?)",
                 ( str(conf_ControlSensorForTriggerDeviceId), str(i) , str("1") , str(time.strftime("%Y-%m-%d %H:%M:%S")), str(time.strftime("%Y-%m-%d %H:%M:%S"))   ))
            db.commit() #Commit changes


        db.close() #closing database
        print("Trigger inserted in table successfully.")

    except:
        print("Exception occurs while inserting trigger in database,please ensure that database and tables are created correctly.")




while(True):
    try:
        client = mqtt.client(conf_ControlSensorForTriggerDeviceId)
        client.on_connect = on_connect
        client.on_message = on_message
        client.connect(conf_GDM_URL, 1883, 60)

        # Blocking call that processes network traffic, dispatches callbacks and
        # handles reconnecting.
        # Other loop*() functions are available that give a threaded interface and a
        # manual interface.
        client.loop_forever()

    except:
        print("Exception occurs in main loop, please check GDM URL and GDM must be in running state")
        time.sleep(10)
        continue

