from jinja2 import  Template
import json
import time

infor = {"id":"id","start_time":15645645,"end_time":464654,"tor_address":"asd4f54.onio",
         "site_name":"site_name","ip_address":"127.0.0.1","country":"国家",
         "servie_type":"bbs","client_ip":"ip who find","path":["relay ip 1","relay ip 2"],
         "clients":["client1","client2","client3"],"stream_id":"stream_id","circ_id":["1","2","3","4"],
         "details":"details"}

class traceReport:
    content = ""
    template=""
    def __init__(self):
        file = open("trace.md","rb")
        self.content = file.read().decode("utf-8")
        self.template = Template(content)
        file.close()

    def trace2md(body):
        #infor = json.loads(body)
        infor = body
        infor["start_time"]=time.asctime(time.localtime(float(infor["start_time"])))
        infor["end_time"]=time.asctime(time.localtime(float(infor["end_time"])))
        outfileInfor = template.render()


temp = traceReport()
temp.trace2md(infor)
