#!/usr/bin/python
# -*- coding: UTF-8 -*

class rabbitMQ:
    rabbitMqServerIP = "192.168.181.1"
    rabbitMqServerPort = 5672
    username = "test"
    password = "test"
    def getIP(self):
        return self.rabbitMqServerIP
    def getPort(self):
        return self.rabbitMqServerPort
    def getUser(self):
        return  self.username
    def getPassword(self):
        return self.password

