#Utils

import time

def out(message, level):
	if level == 0:
		return
	if level == 1:
		print(message)
		return
	if level == 2:
		print(message)
		time.sleep(1)
