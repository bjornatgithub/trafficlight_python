import time

from traffic_light import Light
from traffic_ctrl import LightCtrl
from traffic_monitor import Monitor

class Plc(object):
	'traffic light PLC'
	SC_A12_GO = 'ok (a1 u. a3 - go  , a2 u. a4 - stop)'
	SC_A24_GO = 'ok (a1 u. a3 - Stop, a2 u. a4 - go  )'
	SC_EMCY = 'emcy'
	SC_DOWN = 'shutdown'
	SC_UP   = 'start up'
	STARTUP_TIME = 15
	CYCLE_TIME = 1

	def __init__(self):
		""" init PLC """
		self._ctl_a13 = LightCtrl( (Light('a1'), Light('a3')) )
		self._ctl_a24 = LightCtrl( (Light('a2'), Light('a4')) )
		self._monitor = Monitor( [self._ctl_a13, self._ctl_a24] )
		self._scene = ""

	def update(self):
		""" traffic control next SCENE"""
 
		if (self.SC_A12_GO == self._scene):			
			if (True == self.traffic_ctrl('LC_GO', 'LC_STOP', 'LS_GREEN', 'LS_RED')):
				self._scene = self.SC_A24_GO
 
		elif (self.SC_A24_GO == self._scene):
			if (True == self.traffic_ctrl('LC_STOP', 'LC_GO', 'LS_RED', 'LS_GREEN')):
				self._scene = self.SC_A12_GO

		elif (self.SC_EMCY == self._scene):
			self.traffic_ctrl('LC_ALERT', 'LC_ALERT', 'LS_EMCY', 'LS_EMCY')

		elif (self.SC_UP == self._scene):
			if (True == self.traffic_ctrl('LC_ON', 'LC_ON', 'LS_RED', 'LS_RED')):
				self._scene = self.SC_A12_GO

		elif (self.SC_DOWN == self._scene):
			self.traffic_ctrl('LC_OFF', 'LC_OFF', 'LS_OFF', 'LS_OFF')

		else:
			self._monitor.update(self._status)
		
	def start(self):
		self._scene = self.SC_UP

	def emergency(self):
		self._scene = self.SC_EMCY

	def shutdown(self):
		self._scene = self.SC_DOWN

	def ctrls_get(self):
		return [self._ctl_a13, self._ctl_a24]

	def traffic_ctrl(self, cond_a13, cond_a24, result_a13, result_a24):
		self._ctl_a13.update(cond_a13)
		self._ctl_a24.update(cond_a24)
		self._monitor.update(self._scene)

		a13_finished = a24_finished = False
		if result_a13 == self._ctl_a13.state_get() : a13_finished = True
		if result_a24 == self._ctl_a24.state_get() : a24_finished = True 
		
		return a13_finished and a24_finished

