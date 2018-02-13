import time

from traffic_light import Light
from traffic_ctrl import Ctrl
from traffic_light import Light

class Plc(object):
	'traffic light PLC'
	STAT_OK1 = 'ok (a1 u. a3 - go  , a2 u. a4 - stop)'
	STAT_OK2 = 'ok (a1 u. a3 - Stop, a2 u. a4 - go  )'
	STAT_EMCY = 'emcy'
	STAT_DOWN = 'shutdown'
	STARTUP_TIME = 15
	CYCLE_TIME = 1

	def __init__(self):
	""" init PLC """
		self._ctl_a13 = Ctrl((Light(a1), Light(a3))
		self._ctl_a24 = Ctrl((Light(a2), Light(a4))
		self._monitor = Monitor([self._ctl_a13, self._ctl_a24])
		self._status = STAT_OK1
		self._busy = False
		
		self.traffic_ctrl('LC_ON', 'LC_ON', 'LS_RED', 'LS_RED')

		time.sleep(STARTUP_TIME)

	def update(self):
	""" PLC thread to control traffic """

		#critical region start...
		self._busy = True
 
		if (STAT_OK1 == self._status):
			self._status = STAT_OK2
			self._busy = False
			#...critical region finish

			self.traffic_ctrl('LC_GO', 'LC_STOP', 'LS_GREEN', 'LS_RED')
 
		elif (STAT_OK2 == self._status):
			self._status = STAT_OK1
			self._busy = False
			#...critical region finish

			self.traffic_ctrl('LC_STOP', 'LC_GO', 'LS_RED', 'LS_GREEN')

		elif (STAT_EMCY == self._status):
			self._busy = False
			#...critical region finish

			self.traffic_ctrl('LC_ALERT', 'LC_ALERT', 'LS_EMCY', 'LS_EMCY')

		elif (STAT_DOWN == self._status):
			self._busy = False
			#...critical region finish

			self.traffic_ctrl('LC_OFF', 'LC_OFF', 'LS_OFF', 'LS_OFF')

		else:
			self._monitor.update(self._status)
		

	def emergency(self):
		if not self._busy: #protect critical region (must be executed atomar)
			self._status = STAT_EMCY

	def shutdown(self):
		if not self._busy: #protect critical region (must be executed atomar)
			self._status = STAT_DOWN

	def traffic_ctrl(self, cond_a13, cond_a24, result_a13, result_a24):
		a13_finished = False
		a24_finished = False
		
		while not (a13_finished and a24_finished): 
			self._ctl_a13.update(cond_a13)
			self._ctl_a24.update(cond_a24)
			self._monitor.update(self._status)

			if result_a13 == self._ctl_a13.state_get() : a13_finished = True
			if result_a24 == self._ctl_a24.state_get() : a24_finished = True

			time.sleep(CYCLE_TIME) #PLC sleeps for each steps and gives cpu back for other tasks

