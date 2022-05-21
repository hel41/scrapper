#!/usr/bin/env python
# coding: utf-8

# selenium 4
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By 
import re # regular expressions
import time 
import json
import random
#import logging
#### MQTT ###
from paho.mqtt import client as mqtt_client
from datetime import datetime

options = Options()
options.headless = True
#driver = webdriver.Chrome(service=Service(ChromeDriverManager(cache_valid_range=1).install()),options=options)
url = "http://www.berliner-feuerwehr.de"



broker = '192.168.188.21'
port = 1883
topic = "einsatzzahlen"
client_id = f'python-mqtt-{random.randint(0, 1000)}'
# username = 'emqx'
# password = 'public'

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    # Set Connecting Client ID
    client = mqtt_client.Client(client_id)
    #client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    #client.enable_logger(logger=None)
    return client


def publish(client,data):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S:%f")
    
         #time.sleep(10)  # Intervall bis zur nächsten Nachricht #
    msg = f'{data}'
    result = client.publish(topic, msg)
    
    # result: [0, 1]
    status = result[0]
    if status == 0:
        print(f"{current_time} Send `{msg}` to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")
        

def get_data():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager(cache_valid_range=1).install()),options=options)
    driver.get(url)
    driver.implicitly_wait(3)
    try:
        box = driver.find_element(By.ID, "bfw-ez-data")
        #print(box.text)
    except:
        pass
    einsatz = {}
    try:
        regex = '"[0-9]+"gm'
        data = re.findall('[0-9]+',box.text)
        einsatz ={"Brandbekämpfung": data[3], "Technische Hilfeleistung": data[4], "Rettungsdienst":data[5]}
    except:
        print("NO Response")
        pass
    driver.close()
    return einsatz
def main():
    client = connect_mqtt()
    client.loop()
    while True:
        daten ={}
        daten = get_data()
        if daten:
            #print(daten)
            publish(client,daten)
        
        
        time.sleep(40)
        


if __name__ == "__main__":
     main()



