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

import time, math, sys
import mido

def outputNote(time, note):
	while time > 0:
		print("{},{},".format(time%256, note))
		time -= 256

NO_PAUSE_THRESHOLD = 0.001
lastEventTime = -1
accumulatedTime = 0
noteQueue = [] #assumption: the notes that're held first are released first.

midiFile = mido.MidiFile(sys.argv[1])

trackNumber = int(sys.argv[2]) if len(sys.argv) > 2 else 0
tempo = 500000
for msg in midiFile.tracks[trackNumber]:
	if msg.type in ['note_on', 'note_off']: #note on/off event
		now = time.time()
		deltaTime = now-lastEventTime if lastEventTime != -1 else 0
		lastEventTime = now
	if msg.is_meta and msg.type == 'set_tempo':
		tempo = msg.tempo
	else:
		if msg.type in 'note_on': #note on
			if msg.time != 0:
				outputTime = int(mido.tick2second(msg.time, midiFile.ticks_per_beat, tempo)*100)
				outputNote(outputTime, 255)
			noteQueue.append(msg.note)
		elif msg.type in 'note_off': #note off
			note = noteQueue[0]
			noteQueue = noteQueue[1:]
			outputTime = int(mido.tick2second(msg.time, midiFile.ticks_per_beat, tempo)*100)
			pitchHz = round((2**((note-69)/12))*440)
			pitch = round((math.log2(pitchHz)-5)*32)
			outputNote(outputTime, pitch)
			accumulatedTime = deltaTime-outputTime/100
