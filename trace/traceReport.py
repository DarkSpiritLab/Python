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
    response = request.urlopen(url)
    infor=response.read().decode("utf8")
    inforJson = json.loads(infor)
    inforJson=inforJson["data"]
    strLocal = ""
    if inforJson["country"] != "XX":
        strLocal += inforJson["country"]
    if inforJson["region"] != "XX":
        strLocal += inforJson["region"]
    if inforJson["city"] != "XX":
        strLocal += inforJson["city"]
    if strLocal == "":
        strLocal = "未知"
    return strLocal

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
        return outfileInfor


temp = traceReport()
x = json.dumps(infor)
with open("result.md","wb") as f:
    infor =temp.trace2md(x)
    f.write(infor.encode("utf8"))
