#!/usr/bin/env python
# /* -*-  indent-tabs-mode:t; tab-width: 8; c-basic-offset: 8  -*- */
# /*

# ******************************************************

# Chris Glomb
# Exam 1
# 9/30/14

# this code uses the hubo-simple-demo-python as the base

# ******************************************************

import hubo_ach as ha
import ach
import sys
import time
import math
from ctypes import *

# Open Hubo-Ach feed-forward and feed-back (reference and state) channels
s = ach.Channel(ha.HUBO_CHAN_STATE_NAME)
r = ach.Channel(ha.HUBO_CHAN_REF_NAME)
#s.flush()
#r.flush()

# feed-forward will now be refered to as "state"
state = ha.HUBO_STATE()

# feed-back will now be refered to as "ref"
ref = ha.HUBO_REF()


def SimSleep(ts, Ts):
	t = ts + Ts
	s.get(state, wait=False, last=False)	
	while(state.time < t):
		s.get(state, wait=True, last=False)
	return
# SimSleep


x = 0
y = 0
t = 0
i = 0
shift = 14

# shift weight to right foot
while i < shift:
	s.get(state, wait=False, last=False)
	x += 0.01
	ref.ref[ha.RHR] = x
	ref.ref[ha.LHR] = x
	ref.ref[ha.RAR] = -x
	ref.ref[ha.LAR] = -x
	r.put(ref)
	#print x
	i += 1
	SimSleep(state.time, 0.1)

# lift left leg
x = 0
i = 0
while i < 10:
	s.get(state, wait=False, last=False)
	x += 0.1
	ref.ref[ha.LHP] = -x
        ref.ref[ha.LKN] = 2*x
        ref.ref[ha.LAP] = -x
	r.put(ref)
	#print x
	i += 1
	SimSleep(state.time, 0.1)

s.get(state, wait=False, last=False)
SimSleep(state.time, 0.3)

# crouching right leg
x = 0
i = 0
#y = state.time
while i < 40:
	s.get(state, wait=False, last=False)
	x = 0.4*(1 + math.cos((math.pi + i*0.1*math.pi))) # vertical movement
	h = ((shift*0.01) + ((x/6)*0.15)) # hip shift to cancel out horizontal sway
	ref.ref[ha.LHR] = h
	ref.ref[ha.RHR] = h
	ref.ref[ha.LAR] = -h
	ref.ref[ha.RAR] = -h
	ref.ref[ha.RHP] = -x
        ref.ref[ha.RKN] = 2*x
        ref.ref[ha.RAP] = -x
        r.put(ref)
        #print "i = " + str(i) + ", x = " + str(x)
	i += 1
	SimSleep(state.time, 0.1)
#print state.time - y

s.get(state, wait=False, last=False)
SimSleep(state.time, 0.3)

# left leg down
x = 1
i = 0
while i < 10:
	s.get(state, wait=False, last=False)
	x -= 0.1
	ref.ref[ha.LHP] = -x
        ref.ref[ha.LKN] = 2*x
        ref.ref[ha.LAP] = -x
	r.put(ref)
	#print x
	i += 1
	SimSleep(state.time, 0.1)

s.get(state, wait=False, last=False)
SimSleep(state.time, 0.3)

# shift weight to left foot
#x = .14
x = 0
i = 0
#while i < 2*shift:
while i < shift:
	s.get(state, wait=False, last=False)
	x -= 0.01
	ref.ref[ha.RHR] = x
	ref.ref[ha.LHR] = x
	ref.ref[ha.RAR] = -x
	ref.ref[ha.LAR] = -x
	r.put(ref)
	#print x
	i += 1
	SimSleep(state.time, 0.1)


# lift right leg
x = 0
i = 0
while i < 4:
	s.get(state, wait=False, last=False)
	x += 0.1
	ref.ref[ha.RHP] = -x
        ref.ref[ha.RKN] = 2*x
        ref.ref[ha.RAP] = -x
	r.put(ref)
	#print x
	i += 1
	SimSleep(state.time, 0.1)

s.get(state, wait=False, last=False)
SimSleep(state.time, 0.3)

# parallel to ground pose
x = 0
i = 0
while i < 40:
	s.get(state, wait=False, last=False)
	x += 0.03
	ref.ref[ha.RHP] = -.4 + .1*x
	ref.ref[ha.LHP] = -x
        #ref.ref[ha.LKN] = 2*x
        ref.ref[ha.LAP] = .1*x
	r.put(ref)
	#print x
	i += 1
	SimSleep(state.time, 0.1)
	
s.get(state, wait=False, last=False)
SimSleep(state.time, 0.3)
	
# crouching left leg
x = 0
i = 0
#y = state.time
while i < 40:
	s.get(state, wait=False, last=False)
	x = 0.2*(1 + math.cos((math.pi + i*0.1*math.pi))) # vertical movement
	h = ((shift*0.01) + ((x/6)*0.15)) # hip shift to cancel out horizontal sway
	ref.ref[ha.LHR] = -h
	ref.ref[ha.RHR] = -h
	ref.ref[ha.LAR] = h
	ref.ref[ha.RAR] = h
	ref.ref[ha.RHP] = -.28 + x
	ref.ref[ha.LHP] = -1.2 - x
        ref.ref[ha.LKN] = 2*x
        ref.ref[ha.LAP] = .12 - x
        r.put(ref)
        #print "i = " + str(i) + ", x = " + str(x)
	i += 1
	SimSleep(state.time, 0.1)

# stand back up
x = 1.2
i = 0
while i < 40:
	s.get(state, wait=False, last=False)
	x -= 0.03
	ref.ref[ha.RHP] = -.4 + .1*x
	ref.ref[ha.LHP] = -x
        #ref.ref[ha.LKN] = 2*x
        ref.ref[ha.LAP] = .1*x
	r.put(ref)
	#print x
	i += 1
	SimSleep(state.time, 0.1)
	
# right leg down
x = .4
i = 0
while i < 4:
	s.get(state, wait=False, last=False)
	x -= 0.1
	ref.ref[ha.RHP] = -x
        ref.ref[ha.RKN] = 2*x
        ref.ref[ha.RAP] = -x
	r.put(ref)
	#print x
	i += 1
	SimSleep(state.time, 0.1)

# shift weight to center
x = -.14
i = 0
while i < shift:
	s.get(state, wait=False, last=False)
	x += 0.01
	ref.ref[ha.RHR] = x
	ref.ref[ha.LHR] = x
	ref.ref[ha.RAR] = -x
	ref.ref[ha.LAR] = -x
	r.put(ref)
	#print x
	i += 1
	SimSleep(state.time, 0.1)


# Close the connection to the channels
r.close()
s.close()
