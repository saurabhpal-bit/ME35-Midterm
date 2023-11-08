import requests
import network
import time
import json
import pandas as pd
import random
import sys
import time

# Import Adafruit IO MQTT client.
from Adafruit_IO import MQTTClient

token2 = ''
token = ''
baseid = ''
ADAFRUIT_IO_KEY = ''
ADAFRUIT_IO_USERNAME = ''

def get_airtable_colour(table_name):
    url = f'https://api.airtable.com/v0/{baseid}/{table_name}?fields[]=Colour'
    auth_token = token
    headers = {'Authorization': f"Bearer {auth_token}","Content-Type":"application/json"}
    #params = {'fields[]':'Colour'}
    try:
        response = requests.get(url, headers=headers)
        data = (response.json())
        Colour = (data['records'][0]['fields']['Colour'])
        print(Colour)
        response.close()
    except Exception as e:
        print("Error:", str(e))
    return Colour

def callback(source,user,message):
    print(message.payload.decode())


# Group Name
group_name = 'Default'
group_feed_one = 'Colour2'

def connected(client):
    print('Listening for changes on ', group_name)
    # Subscribe to changes on a group, `group_name`
    client.subscribe_group(group_name)

def disconnected(client):
    # Disconnected function will be called when the client disconnects.
    print('Disconnected from Adafruit IO!')
    sys.exit(1)

def message(client, topic_id, payload):
    # Message function will be called when a subscribed topic has a new value.
    # The topic_id parameter identifies the topic, and the payload parameter has
    # the new value.
    print('Topic {0} received new value: {1}'.format(topic_id, payload))


# Create an MQTT client instance.
client = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

# Setup the callback functions defined above.
client.on_connect    = connected
client.on_disconnect = disconnected
client.on_message    = message

# Connect to the Adafruit IO server.
client.connect()

client.loop_background()

while True:
    value = random.randint(0, 100)
    client.publish(group_feed_one, get_airtable_colour('tempData'), group_name)
    time.sleep(5)
    

client.loop_stop()
client.disconnect()