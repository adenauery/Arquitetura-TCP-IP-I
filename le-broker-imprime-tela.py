import paho.mqtt.client as mqtt
import json
import time
from datetime import datetime
from datetime import timezone


# Retorno quando um cliente recebe um  CONNACK do Broker, confirmando a subscricao
def on_connect(client, userdata, flags, rc):
    print("Conectado, com o seguinte retorno do Broker: "+str(rc))

# O subscribe fica no on_connect pois, caso perca a conexão ele a renova
# Lembrando que quando usado o #, você está falando que tudo que chegar após a barra do topico, será recebido
    client.subscribe("temp-cp/#")

# Callback responsavel por receber uma mensagem publicada no tópico acima
def on_message(client, userdata, msg):
   print(msg.topic+" "+str(msg.payload))

   try:
      dados_python = json.loads(msg.payload)
      metrica = dados_python['id']
      sensor = dados_python['data']
      data_e_hora_atuais = datetime.now()
      data_e_hora_em_texto = data_e_hora_atuais.strftime("%d/%m/%Y %H:%M:%S")
      print (data_e_hora_em_texto)
      message = metrica + " " + sensor + " " + str(int(time.time())) + "\n"
      print (message)

   except Exception:
      print("Erro na leitura do JSON via Broker MQTT")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Define um usuário e senha para o Broker, se não tem, não use esta linha
client.username_pw_set("eb-06", password="exehda!@#")

# Conecta no MQTT Broker
client.connect("142.47.103.158", 1883)

# Inicia o loop
client.loop_forever()
