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

# Lets take a look at how we can find edges in signals. We'll print out all the
# rising edges on the clk signal...
sys.stderr.write("rising edges for the clk signal...\n")
t = 0.0
while True:
    # Find the time at which the next rising edge occurs after t.
    t, ok = w.nextEdge("clk", t, posedge=True, negedge=False)

    # If no edge was found, we are done.
    if not ok:
        break
        
    #gets each bit
    answer = (w.signalAt("s0", t)) | (w.signalAt("s1", t) << 1) | (w.signalAt("s2", t) << 2) | (w.signalAt("s3", t) << 3) | (w.signalAt("s4", t) << 4) | (w.signalAt("s5", t) << 5) | (w.signalAt("s6", t) << 6) | (w.signalAt("s7", t) << 7)
    #format bits into hex
    print("{:02x}".format(answer))

    sys.stderr.write("\t* rising edge at time={}\n".format(t))

# Finally, let's try sampling some signals at regular intervals. Well display a
# table with the values of the s0...s3 signals at intervals of 0.001 time
# units.
sys.stderr.write("time\t\ts0\ts1\ts2\ts3\n")
t = 0.0
while True:
    # Note that we can also get the value of a signal by it's sample index.
    # To get the value of the signal 's' at sample index 'i', we could use:
    #
    #    w.data[i][1][s]

    sys.stderr.write("{:2.4f}\t\t{}\t{}\t{}\t{}\n".format(
        t,
        w.signalAt("s0", t),
        w.signalAt("s1", t),
        w.signalAt("s2", t),
        w.signalAt("s3", t)
        )
    )

    t += 0.001

    # If the timestamp is greater than the time at which the final sample
    # was recorded, stop looping.
    if t > w.data[-1][0]:
        break
