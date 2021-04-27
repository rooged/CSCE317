# Reused code provided from assignment 1 to read/parse waves.
# My code will be marked below.
# Copyright 2021 Jason Bakos, Philip Conrad, Charles Daniels
#
# Part of the University of South Carolina CSCE317 course materials. Used by
# instructors for test case generators. Do not redistribute.

import sys
import os

###############################################################################

# This block is setup code that loads the utility library for this assignment.
# You shouldn't mess with it unless you know what you are doing.

# this is the directory where our code is (main.py)
code_dir = os.path.split(os.path.abspath(sys.argv[0]))[0]

# this will be ./.. - the project directory
parent_dir = os.path.split(code_dir)[0]

# the python utils live in ../utils/python_utils
python_utils_dir = os.path.join(parent_dir, "utils", "python_utils")

# append this to Python's import path and import it
sys.path.append(python_utils_dir)
from waves import Waves

###############################################################################

# Read in all the data from standard input and parse it.
w = Waves()
w.loadText(sys.stdin.read())

# Display some information about it. We can use sys.stderr.write() to send a
# log message to standard error without it interfering with the data we
# send to standard out for grade.sh to interpret.
sys.stderr.write("read a waves file with {} signals and {} samples\n".format(len(w.signals()), w.samples()))
sys.stderr.write("input has these signals:\n")
for s in w.signals():
	sys.stderr.write("\t* {} ({} bits)\n".format(s, w.sizes[s]))

# Copyright Timothy Gedney Lab 2

#set starting time values
t = 0.0; ok = True

#get initial cpol & cpha values and change posedge & negedge values to match
t, ok = w.nextEdge("sclk", t, posedge = True, negedge = True)
cpol = w.signalAt("cpol", t)
cpha = w.signalAt("cpha", t)
posedge = True; negedge = False
if cpol == 1: posedge = False; negedge = True
if cpha == 1: nedgedge = True

#initialize all required variables
t = 0.0
exchange = 1; N = 0
answer = ""; mosi = ""; miso = ""; value = ""; countN = ""
streamBool = False; streamM = True

#repeat till end of test
while True:
	#get first 8 bits to get address, r/w, and stream
	while exchange < 9:
		t, ok = w.nextEdge("sclk", t, posedge = posedge, negedge = negedge)
		if not ok: break
		if exchange < 7:
			mosi += str(w.signalAt("mosi", t))
		elif exchange == 7:
			if w.signalAt("mosi", t) == 1:
				answer = "WR"
				streamM = True
			else:
				answer = "RD"
				streamM = False
		elif exchange == 8:
			if w.signalAt("mosi", t) == 1 or w.signalAt("miso", t) == 1:
				answer += " STREAM"
				streamBool = True
			else:
				streamBool = False
		exchange += 1
	if not ok: break
	exchange = 1
	
	#add address to answer string
	answer += " {:02x}".format(int(mosi, 2))
	
	#if/else from stream
	if not streamBool:
		#get value if not a stream and print
		while exchange < 9:
			t, ok = w.nextEdge("sclk", t, posedge = posedge, negedge = negedge)
			if not ok: break
			if streamM:
				value += str(w.signalAt("mosi", t))
			else:
				value += str(w.signalAt("miso", t))
			exchange += 1
		if not ok: break
		answer += " {:02x}".format(int(value, 2))
	else:
		#get N value to tell stream length
		while exchange < 9:
			t, ok = w.nextEdge("sclk", t, posedge = posedge, negedge = negedge)
			if not ok: break
			countN += str(w.signalAt("mosi", t))
			exchange += 1
		if not ok: break
		exchange = 1
		N = int(countN, 2)
		
		#get all items from the stream and add them to answer
		while N > 0:
			while exchange < 9:
				t, ok = w.nextEdge("sclk", t, posedge = posedge, negedge = negedge)
				if not ok: break
				if streamM:
					value += str(w.signalAt("mosi", t))
				else:
					value += str(w.signalAt("miso", t))
				exchange += 1
			if not ok: break
			answer += " {:02x}".format(int(value, 2))
			value = ""
			exchange = 1
			N -= 1
		if not ok: break
	
	#reset all variables	
	print(answer)
	answer = ""; mosi = ""; miso = ""; value = ""; countN = ""
	exchange = 1; N = 0
