#!/usr/bin/python3

# Copyright @ Balz Guenat 2018

import http.server as srv
import json
import subprocess
import os

VERSION = '0.2'

PORT = 8001
WRITE_DEBUG_FILES = False

cp = subprocess.run(['pandoc', '--version'], stdout=subprocess.PIPE)
pandocVersion = cp.stdout.decode().split('\n')[0].split(' ')[1]

def readLine(bytestream):
	bs = bytestream.read(2)
	while not bs.endswith(b'\r\n'):
		bs = bs + bytestream.read(1)
	return bs
			
def readChunks(bytestream):
	while True:
		length = int(readLine(bytestream), 16)
		if length == 0:
			return
		yield bytestream.read(length)
		bytestream.read(2) # consume \r\n after chunk
	
def readChunked(bytestream):
	s = b''
	for chunk in readChunks(bytestream):
		s = s + chunk
	return s

class MarkdownServer(srv.BaseHTTPRequestHandler):
	def do_POST(self):
		if 'Transfer-Encoding' in self.headers \
		and self.headers['Transfer-Encoding'] \
		and encodingHeader.contains('chunked'):
			print('content is chunked')
			postData = readChunked(self.rfile)
		else:
			contentLength = int(self.headers['Content-length'])
			postData = self.rfile.read(contentLength)
		
		if self.headers['Content-type'] and 'text/markdown' in self.headers['Content-type']:
			text = postData
			title = 'Untitled'
		else:
			jsonData = json.loads(postData)
			text = jsonData['text'].encode()
			title = jsonData['filename'] if 'filename' in jsonData else 'Untitled'

		if WRITE_DEBUG_FILES:
			with open('rmdsin.md', 'bw') as f:
				f.write(text)
		cp = subprocess.run([
			'pandoc', 
			'-c', os.path.realpath('github.css'), '--self-contained', 
			'--metadata', 'pagetitle=\"{}\"'.format(title)
			], input=text, stdout=subprocess.PIPE)
		self.send_response(200)
		self.send_header('Content-type', 'text/html; charset=utf-8')
		self.send_header('Content-length', len(cp.stdout))
		self.send_header('Pandoc-version', pandocVersion)
		self.end_headers()
		if WRITE_DEBUG_FILES:
			with open('rmdsout.html', 'bw') as f:
				f.write(cp.stdout)
		self.wfile.write(cp.stdout)
	def do_GET(self):
		self.send_response(200)
		self.send_header('Content-type', 'text/html')
		self.end_headers()
		self.wfile.write(b'Try POST.')
	
def run():
	httpd = srv.HTTPServer(('localhost', PORT), MarkdownServer)
	httpd.serve_forever()

print('Starting Markdown Server...')
print('pandoc version = {}'.format(pandocVersion))
run()
