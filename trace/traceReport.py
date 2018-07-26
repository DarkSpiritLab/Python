from jinja2 import  Template
import json
import time
from urllib import request

infor = {"id":"id","start_time":15645645,"finish_time":464654,"tor_address":"asd4f54.onio",
         "site_name":"site_name","ip_address":"127.0.0.1",
         "service_type":"bbs","client_ip":"ip who find","path":["relay ip 1","relay ip 2"],
         "clients":["client1","client2","client3"],"stream_id":"stream_id","circ_id":["1","2","3","4"],
         "details":"details"}

def getCountry(ip):
    url = "http://ip.taobao.com/service/getIpInfo.php?ip="+str(ip)
    response = request.urlopen(ip)
    infor=response.read()
    infor=infor.decode("utf8")
    infor = json.loads(infor)
    return infor["country"]+infor["region"]

class traceReport:
    content = ""
    template=""
    def __init__(self):
        file = open("trace.md","rb")
        self.content = file.read().decode("utf-8")
        self.template = Template(self.content)
        file.close()
    def trace2md(self,body):
        infor = json.loads(body)
        #infor = body
        infor["country"]=getCountry(infor["ip_address"])
        infor["start_time"]=time.asctime(time.localtime(float(infor["start_time"])))
        infor["finish_time"]=time.asctime(time.localtime(float(infor["finish_time"])))
        outfileInfor = self.template.render(**infor)
        return outfileInfor.encode("utf-8")


temp = traceReport()
x = json.dumps(infor)
print(temp.trace2md(x))
