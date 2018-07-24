#host  insert data into db from rabbitmq

#------coding=utf-8--*---
import json
import MySQLdb
import pika
import time
from rabbitMq import rabbitMQ

rmq= rabbitMQ()

rabbitMqServerIP = rmq.getIP()
rabbitMqServerPort = rmq.getPort()

username =rmq.getUser()
password = rmq.getPassword()

credentials = pika.PlainCredentials(username,password)
connectionRabbitMQ = pika.BlockingConnection(pika.ConnectionParameters(rabbitMqServerIP,rabbitMqServerPort,'/',credentials))
channel = connectionRabbitMQ.channel()
channel.queue_declare(queue="relayInfor")

conn= MySQLdb.connect(
        host='localhost',
        port = 3306,
        user='root',
        passwd='2015huster',
        db ='test',
        )

def isEXSIT(circle_id, next_ip):
    cur = conn.cursor()
    a=cur.execute("select * from relayInfor where next_ip=%s and next_circ_id=%s",(next_ip,circle_id))
    if a == 0:
        cur.execute("insert into relayInfor (next_ip,next_circle_id) values(%s,%s)",(next_ip,circle_id))
    cur.close()

# def insertRelay(infor):
#     isEXSIT(infor["info"]["next_circle_id"],infor["info"]["next_ip"])
#     cur = conn.cursor()
#     cur.execute("update relayInfor set my_ip = "" where next_ip=%s and next_circ_id=%s and time < %s",(,,))
#     cur.close()
#

def insertRelay(infor):
    cur = conn.cursor()
    a=cur.execute("select * from relayInfor where next_ip=%s and next_circ_id=%s and time > %s",(infor["info"]["next_circle_id"],infor["info"]["next_ip"],str(time.time()-6000)))
    if a == 0:
        cur.execute("insert into relayInfor values(%s,%s,%s,%s,%s,%s,%s,%s)",
                    (infor["localIP"],infor["info"]["next_ip"],str(infor["info"]["port"]),str(infor["info"]["last_circ_id"]),
                     str(infor["info"]["next_circ_id"]),str(infor["info"]["direction"]),str(infor["info"]["stream_id"]),
                     str(infor["info"]["is_origin"]),str(time.time()-6000)))
    cur.close()

def insetStream(infor):
    print "un do"


def insertSQL(infor):
    if infor["type"]=="relay":
        insertRelay(infor)
    elif infor["type"]=="streamjoin":
        insetStream(infor)
    else:
        print "error"+infor


# too lazy to do


for method_fram,properties,body in channel.consume("relayInfor"):
    insertSQL(json.loads(body))
    channel.basic_ack(delivery_tag = method_fram.delivery_tag)

conn.commit()
conn.close()
requeued_messages = channel.cancle()
print ('Requeued %i messages' %requeued_messages)
connectionRabbitMQ.close()




