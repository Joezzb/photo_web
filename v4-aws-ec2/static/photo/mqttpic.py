#from ast import Num
#from pickle import TRUE

# import mqtt package
#from attr import define
import paho.mqtt.client as mqtt

#import time


pic_topic="PICTURE"  # define subscribe topic
pcode=0


# define the topic we want to subscribe
def on_connect(client, userdata, flags, rc):
    print("Connected with result code ")
    client.subscribe(pic_topic)
    

# define the message we want to return
def on_message(client, userdata, message):
    global pcode
    print(f"D {pcode}")
    print(message.topic)
    if (message.topic == pic_topic):
        pcode+=1
        save_payload(message.payload, (str(pcode)+".jpg"))

# define saving picture function   
def save_payload(payload, filename):
    print("Saving file: "+filename)
    f=open(filename, "wb") # 'w' for 'write', 'b' for 'write as binary, not text'
    f.write(payload)
    f.close()	

# define Mqtt address, and password
SERVER = "35.174.5.8"
user_name = "moment"
password = "iot2022"


# assign a client who want to connect to the MQTT broker

client = mqtt.Client(client_id="", clean_session=True, userdata=None, protocol=mqtt.MQTTv311, transport="tcp")

client.on_message= on_message


client.on_connect = on_connect


# use the username and password to connect the MQTT broker
client.username_pw_set(username=user_name, password=password)
print("Connecting...")
client.connect(SERVER, 1883, 30)


# keep connected
client.loop_forever()

 