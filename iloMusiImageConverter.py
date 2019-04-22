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

def processImageBlock(imageBlockData):
	imageName = imageBlockData[0]
	imageData = []
	imageWidth = len(imageBlockData[1].strip()[1:-1])
	for line in imageBlockData[2:-1]:
		imageData.append(line[1:imageWidth+1])
		if len(line.strip()) != imageWidth+2:
			print('WARNING: Wrong image width detected in the following line:\n{}'.format(line))
	#TODO: process imageName and imageData
	imageHeight = ((len(imageData)+7)//8)*8

	for i in range(len(imageData), imageHeight):
		imageData.append(' '*imageWidth)
	#Calculate the bytes representing the image right here
	imageArray = []
	for i in range(imageWidth):
		nextValue = 0
		for j in range(imageHeight):
			k = j%8
			if k == 0:
				nextValue = 0
			value = 1 if imageData[j][i] != ' ' else 0
			nextValue += value * (2**k)
			if k == 7:
				imageArray.append(nextValue)

	if imageName[0] == '>':
		with open(imageName[1:], 'wb') as f:
			f.write(bytes([imageWidth, imageHeight]))
			f.write(bytes(imageArray))
	else:
		print('uint8_t {}[] = {{{}}};'.format(imageName, ''.join(['{}, '.format(hex(i)) for i in imageArray])))
		print('.imageHeight={}; .imageWidth={};'.format(imageHeight, imageWidth))
	#If imageName has a > prefix, it's to be written to a file
	#Otherwise, it's to be written as a variable
	#TODO: what about the width and height of the image? hmm. maybe store it right at the beginning? or at the end? I don't know.

with open(sys.argv[1], 'r') as inputFile:
	lookingForCharacter = True
	imageBlockData = []
	for line in inputFile.readlines():
		line = line.replace('\n', '')
		if lookingForCharacter:
			if len(line.strip()) != 0:
				lookingForCharacter = False
				imageBlockData = []
		if not lookingForCharacter:
			if line.strip() == 'END':
				lookingForCharacter = True
				processImageBlock(imageBlockData)
			else:
				imageBlockData.append(line)

