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

readingCharacterRow = -1 #-1 = looking for first row.

characterData = []
characterOffset = 0
with open('font.txt', 'r') as fontFile:
	characterUnit = 1
	character = [0,0,0,0,0]
	for i in fontFile.readlines():
		i = i.replace('\n', '')
		if readingCharacterRow == -1:
			i = i.strip()
			if len(i) == 0:
				continue
			codePoint = int(i[0:2], 16)
			readingCharacterRow = 0
			character = [0,0,0,0,0]
		else:
			for c in range(5):
				character[c] += (0 if i[c]==' ' else 1)*(2**readingCharacterRow)
			if readingCharacterRow == 7:
				readingCharacterRow = -1
				characterData.append((codePoint, character))
			else:
				readingCharacterRow += 1

characterData = sorted(characterData)
characterDataWithFiller = []
for codePoint in range(characterData[0][0], characterData[-1][0]+1):
	for data in characterData:
		if codePoint == data[0]:
			characterDataWithFiller.append(data)
			break
	else:
		characterDataWithFiller.append((codePoint,[0,0,0,0,0]))

print('const static uint8_t FONT_DATA[][5] = {')
for item in characterDataWithFiller:
	codePoint = item[0]
	data = item[1]
	print('\t{', end='')
	for j in data:
		print('{}, '.format(hex(int(j))), end='')
	print("}}, // {:02x} '{}'".format(codePoint, chr(codePoint)))
print('};')


sys.stderr.write("Code generation completed! Now generating image for the font (requires PIL)...\n")
DOT_SIZE = 10
DOT_MARGIN = 2
import PIL.Image, PIL.ImageDraw
import shutil
import os

OUTPUT_DIR = './generated_images'
if os.path.exists(OUTPUT_DIR):
	shutil.rmtree(OUTPUT_DIR)
os.mkdir(OUTPUT_DIR)
for item in characterData:
	codePoint = item[0]
	data = item[1]
	img = PIL.Image.new( 'RGBA', (5*(DOT_SIZE+DOT_MARGIN),7*(DOT_SIZE+DOT_MARGIN)), "white")
	draw = PIL.ImageDraw.Draw(img)
	for index, row in enumerate(data):
		y = 0
		while y <= 7:
			draw.rectangle(
				(
					(DOT_MARGIN+index*(DOT_SIZE+DOT_MARGIN), DOT_MARGIN+y*(DOT_SIZE+DOT_MARGIN)),
					(DOT_MARGIN+index*(DOT_SIZE+DOT_MARGIN)+DOT_SIZE, DOT_MARGIN+y*(DOT_SIZE+DOT_MARGIN)+DOT_SIZE)
				),
				(0, 0, 0, 255) if row&(1<<y) else (255, 255, 255, 0))
			y += 1
	del draw
	img.save(os.path.join(OUTPUT_DIR, f'0x{codePoint:02x}.png'))
