# -*- coding: utf-8 -*-
#!/usr/bin/python

### IDEA: Get palette instead of dominant colour in order to create a fade effect

from colorthief import ColorThief
import pigpio as gpio
import socket, thread

# Main options
PORT = 5000			# Port to revieve from
RED_PIN = 36		# GPIO PIN for red
GREEN_PIN = 38		# GPIO PIN for green
BLUE_PIN = 40		# GPIO PIN for blue

def ServeClient(clientSocket, addr):
	# Initialize RPI GPIO configuration
	rpi = gpio.pi()

	while True:
		# Receive dominant color
		data = clientSocket.recv(4096)
		if not data: break	# If no new colour is received, break

		# Conver string to RGB touple of ints
		data = data.replace("(", "").replace(")", "").replace(" ", "")
		colours = tuple(map(int, data.split(",")))

		# Check if colours are correct
		for colour in colours:
			if not (0 <= colour <= 255):
				print "[!] ERROR: bad colour format"
				pass

		print colours

		# Write colours to leds
		rpi.set_PWM_dutycycle(RED_PIN, colours[0])		# Set red
		rpi.set_PWM_dutycycle(GREEN_PIN, colours[1])	# Set green
		rpi.set_PWM_dutycycle(BLUE_PIN, colours[2])		# Set blue

def main():
	# Initialize socket configuration
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind(('', PORT))
	s.listen(1)

	# Accept connections from clients and strat a new thread for each of them
	while True:
		conn, addr = s.accept()
		print "[+] Connected by: ", addr
		thread.start_new_thread(ServeClient, (conn, addr))

	socket.close()


if __name__ == '__main__':
	main()
