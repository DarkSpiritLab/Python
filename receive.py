import socket
import sys
import os
import socket
import pika
import json

rabbitMqServerIP = "10.11.49.71"
rabbitMqServerPort = 5672

credentials = pika.PlainCredentials("test","test")
connectionRabbitMQ = pika.BlockingConnection(pika.ConnectionParameters(rabbitMqServerIP,rabbitMqServerPort,'/',credentials))
channel = connectionRabbitMQ.channel()
channel.queue_declare(queue="relayInfor")
localIP = "0.0.0.0"

def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

localIP =get_host_ip()

def sendToRabbitMQ(infor):
    tempJson = json.loads(infor)
    global  localIP
    if localIP == "0.0.0.0":
        localIP = get_host_ip()
    tempJson["localIP"] = localIP
    newBody = json.dumps(tempJson)
    channel.basic_publish(exchange='',routing_key='relayInfor',body=newBody)
    #print infor

server_address = '/home/uds_socket'

# Make sure the socket does not already exist
try:
    os.unlink(server_address)
except OSError:
    if os.path.exists(server_address):
        raise
# Create a UDS socket
sock = socket.socket(socket.AF_UNIX,socket.SOCK_STREAM)
# Bind the socket to the port
#print >>sys.stderr, 'starting up on %s' % server_address
sock.bind(server_address)

# Listen for incoming connections
sock.listen(100)
while True:
    # Wait for a connection
    #print >>sys.stderr, 'waiting for a connection'
    connection, client_address = sock.accept()
    try:
        print >>sys.stderr, 'connection from', client_address
        data = ""
        # Receive the data in small chunks and retransmit it
        while True:
            temp = connection.recv(10000)
            #print >>sys.stderr, 'received "%s"' % data
            data += temp
            if not(temp):
                break
        sendToRabbitMQ(data)
    finally:
        # Clean up the connection
        #print "close la!"
        connection.close()

connectionRabbitMQ.close()
