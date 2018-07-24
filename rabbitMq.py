#!/usr/bin/python
# -*- coding: UTF-8 -*

class rabbitMQ:
    rabbitMqServerIP = "222.20.73.252"
    rabbitMqServerPort = 5672
    username = "dark"
    password = "darkGenius"
    def getIP(self):
        return self.rabbitMqServerIP
    def getPort(self):
        return self.rabbitMqServerPort
    def getUser(self):
        return  self.username
    def getPassword(self):
        return self.password

