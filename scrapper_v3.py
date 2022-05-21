#!/usr/bin/env python
# coding: utf-8


from selenium import webdriver
from selenium.webdriver.chrome import service as Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import re
import random
import json
from paho.mqtt import client as mqtt_client
from datetime import datetime
url = "http://www.berliner-feuerwehr.de"

#chrome driver  
options = Options()
options.headless = True
service = Service.Service(executable_path="driver/chromedriver")  


#### MQTT ###
broker = '192.168.188.32'
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

def data_extract(input_data):
    regex = '"[0-9]+"gm'
    data = re.findall('[0-9]+',input_data)
    einsatz ={"Brandbekämpfung": data[3], "Technische Hilfeleistung": data[4], "Rettungsdienst":data[5]}
    return json.dumps(einsatz, ensure_ascii=False)

def main():
    client = connect_mqtt()
    client.loop_start()

    run = True
    while run:
        try:
            driver = webdriver.Chrome(service=service, options=options)
            driver.get(url=url)
            zahlen_response = driver.find_element(By.ID, "einsatzahlen").text
            driver.close()
            #print(zahlen_response)
            publish(client=client, data=data_extract(zahlen_response))
            #print(time.asctime(), " " , data_extract(zahlen_response))
            time.sleep(60)
            
        except:
            pass



if __name__ == "__main__":
     main()



