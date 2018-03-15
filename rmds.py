#!/usr/bin/python3

import http.server as srv
import json
import subprocess
import os


cp = subprocess.run(['pandoc', '--version'], stdout=subprocess.PIPE)
pandocVersion = cp.stdout.decode().split('\n')[0].split(' ')[1]

def readLine(bytes):
	s = ''
	while True:
		s = s + bytes.read(1).decode()
		if s.endswith('\r\n'):
			return s
			
def readChunks(bytes):
	length = int('0x' + readLine(bytes)[:-2], 16)
	while length != 0:
		# print("chunk length = " + str(length))
		chunk = bytes.read(length).decode()
		bytes.read(2) # consume \r\n after chunk
		# print(chunk)
		yield chunk
		length = int('0x' + readLine(bytes)[:-2], 16)
	# print("last chunk detected")
	
def readChunked(bytes):
	s = ''
	for chunk in readChunks(bytes):
		s = s + chunk
	return s

class MarkdownServer(srv.BaseHTTPRequestHandler):
	def do_POST(self):
		# if self.headers['Content-type'] != ''
		encodingHeader = self.headers['Transfer-Encoding']
		if encodingHeader and encodingHeader.split(',').contains('chunked'):
			print('content is chunked')
			postData = readChunked(self.rfile)
		else:
			contentLength = int(self.headers['Content-length'])
			postData = self.rfile.read(contentLength)

		# print(self.requestline)
		# contentLength = int('0x' + self.rfile.read(2).decode(), 16)
		# print(self.headers)
		# postData = json.load(self.rfile)
		
		# contentLength = 2
		# postData = self.rfile.read(contentLength + 6).decode()
		
		print(postData.decode().encode('UTF-8'))
		if self.headers['Content-type'] and 'text/markdown' in self.headers['Content-type']:
			text = postData
		else:
			text = json.loads(postData)['text'].encode()
		with open('out2.html', 'bw') as outFile:
			outFile.write(text)
		# subprocess.run(['echo', r'%cd%'])
		cp = subprocess.run(['pandoc', '-c', os.path.realpath('github.css'), '--self-contained'], input=text, stdout=subprocess.PIPE)
		self.send_response(200)
		self.send_header('Content-type', 'text/html; charset=utf-8')
		self.send_header('Content-length', len(cp.stdout))
		self.send_header('Pandoc-version', pandocVersion)
		self.end_headers()
		with open('out.html', 'w') as outFile:
			outFile.write(cp.stdout.decode())
		self.wfile.write(cp.stdout)
		# self.wfile.write(b'<html><body>')
		# self.wfile.write(text.encode())
		# self.wfile.write(self.rfile.read())
		# self.wfile.write(b'</body></html>')
		# self.wfile.write(eof)
	def do_GET(self):
		self.send_response(200)
		self.send_header('Content-type', 'text/html')
		self.end_headers()
		self.wfile.write(b'Try POST.')
	
def run():
	httpd = srv.HTTPServer(('localhost', 8001), MarkdownServer)
	httpd.serve_forever()

print('Starting Markdown Server...')
print('pandoc version = {}'.format(pandocVersion))
run()
