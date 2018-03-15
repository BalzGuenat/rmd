#!/usr/bin/python3

import requests as rq
import json
import sys

dataFilePath = 'notes.md'
outFilePath = 'notes.html'
# apiUrl = 'https://api.github.com/markdown'
apiUrl = 'http://localhost:8001'

def go():
	with open(dataFilePath, 'r') as dataFile, open(outFilePath, 'w') as outFile:
		dataStr = dataFile.read()
		dataJson = json.dumps({'text': dataStr, 'mode': 'markdown'})
		r = rq.post(apiUrl, data = dataJson)
		outFile.write(r.text)
		print(r.text)
		return r
