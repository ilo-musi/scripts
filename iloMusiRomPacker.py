#!/usr/bin/python3
#Copyright 2019 Wong Cho Ching <https://sadale.net>
#
#Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
#
#1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
#
#2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
#
#THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
import sys

if len(sys.argv) != 3:
	print("Usage: {} [in.csv] [OUT.NMW]".format(sys.argv[0]))
	exit(1)

name = None
author = None
description = None
assetsTable = [None for i in range(256)]

#Loads the csv input file
with open(sys.argv[1], 'r') as assetListFile:
	for i in assetListFile.readlines():
		i = i.replace('\n', '')
		fields = i.split(',', 1)
		fields[0] = fields[0].strip()
		if len(fields) != 2:
			continue
		
		if fields[0] == "NAME":
			name = fields[1].encode('utf-8')
		elif fields[0] == "AUTHOR":
			author = fields[1].encode('utf-8')
		elif fields[0] == "DESCRIPTION":
			description = fields[1].encode('utf-8')
		else:
			if not fields[0].isdigit():
				continue
			if assetsTable[int(fields[0])] != None:
				print('ERROR: Duplicate index {}'.format(int(fields[0])))
				exit(1)
			assetsTable[int(fields[0])] = fields[1]

#Sanitization
if name == None:
	print('ERROR: Attribute "NAME" not defined in the input file')
	exit(1)
elif len(name) > 32:
	print('ERROR: Attribute "NAME" is too long. It has to be shorter than 32 bytes')
	exit(1)

if author == None:
	print('ERROR: Attribute "AUTHOR" not defined in the input file')
	exit(1)
elif len(author) > 32:
	print('ERROR: Attribute "AUTHOR" is too long. It has to be shorter than 32 bytes')
	exit(1)

if description == None:
	print('ERROR: Attribute "DESCRIPTION" not defined in the input file')
	exit(1)
elif len(description) > 256:
	print('ERROR: Attribute "DESCRIPTION" is too long. It has to be shorter than 256 bytes')
	exit(1)

TABLE_ELEMENTS_COUNT = 256
offsetTable = [None for i in range(TABLE_ELEMENTS_COUNT)]
lengthTable = [None for i in range(TABLE_ELEMENTS_COUNT)]
offset = 1024+TABLE_ELEMENTS_COUNT*8
outputHeader = b''
outputContent = b''


#Calculates output content
for i in range(len(assetsTable)):
	offsetTable[i] = offset
	if assetsTable[i] != None:
		if assetsTable[i][0] == '[' and assetsTable[i][-1] == ']':
			fillLength = int(assetsTable[i][1:-1])
			outputContent += b'\0'*(fillLength)
			offset += fillLength
		else:
			for assetFile in assetsTable[i].split(','):
				with open(assetFile, 'rb') as f:
					fileContent = f.read()
					outputContent += fileContent
					offset += len(fileContent)
	lengthTable[i] = offset-offsetTable[i]
	#Pad the sector to 512 bytes. That's because pf_write() only supports write operations that's aligned to 512 bytes.
	if offset%512 != 0:
		nextOffset = (offset//512+1)*512
		outputContent += b'\0'*(nextOffset-offset)
		offset = nextOffset

#Calculates output header
outputHeader += b'\xAD\xD1\xC7'
outputHeader += (0).to_bytes(1, byteorder='little')
outputHeader += name.ljust(32, b'\0')
outputHeader += author.ljust(32, b'\0')
outputHeader += description.ljust(256, b'\0')
outputHeader += b'\0'*(1024-len(outputHeader))
for i in range(TABLE_ELEMENTS_COUNT):
	outputHeader += offsetTable[i].to_bytes(4, byteorder='little')
	outputHeader += lengthTable[i].to_bytes(4, byteorder='little')

#Write to output file
with open(sys.argv[2], 'wb') as f:
	f.write(outputHeader)
	f.write(outputContent)

print('Successfully written to "{}"'.format(sys.argv[2]))
