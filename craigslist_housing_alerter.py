#!/bin/python3


### IMPORTS =====================================

import requests 
import time
import re
import os


### CONSTS ======================================

FILENAME = "links.txt"
SOUNDFILE = "alert.mp3"
URL = "https://vancouver.craigslist.org/search/apa?availabilityMode=0&max_price=1800&postal=V6R2J1&search_distance=9&sort=date"
BROWSER = "chromium"
MEDIA_PLAYER = "play -q"


### FUNCTIONS ===================================

# Get with dirty crash prevention
def better_get(url) :
	while 1 :
		try :
			raw = requests.get(url)
			break
		except :
			print("failed to get page, retrying in 5 secs")
			time.sleep(5)
	return raw

# Append to a file
def append_file(filename, data) :
	f = open(filename, 'a+')
	f.write(data)
	f.close()

# read from a file seperated with line breaks
def load_file(filename) :
	f = open(filename, 'r+')
	data = f.read().split("\n")
	f.close()
	return data


### SCRIPT ======================================

# Setup: load previously seen links so we don't open them again
try :
	seen_links = load_file(FILENAME)
except FileNotFoundError :
	seen_links = []
print("Loaded " + str(len(seen_links)) + " links.")

# Main loop: Keep loading the page and checking for new links
while 1 :
	
	# Get page, compile the links list
	print("running...")
	raw_page = better_get(URL).content.decode('utf-8')
	links = list(set(re.findall(r"https.*\/van\/apa\/d.*\.html", raw_page)))
	print("looking at found links (" + str(len(links)) + ")...")

	# Check for new links, add new ones to file
	browser_args = []
	for link in links :
		if link not in seen_links :
			print(">>> NEW LINK: " + link)
			seen_links.append(link)
			append_file(FILENAME, link+"\n")
			browser_args.append(link)

	# Print new links, open them in browser, play alert sound if possible
	if len(browser_args) > 0 :
		command = BROWSER + "".join([" " + a for a in browser_args]) \
			  + " &"
		print ("Found " + str(len(browser_args)) + " new link(s)")
		os.system(command)	
		os.system(MEDIA_PLAYER + " " + SOUNDFILE + " &")
		time.sleep(1)
	print("Currently " + str(len(seen_links)) + " links.")
	print("-----------------------")

	# 1 min delay with slick countdown
	countdown = [i for i in range(1, 61)]
	countdown.reverse()	
	for t in countdown :
		os.system('echo -en "\\r' + str(t) + ' "')
		time.sleep(1)
	print("\n")

