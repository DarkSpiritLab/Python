#"btcAddr"  ->    addresses.append({"addr":"1C1mCxRukix1KfegAY5zQQJV7samAciZpv","onio":"onio","user":"username"})
#result.append({"monitor":{},"tx":{}})  ->    "btcResult"
#"btcReport" <- {"fileName":name,"addr":addr,"time":thisTime,"hash":hash,"md":mdInfo}

from jinja2 import  Template
import  pika
import json
import urllib
import time
import urllib2
from rabbitMq import rabbitMQ

rmq= rabbitMQ()

rabbitMqServerIP = rmq.getIP()
rabbitMqServerPort = rmq.getPort()

username =rmq.getUser()
password = rmq.getPassword()

credentials = pika.PlainCredentials(username,password)
connection = pika.BlockingConnection(pika.ConnectionParameters(rabbitMqServerIP,rabbitMqServerPort,'/',credentials))
channel= connection.channel()
channel.queue_declare(queue="btcResult")
channel.basic_qos(prefetch_count=1)
file = open("btc.md","rb")
content = file.read().decode("utf-8")
template = Template(content)

def currencySearch(value , inTime):
    url = "https://blockchain.info/frombtc?value="+str(value)+"&currency=CNY&time="+str(inTime)+"000"
    resultStr = ""
    try:
        req = urllib2.Request(url)
        infor = urllib2.urlopen(req).read()
        resultStr = str(infor)+" CNY"
    except:
        resultStr = str(value)+" sat"
    return resultStr

def  sendReportName(name):
    infor = {"file":name}
    channel.basic_publish(exchange='', routing_key="btcReport", body=json.dumps(infor))

def sendReport(name,addr,hash,thisTime,mdInfo):
    channelSendResult = connection.channel()
    channelSendResult.queue_declare(queue="btcReport")
    infor = {"fileName":name,"addr":addr,"time":thisTime,"hash":hash,"md":mdInfo}
    channelSendResult.basic_publish(exchange='', routing_key="btcReport", body=json.dumps(infor))

def btc2md(body):
    infor = json.loads(body)
    #print infor
    coin_type = "BTC"
    receive_account = infor["monitor"]["addr"]
    onion_site = infor["monitor"]["onio"]
    username = infor["monitor"]["user"]
    send_amount = infor["amount"]
    tx = infor["tx"]
    thisTime = tx["time"]
    strTime = time.asctime(time.localtime(float(thisTime)))
    currency = currencySearch(send_amount,thisTime)
    size =tx["size"]
    output_accounts = list()
    in_amount=0
    out_amount = 0
    for i in tx["out"]:
        if i.has_key("addr"):
            output_accounts.append(i["addr"])
            out_amount = out_amount + i["value"]
    input_accounts = list()
    for i in tx["inputs"]:
        x={}
        #print i
        if i.has_key("prev_out"):
            x=i["prev_out"]
        if x.has_key("addr"):
            input_accounts.append(x["addr"])
        if x.has_key("value"):
            in_amount = in_amount+x["value"]
    hash = tx["hash"]
    weight=tx["weight"]
    fees=in_amount-out_amount
    block_height=infor["height"]
    block_time=tx["time"]
    url=tx["hash"]
    tx_id = infor["tx_index"]
    outfileInfor = template.render(coin_type=coin_type,receive_account=receive_account,onion_site=onion_site,username=username,send_amount=send_amount,time=strTime,currency=currency,size=size,output_accounts=output_accounts,input_accounts=input_accounts,hash=hash,recv_amount=in_amount,weight=weight,fees=fees,block_height=block_height,block_time=block_time,url=url,tx_id=tx_id)
    fileName =receive_account+"_"+hash+"_"+str(thisTime)+".md"
    sendReport(fileName,receive_account,hash,str(thisTime),outfileInfor.encode("utf-8"))
    #outfile = open(fileName,"wb")
    #print fileName
    #sendReportName(fileName)
    #print "MD : "+hash +"\n INFOR:\n"+outfileInfor
    #outfile.write(outfileInfor.encode("utf-8"))
    #outfile.close()



for method_fram,properties,body in channel.consume("btcResult"):
    print "****************\nReceive from RabbitMQ!"
    btc2md(body)
    channel.basic_ack(delivery_tag = method_fram.delivery_tag)

requeued_messages = channel.cancle()
print ('Requeued %i messages' %requeued_messages)
connection.close()



