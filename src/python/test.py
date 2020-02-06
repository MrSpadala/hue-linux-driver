
import threading
from queue import Queue
from time import sleep

f = open("/dev/skel2", "wb")

payload_random = b"\x4b\x02\x00\x01\x00" \
b"\xff\x00\xff\xff\x00\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff" \
b"\xff\x00\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x00\xff\xff\xff" \
b"\xff\xff\xff\xff\x00\xff\xff\xff\x00\xff\xff\xff\x00\xff\xff\xff" \
b"\xff\xff\xff\xff\xff\xff\xff\x00\xff\x00\xff\xff\x00\x00\x00\x00" \
b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00" \
b"\x00\x00\x00\x00\x00\x00\x00\x00"

payload_blue_1 = b"\x4b\x01\x00\x01\x00" + b"\x00\x00\xff"*20 + b"\x00"*(3*20)
payload_blue_2 = b"\x4b\x02\x00\x01\x00" + b"\x00\x00\xff"*20 + b"\x00"*(3*20)
payload_blue = (payload_blue_1, payload_blue_2)

payload_red_1 = b"\x4b\x01\x00\x01\x00" + b"\xff\x00\x00"*20 + b"\x00"*(3*20)
payload_red_2 = b"\x4b\x02\x00\x01\x00" + b"\xff\x00\x00"*20 + b"\x00"*(3*20)
payload_red = (payload_red_1, payload_red_2)

payload_green_1 = b"\x4b\x01\x00\x01\x00" + b"\x00\xff\x00"*20 + b"\x00"*(3*20)
payload_green_2 = b"\x4b\x02\x00\x01\x00" + b"\x00\xff\x00"*20 + b"\x00"*(3*20)
payload_green = (payload_green_1, payload_green_2)

payload_white_1 = b"\x4b\x01\x00\x01\x00" + b"\xff\xff\xff"*20 + b"\x00"*(3*20)
payload_white_2 = b"\x4b\x02\x00\x01\x00" + b"\xff\xff\xff"*20 + b"\x00"*(3*20)
payload_white = (payload_white_1, payload_white_2)

payload_sync = b"\xc0"

def awake_loop(queue):
	while True:
		if queue.qsize() > 0:
			cmd = queue.get()
			if type(cmd) == tuple:
				f.write(cmd[0])
				f.flush()
				sleep(0.2)
				f.write(cmd[1])
			else:
				f.write(cmd)
		else:
			f.write(payload_sync)
		f.flush()
		sleep(1.1)


queue_payload = Queue()

loop_thr = threading.Thread(target=awake_loop, args=(queue_payload, )) 
loop_thr.start()


sleep(2)

def send(cmd):
	queue_payload.put(cmd)





"""
f.write(payload_sync)
f.flush()
sleep(0.8)
f.write(payload_sync)
f.flush()
sleep(0.8)
f.write(payload_sync)
f.flush()
sleep(0.8)
f.write(payload_blue)
"""


