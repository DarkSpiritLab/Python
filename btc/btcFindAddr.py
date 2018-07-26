"""
python 3
直接运行，得到最近区块中交易的内容

"""
from urllib import request
import json

url_lastblock = "http://blockchain.info/latestblock"
url_rawblock = "http://blockchain.info/rawblock/"

def searchLastblockHash():
    response = request.urlopen(url_lastblock)
    info = response.read().decode("utf8")
    blockJson = json.loads(info)
    return blockJson["hash"]

def searchTransactionByHash(blockhash):
    response = request.urlopen(url_rawblock+blockhash)
    info = response.read().decode("utf8")
    blockJson = json.loads(info)
    return blockJson

def search():
    lastHash = searchLastblockHash()
    tran = searchTransactionByHash(lastHash)
    tranLists = tran["tx"]
    for i in tranLists:
        if not ( "out" in i):
            break
        outLists = i["out"]
        j = outLists[0]
        if not ("addr" in j):
            continue
        print(j["addr"])

if __name__ == "__main__":
    search()
