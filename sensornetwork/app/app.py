import paho.mqtt.client as mqtt
import json
import time
import datetime
import csv


# Visualiza los registros que se realizan
def on_log(client, userdata, level, buf):
    print("log: ",buf)

# Establece conexion al broker MQTT, Subscribirse en el topico especificado
def on_connect(client, userdata, flags, rc):
    #connected
    print("Conectado")
    client.subscribe(topic='sensores2', qos=2)

    
client = mqtt.Client()
client.on_connect = on_connect
client.on_log = on_log
client.connect('mqttserver', 1883)


with open('dataset.csv') as csvFile:
    csvReader = csv.DictReader(csvFile)
    tempHour = ''
    for csvRow in csvReader:
        data = {}
        data['dateTime'] = csvRow['datetime']
        data['idStation'] = csvRow['clave_estacion']
        data['mediciones'] = []
        parameters = ['RH','TMP','WDR','WSP','CO','NO','NO2','NOX','O3','PM10','PM2.5','PMCO','SO2']
        for param in parameters:
            medicion = {
                "idParametro": param,
                "valor": csvRow[param]
            }
            data['mediciones'].append(medicion)
        data = json.dumps(data)
        print(data)
        if (tempHour != csvRow['hora']):
            time.sleep(5)
            print('CHANGE HOUR')
        client.publish('sensores2', data)
        tempHour = csvRow['hora']