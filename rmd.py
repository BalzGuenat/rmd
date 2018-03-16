#!/usr/bin/python3

# Copyright @ Balz Guenat 2018

import requests as rq
import json
import sys
import argparse
import locale

VERSION = '0.2'

WRITE_DEBUG_FILES = False

defaultApiUrl = 'http://localhost:8001'

def fetch(mdFilePath, args=None):
	if not args:
		args = vars(parser.parse_args([mdFilePath]))

	with open(mdFilePath, 'br') as dataFile:
		dataStr = dataFile.read()
		if WRITE_DEBUG_FILES:
			with open('rmdin.md', 'bw') as f:
				f.write(dataStr)
		dataJson = json.dumps({'text': dataStr.decode(), 'mode': 'markdown'})
		return rq.post(args['url'], data = dataJson).text


parser = argparse.ArgumentParser(description='Remote Markdown - Compile markdown by calling APIs.')
parser.add_argument('-o', '--output', metavar='outfile', dest='outfile',
                    help='Write the output to outfile')
parser.add_argument('-url', metavar='url', dest='url',
					default=defaultApiUrl,
                    help='The URL to send the API call to.')
parser.add_argument('--version', action='version', version='%(prog)s {}'.format(VERSION))
parser.add_argument('infile', metavar='FILE',
					help='The input markdown file.')

def rmd(args):
	if type(args) is str:
		args = [args]
	args = vars(parser.parse_args(args))
	return fetch(args['infile'], args)

if __name__ == "__main__":
	args = vars(parser.parse_args())
	text = fetch(args['infile'], args)
	if WRITE_DEBUG_FILES:
		with open('rmdout.html', 'bw') as f:
			f.write(text.encode())
	if 'outfile' in args and args['outfile']:
		with open(args['outfile'], 'bw') as outFile:
			outFile.write(text.encode())
	else:
		sys.stdout.buffer.write((text.encode(locale.getpreferredencoding())))
