import oc
import json

from threading import Thread


def getConfig():
    configFile = open("chrome.json", 'r')
    return json.load(configFile)


config = getConfig()

for p in list(config["profiles"]):
    oc.run(config, p)
    # Thread(target=oc.run, args=(config, p,)).start()
