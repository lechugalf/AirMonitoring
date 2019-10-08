import pymongo
import paho.mqtt.client as mqtt
import json
import sys
import ast
import criterios as c
import datetime


# Usar un archivo .json (rangos) como argumento
with open(sys.argv[1]) as f:
    rangos = json.load(f)

# Visualiza los registros que se realizan
def on_log(client, userdata, level, buf):
    print("log: ",buf)

# Establece conexion al broker MQTT, Subscribirse en el topico especificado
def on_connect(client, userdata, flags, rc):
    #connected
    print("Conectado")
    client.subscribe(topic='sensores2', qos=2)

# Recibe publicaciones del topico subscrito
# Verifica el mensaje recibido de mqtt
# Inserta en base de datos
def on_message(client, userdata, message):
    # varificar datos
    verificado = c.verificar(message.payload, rangos)

    #formato de datetime
    dateStr = verificado['dateTime']
    dateFormat = datetime.datetime.strptime(dateStr, "%Y-%m-%d %H:%M:%S")
    
    print(verificado)
    
    #collection.insert_one(ast.literal_eval(verificado))
    collection.insert({
        "idStation": verificado['idStation'],
        "dateTime": dateFormat,
        "mediciones": verificado['mediciones']
    })

# Define un cliente Mongo
mongoClient = pymongo.MongoClient('mongodb://mongodb:27017/')
db = mongoClient.project
collection = db.measurements

# Define un cliente MQTT
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_log = on_log
client.connect('mqttserver', 1883)
client.loop_forever()