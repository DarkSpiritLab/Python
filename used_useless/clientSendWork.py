# "clientReceive" -> {"url":"xxx.onio","level":"1,2,3,4,5"}
import pika
import json
from rabbitMq import rabbitMQ

rmq= rabbitMQ()

rabbitMqServerIP = rmq.getIP()
rabbitMqServerPort = rmq.getPort()

username =rmq.getUser()
password = rmq.getPassword()


credentials = pika.PlainCredentials(username,password)
connectionRabbitMQ = pika.BlockingConnection(pika.ConnectionParameters(rabbitMqServerIP,rabbitMqServerPort,'/',credentials))
channel = connectionRabbitMQ.channel()
channel.queue_declare(queue="clientReceive")
infor = {"url":"www.baidu.com","level":"1,2,3,4,5"}
body= json.dumps(infor)
channel.basic_publish(exchange='', routing_key="clientReceive", body=body)
connectionRabbitMQ.close()

