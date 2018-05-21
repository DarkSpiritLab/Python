import pika
import json
import sys

rabbitMqServerIP = "222.20.73.252"
rabbitMqServerPort = 5672

username ="dark"
password = "darkGenius"

credentialsSend = pika.PlainCredentials(username,password)
connectionSend = pika.BlockingConnection(pika.ConnectionParameters(rabbitMqServerIP,rabbitMqServerPort,'/',credentialsSend))
channelSend = connectionSend.channel()
channelSend.queue_declare(queue="btcAddr")

btcAddr = {"addr":str(sys.argv[1]),"onio":"testOnio.onio","user":"testUserName"}
infor = json.dumps(btcAddr)

channelSend.basic_publish(exchange='', routing_key='btcAddr', body=infor)

connectionSend.close()
