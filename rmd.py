#!/usr/bin/python3

# Copyright @ Balz Guenat 2018

import time
import requests as rq
import json
import sys
import argparse
import locale
from pathlib import Path

VERSION = '0.2'

WRITE_DEBUG_FILES = False

defaultApiUrl = 'http://localhost:8001'

parser = argparse.ArgumentParser(description='Remote Markdown - Compile markdown by calling APIs.')
parser.add_argument('-o', '--output', dest='outfile', help='Write the output to outfile.')
parser.add_argument('-url', default=defaultApiUrl, help='The URL to send the API call to.')
parser.add_argument('-m', '--monitor', action='store_true', help='Continually monitor the input file and rerender if it changes. Requires the watchdog module.')
parser.add_argument('--version', action='version', version='%(prog)s {}'.format(VERSION))
parser.add_argument('infile', metavar='FILE', help='The input markdown file.')

def fetch(mdFilePath, args=None):
	if not args:
		args = vars(parser.parse_args([mdFilePath]))

	mdFilePath = Path(mdFilePath)
	with open(mdFilePath, 'br') as dataFile:
		dataStr = dataFile.read()
		if WRITE_DEBUG_FILES:
			with open('rmdin.md', 'bw') as f:
				f.write(dataStr)
		dataJson = json.dumps({'text': dataStr.decode(), 'mode': 'markdown', 'filename': mdFilePath.name})
		return rq.post(args['url'], data = dataJson).text

def rmd(args):
	if type(args) is str:
		args = [args]
	args = vars(parser.parse_args(args))
	return fetch(args['infile'], args)
	

def monitor(file, args):
	from watchdog.observers import Observer
	from watchdog.events import FileSystemEventHandler

	class FileChangedHandler(FileSystemEventHandler):
		def __init__(self, file, args):
			self.file = file
			self.args = args
		def on_modified(self, event):
			if Path(event.src_path) == Path(file):
				# print('File changed. Rendering...')
				doIt(self.file, self.args)

	o = Observer()
	o.schedule(FileChangedHandler(file, args), str(Path(file).parent))
	o.start()
	# print('Monitoring...')
	try:
		while True:
			time.sleep(1)
	except KeyboardInterrupt:
		# print('Stopping...')
		o.stop()
	o.join()

def doIt(file, args):
	text = fetch(file, args)
	if WRITE_DEBUG_FILES:
		with open('rmdout.html', 'bw') as f:
			f.write(text.encode())
	if 'outfile' in args and args['outfile']:
		with open(args['outfile'], 'bw') as outFile:
			outFile.write(text.encode())
	else:
		sys.stdout.buffer.write((text.encode(locale.getpreferredencoding())))

if __name__ == "__main__":
	args = vars(parser.parse_args())
	if args['monitor']:
		monitor(args['infile'], args)
	else:
		doIt(args['infile'], args)
