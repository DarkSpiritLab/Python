#"btcAddr"  ->    addresses.append({"addr":"1C1mCxRukix1KfegAY5zQQJV7samAciZpv","onio":"onio","user":"username"})
#result.append({"monitor":{},"tx":{}})  ->    "btcResult"

import jinja2
import  pika
import json

rabbitMqServerIP = "10.11.49.71"
rabbitMqServerPort = 5672

username ="test"
password = "test"

credentials = pika.PlainCredentials(username,password)
connection = pika.BlockingConnection(pika.ConnectionParameters(rabbitMqServerIP,rabbitMqServerPort,'/',credentials))
channel= connection.channel()
channel.queue_declare(queue="btcResult")


def btc2md(body):
	infor = json.loads(body)
	coin_type = "BTC"
	receive_account = infor["monitor"]["addr"]
	onion_site = infor["monitor"]["onio"]
	username = infor["monitor"]["username"]



for method_fram,properties,body in channel.consume("btcAddr"):
        btc2md(body)
        channel.basic_ack(delivery_tag = method_fram.delivery_tag)

requeued_messages = channel.cancle()
print ('Requeued %i messages' %requeued_messages)
 connection.close()



