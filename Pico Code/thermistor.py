from machine import ADC, Pin
import time
import math
import mqtt
from seecrets import Bananas as wifi
import network
import ubinascii
import urequests as requests
import display as display
import jgamepad as gamepad

token2 = ''
token = ''
baseid = ''

### SETUP ###

adc = ADC(Pin(26))
R1 = 10800 # R Values determined by experimentation
R2 = 7400
t1 = 273.15+22
t2 = 273.15+37
Beta = math.log(R1/R2) * ((t1*t2)/(t2-t1))
invBeta = 1/Beta
adcMax = 65535
invT = 1/298.15


### FUNCTIONS ###

def read_temp():
    K = 1.00 / (invT + invBeta*(math.log(adcMax/adc.read_u16() - 1.00)))
    C = K-273.15
    F = (1.8)*C + 32
    return K,C,F

def connect_wifi(wifi):
    station = network.WLAN(network.STA_IF)
    station.active(True)
    mac = ubinascii.hexlify(network.WLAN().config('mac'),':').decode()
    print("MAC " + mac)
    station.connect(wifi['ssid'],wifi['pass'])
    while not station.isconnected():
        time.sleep(1)
    print('Connection successful')
    print(station.ifconfig())

def whenCalled(topic, msg):
    print((topic.decode(), msg.decode()))
    led.on()
    time.sleep(0.5)
    led.off()

def get_airtable_colour(table_name):
    url = f'https://api.airtable.com/v0/{baseid}/{table_name}?fields[]=Colour'
    auth_token = token
    headers = {'Authorization': f"Bearer {auth_token}","Content-Type":"application/json"}
    try:
        response = requests.get(url, headers=headers)
        data = (response.json())
        Colour = (data['records'][0]['fields']['Colour'])
        if Colour == 'Blue':
            return 'Blue'
        if Colour == 'Green':
            return 'Green'
        if Colour == 'Red':
            return 'Red'
        response.close()
    except Exception as e:
        print("Error:", str(e))

def chuck_jokes():
    url = "https://api.chucknorris.io/jokes/random"
    headers = {"Content-Type":"application/json"}
    button_val = gamepad.check_button()
    if button_val == 'A':
        r= requests.get(url, headers=headers)
        print(r.json()['value'])
        display.display(r.json()['value'])


def main():
    try:
        fred = mqtt.MQTTClient(client_id='MyPico2', server='io.adafruit.com', user='',password='')
        print('Connected')
        fred.connect()
        fred.set_callback(whenCalled)
        print('nexxt')
    except OSError as e:
        print('Failed')
        return
    try:
        while True: #check subscriptions - you might want to do this more often
            K,C,F = read_temp()
            colour = get_airtable_colour('tempData')
            chuck_jokes()
            if colour == 'Blue':
                fred.publish('dinosaurabh/feeds/Units','K')
                fred.publish('dinosaurabh/feeds/temperature',str(K))
                display.display(str(K)+'K')
                send_airtable('Temperatures',str(K))
            if colour == 'Red':
                fred.publish('dinosaurabh/feeds/Units','C')
                fred.publish('dinosaurabh/feeds/temperature',str(C))
                display.display(str(C)+'C')
                send_airtable('Temperatures',str(C))
            if colour =='Green':
                fred.publish('dinosaurabh/feeds/Units','F')
                fred.publish('dinosaurabh/feeds/temperature',str(F))
                display.display(str(F)+'F')
                send_airtable('Temperatures',str(F))
            time.sleep(1)
    except Exception as e:
        print(e)
    finally:
        fred.disconnect()
        print('done')

def send_airtable(table_name,value):
    url = f'https://api.airtable.com/v0/{baseid}/{table_name}'
    auth_token = token
    headers = {'Authorization': f"Bearer {auth_token}","Content-Type":"application/json"}
    data = {"records":[{'fields':{'temperatures':value}}]}
    try:
        response = requests.post(url, json=data,headers=headers)
        response.close()
    except Exception as  e:
        print("Error:", str(e))
    except Exception as e:
        print("Error:", str(e))

### EXECUTION ###

connect_wifi(wifi)
main()
