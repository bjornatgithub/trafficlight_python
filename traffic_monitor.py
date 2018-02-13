import os
import time

from traffic_ctrl import LightCtrl
from traffic_light import Light

class Monitor(object):
	'traffic monitor'
	def __init__(self, LightCtrls):
		self._ctrls = LightCtrls

	def update(self, status):
		os.system('cls' if os.name == 'nt' else 'clear')
		print 'traffic monitor...\t ( ', time.asctime(time.localtime(time.time())), ' )\n\n'
		print 'system status: ', status
		
		ctrl_cnt = len(self._ctrls)
		
		print '\n\nnumber of traffic controller: ', ctrl_cnt, '\n'

		for i in range(ctrl_cnt):
			lights = self._ctrls[i].lights_get()

			print '\n controler ', i, ' is in state ', self._ctrls[i].state_get() ,' controls ', len(lights), ' traffic lights\n'

			for l in lights:
				print 'id: ', l.id_get(), ' is ', l.signal_get()

