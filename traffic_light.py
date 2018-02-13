class Light(object):
	COLORS = ('GREEN', 'YELLOW','RED')
	ALERT_SIG = 'YELLOW'

	"""Class represents a traffic light"""
	def __init__(self, id):
		self._id = id
		self._sig = "" #traffic light is off

	def signal_set(self, signal):
		assert (signal in self.COLORS), "Light assert: invalid signal"

		self._sig = signal

	def signal_get(self):
		return self._sig

	def id_get(self):
		return self._id

	def turn_off(self):
		self._sig = ""

	def alert(self):
		assert (self.ALERT_SIG in self.COLORS), "Light assert: invalid alert signal"

		if (ALERT_SIG != self._sig):
			self._sig = ALERT_SIG
		else:
			self._sig = ""

