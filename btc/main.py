#!/usr/bin/env python
#coding: utf-8
import  os


if __name__ == "__main__":
    pid = os.fork()
    if not pid:
        #child
        print("btcToMD start!")
        os.system("python btcToMD.py")
        print("btcToMD end!")
    else:
        #parent
        pid2 = os.fork()
        if not pid2:
            #child
            print("btcSearch end!")
            os.system("python btcSearch.py")
            print("btcToSearch end!")
        else:
            print ("all open")




