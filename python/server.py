
import threading
from time import sleep
from queue import Queue
from flask import Flask
from flask import request, send_file

def get_index_html(color_default="#ffffff"):
	return f"""
		<html>
		<body>
		<form action="/" method="post">
		Select a color: <input type="color" name="newcolor" value="{color_default}">
		<br>
		<input type="submit" value="Go">
		</form>
		</body>
		</html>
	"""

app = Flask(__name__)

payload_sync = b"\xc0"

def awake_loop(queue):
	"""
	Loops constantly to keep awake the device, sending payload_sync every second.
	In queue there are the payloads to be sent
	"""
	print("Loop thread started")
	f = open("/dev/skel2", "wb")
	while True:
		if queue.qsize() > 0:
			cmd = queue.get()
			if type(cmd) == tuple:
				f.write(cmd[0])
				f.flush()
				sleep(0.1)
				f.write(cmd[1])
			else:
				f.write(cmd)
		else:
			f.write(payload_sync)
		f.flush()
		sleep(1.1)


def build_payload(rgb):
	"""
	Receives a color as RGB hex string (e.g. "ff22aa") and returns the payload
	for the first 20 leds, the others are set to black
	"""
	# mysterious header
	header_1 = b"\x4b\x01\x00\x01\x00"
	header_2 = b"\x4b\x02\x00\x01\x00"

	# create payload as GRB instead of RGB, because it wants like so
	payload = bytes.fromhex(rgb[2:4]) + \
		bytes.fromhex(rgb[0:2]) + \
		bytes.fromhex(rgb[4:6])
	payload *= 20

	# pad last 20 leds  
	padding = b"\x00"*(3*20)

	return (header_1+payload+padding, header_2+payload+padding)


@app.route("/", methods = ["POST", "GET"])
def index():
	if request.method == "GET":
		return get_index_html()
	color = request.form["newcolor"]
	print("Received color: ", color)

	payload = build_payload(color[1:])   #[1:] to discard heading '#'
	print(payload)

	global queue_payload
	queue_payload.put(payload)

	return get_index_html(color)


if __name__ == '__main__':
	global queue_payload
	queue_payload = Queue()
	loop_thr = threading.Thread(target=awake_loop, args=(queue_payload, )) 
	loop_thr.start()
	
	app.debug = False
	app.run(host="0.0.0.0", port=5000)
