import requests, zipfile, json, os, io


def create_folders():
    pass

def UPDATER_START():
    with open("data.json", 'r') as file:
        data = json.load(file)
    dest = "../"
    anchor = data['github']['raw_link']
    folders = data['content']['folders']
    files = data['content']['files']