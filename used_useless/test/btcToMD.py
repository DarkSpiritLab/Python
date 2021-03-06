from jinja2 import  Template
import json

import urllib
import urllib2


file = open("btc.md","rb")
content = file.read().decode("utf-8")
template = Template(content)

def currencySearch(value , time):
    url = "https://blockchain.info/frombtc?value="+str(value)+"&currency=CNY&time="+str(time)+"000"
    req = urllib2.Request(url)
    infor = urllib2.urlopen(req).read()
    return infor


def btc2md(body):
    infor = json.loads(body)
    coin_type = "BTC"
    receive_account = infor["monitor"]["addr"]
    onion_site = infor["monitor"]["onio"]
    username = infor["monitor"]["user"]#change from username to user
    send_amount = infor["amount"]
    tx = infor["tx"]
    time = tx["time"]
    currency = currencySearch(send_amount,time)
    size =tx["size"]
    output_accounts = list()
    in_amount=0
    out_amount = 0
    for i in tx["out"]:
        output_accounts.append(i["addr"])
        out_amount = out_amount + i["value"]
    input_accounts = list()
    #for i in tx["inputs"]:
    #    if not i["witness"]:
    #        input_accounts.append(i["prev_out"]["addr"])
    #        in_amount = in_amount+i["prev_out"]["value"]
    for i in tx["inputs"]:
        input_accounts.append(i["prev_out"]["addr"])
        in_amount = in_amount+i["prev_out"]["value"]
    hash = tx["hash"]
    weight=tx["weight"]
    fees=in_amount-out_amount
    block_height=infor["height"]
    block_time=tx["time"]
    url=tx["hash"]
    tx_id = infor["tx_index"]
    outfileInfor = template.render(coin_type=coin_type,receive_account=receive_account,onion_site=onion_site,username=username,send_amount=send_amount,time=time,currency=currency,size=size,output_accounts=output_accounts,input_accounts=input_accounts,hash=hash,recv_amount=in_amount,weight=weight,fees=fees,block_height=block_height,block_time=block_time,url=url,tx_id=tx_id)
    outfile = open(hash+"_"+str(time)+".md","wb")
    print "MD : "+hash  # +"\n INFOR:\n"+outfileInfor
    outfile.write(outfileInfor.encode("utf-8"))
    outfile.close()

testFile = open("btcInfoTest.json","rb")
testContent = testFile.read().decode("utf-8")
btc2md(testContent)






