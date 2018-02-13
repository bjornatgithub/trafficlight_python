import time

from traffic_plc import Plc

plc = Plc()

plc.start()

while True:
	plc.update()
	time.sleep(3) 
