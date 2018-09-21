import json
import os


def readjson(file):
    with open(os.getcwd() + file) as f:
        data = json.load(f)
        return data


def readtoken():
    tokenjson = readjson(os.path.join("/config", "config.txt"))
    return tokenjson["token"]
