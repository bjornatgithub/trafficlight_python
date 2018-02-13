import time

from traffic_ctrl import LightCtrl
from traffic_light import Light
from traffic_plc import Plc

#test settings
TC_ALL 	 = False
TC_START = True
TC_OP 	 = False

def tc_traffic_start():

	print 'run tc traffic start...'
	#preperation
	plc = Plc()
	ctrls = plc.ctrls_get()
	lights = []

	for c in ctrls:
		lights.extend(c.lights_get()) 

	#tc
	plc.start()

	#verification
	for l in lights:
		assert ('RED' == l.signal_get()), ("tc traffic start fails for light: %s value is %s", l.id_get(), l.signal_get())

	print 'ok'


def tc_traffic_operate():

	print 'run tc traffic start...'
	#preperation
	plc = Plc()
	ctrls = plc.ctrls_get()
	light_a13 = ctrls[0].lights_get()
	light_a24 = ctrls[1].lights_get()

	for c in ctrls:
		lights.extend(c.lights_get()) 

	plc.start()

	#tc step 1: a1,a3 -> go a2, a4 -> stop
	plc.update()
	
	#tc verify step 1
	for l in light_a13:
		assert ('GREEN' == l.signal_get()), ("tc traffic start fails for light: %s value is %s", l.id_get(), l.signal_get())

	for l in light_a24:
		assert ('RED' == l.signal_get()), ("tc traffic start fails for light: %s value is %s", l.id_get(), l.signal_get())

	#tc step 2: a1,a3 -> stop a2, a4 -> go
	plc.update()
	
	#tc verify step 1
	for l in light_a13:
		assert ('RED' == l.signal_get()), ("tc traffic operation <GO A1/A3> fails for light: %s value is %s", l.id_get(), l.signal_get())

	for l in light_a24:
		assert ('GREEN' == l.signal_get()), ("tc traffic operation <GO A2/A4> fails for light: %s value is %s", l.id_get(), l.signal_get())

	print 'ok'



#main_test...
try:
	if TC_ALL or TC_START: tc_traffic_start()
except AssertionError, a:
	print a

try:
	if TC_ALL or TC_OP: tc_traffic_operate()
except AssertionError, a:
	print a

