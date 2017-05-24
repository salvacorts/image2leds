#!/usr/bin/python
# -*- coding: utf-8 -*-

### IDEA: Get palette instead of dominant colour to create a fade effect

from colorthief import ColorThief
import os, sys, socket, time

# Main options
PORT = 5000				# Port to revieve from
SERVER = "192.68.1.8"	# Server address
QUALITY = 5				# Quality to get dominant color
DURATION = 10			# Time to sleep before checking again (seconds)

def GetDominantColour():
	dominantColour = -1

	# Get current wallpaper
	wallpaper = os.popen("gsettings get org.gnome.desktop.background picture-uri").read()
	wallpaper = wallpaper.replace("file://", "").replace("'", "").replace("\n", "");

	# Get dominant color from this wallpaper
	try:
		colours = ColorThief(wallpaper)
		dominantColour = colours.get_color(QUALITY)
	except:
		print("[!] CLIENT: Error picking primary color")

	return dominantColour

def main():
	lastdominantColour = "0"

	# Parse arguments
	if len(sys.argv) > 1: end = int(sys.argv[1])
	else: end = -1

	# Initialize socket configuration and connect to server
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		s.connect((SERVER, PORT))
	except:
		print "[!] Error connecting to server. check configuration"

	i = 0;
	while (i != end):
		dominantColour = GetDominantColour()

		if dominantColour != lastdominantColour:
			lastdominantColour = dominantColour
			s.sendall(str(dominantColour))

		time.sleep(DURATION)
		i += 1

	s.close()


if __name__ == '__main__':
	main()
