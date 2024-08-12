import requests, zipfile, json, os, io

def UPDATER_START():
    with open("data.json", 'r') as file:
        data = json.load(file)
    dest = "../"
    github = data['github']
    folders = data['content']['folders']
    files = data['content']['files']