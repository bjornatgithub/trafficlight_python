import sys
import time

from traffic_light import Light

class LightCtrl(object):
	"""Signal Controller for list of traffic lights"""
	LIGHT_STATE = ('LS_OFF', 'LS_RED', 'LS_YELLOW', 'LS_GREEN', 'LS_EMCY')
	LIGHT_COND = ('LC_ON', 'LC_OFF', 'LC_GO', 'LC_STOP')
	LIGHT_EMCY = 'YELLOW'
	LIGHT_TIME = 0.001 #time to ransit from yellos to green or red in ms

	def __init__(self, lights):
		self._lights = lights
		self._state = 'LS_OFF'
		self._time_ms = sys.maxint

		for light in lights:
			light.turn_off()

	def update(self, cond):
		assert (self._state in self.LIGHT_STATE), "LightCtrl assert: invalid light state"
		assert (cond in self.LIGHT_COND), "LightCtrl assert: invalid light condition"
				
		if ('LS_OFF' == self._state):
			self.off_state(cond)

		elif ('LS_RED' == self._state):
			self.red_state(cond)

		elif ('LS_YELLOW' == self._state):
			self.yellow_state(cond)

		elif ('LS_GREEN' == self._state):
			self.green_state(cond)

		elif ('LS_EMCY' == self._state):
			self.emcy_state(cond)
		else:
			raise Exception("LightCtrl exception: invalid state")

	def off_state(self, cond):
		if ('LC_ON' == cond):
			for light in self._lights: light.signal_set('RED')
			self._state = 'LS_RED'

		if ('LC_ALERT' == cond):
			self._state = 'LS_EMCY'

	def red_state(self, cond):
		if ('LC_OFF' == cond) or ('LC_ALERT' == cond):
			for light in self._lights: light.turn_off()
			self._state = 'LS_OFF'

		if ('LC_GO' == cond):
			for light in self._lights: light.signal_set('YELLOW')
			self._state = 'LS_YELLOW'

	def yellow_state(self, cond):
		#timing condition for transition is 3s
		if self.time_expired(self.LIGHT_TIME):

			#after 3s either green or red
			if ('LC_STOP' == cond) or ('LC_OFF' == cond) or ('LC_ALERT' == cond):
				for light in self._lights: light.signal_set('RED')
				self._state = 'LS_RED'

			if ('LC_GO' == cond):
				for light in self._lights: light.signal_set('GREEN')
				self._state = 'LS_GREEN'

	def green_state(self, cond):
		if ('LC_STOP' == cond) or ('LC_OFF' == cond) or ('LC_ALERT' == cond):
			for light in self._lights: light.signal_set('YELLOW')
			self._state = 'LS_YELLOW'

	def emcy_state(self, cond):
		for light in self.lights: light.alert()

		if ('LC_OFF' == cond):
			for light in self._lights: light.turn_off()
			self._state = 'LS_OFF'

	def state_get(self):
		return self._state

	def lights_get(self):
		return self._lights

	def time_expired(self, time_ms):
		if (sys.maxint == self._time_ms):
			self._time_ms = time.clock()

			print time.asctime(time.localtime(time.time()))

			return False
		else:
			time_diff = time.clock() - self._time_ms

			if time_ms < time_diff:
				print time.asctime(time.localtime(time.time()))

				self._time_ms = sys.maxint
				return True
			else:
				return False
