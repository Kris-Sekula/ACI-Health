#!/usr/bin/env python
# 
#
#  For debugging we use the bottom left corner pixel and:
#
# 					show red dot if failed to get data
# 					show blue dot if failed to refresh the cookie.
#					show orange when we start refreshing data.
#					show yellow when login fails.
#
#
# ver 1.1 added dispaly of ip address on boot in binary format. 
#
#


import time
import json
import requests
import time
import unicornhat as unicorn
import urllib3
import socket
import commands

urllib3.disable_warnings()

unicorn.set_layout(unicorn.PHAT)
unicorn.rotation(180)
unicorn.brightness(0.4)
height,width=unicorn.get_shape()


#  login details for your APIC

apic = '10.50.138.215'
username = 'aci-health'
password = 'aci-health'



# show blue pixels in each corner
def show_icon(timedel):	
	unicorn.set_pixel(0,0,0,0,255)
	unicorn.set_pixel(0,3,0,0,255)
	unicorn.set_pixel(7,0,0,0,255)
	unicorn.set_pixel(7,3,0,0,255)
	unicorn.show()
	time.sleep(timedel)



# show ipv4 address in binary on the 4x8 LEDs 
def show_ip(timedel):
	for address in filter(None, commands.getoutput("hostname -I").split(" ")):
		show_icon(1)
		try:
			print "processing:  ",address
			for octetidx,octet in enumerate(address.split(".")):
				bin_octet="{0:08b}".format(int(octet))
				for idx,c in enumerate(bin_octet[::-1]):
					if c == "0":
						unicorn.set_pixel(idx,octetidx,0,255,0)
					elif c == "1":
						unicorn.set_pixel(idx,octetidx,255,0,0)
			print "display: ", address
			unicorn.show()
			time.sleep(timedel)
		except:
			print "skip ipv6"
			pass
		unicorn.clear()
		unicorn.show()
	return()

# some colour defs
red=(255,0,0)
orange=(255,128,0)
green=(0,255,0)

#
# get data from APIC function
#
def getdata():

	url='https://%s/api/node/mo/topology/health.json' % apic

	try:	
		print "Getting data from APIC...",apic
		response = requests.get(url,cookies=cook,timeout=2,verify=False)
		json_data = response.json()
		health = json_data["imdata"][0]["fabricHealthTotal"]["attributes"]["cur"]
		print "currnet health score is",health
		show_unicorn(int(health))
		print "\n---------------\n"
    	except:
		unicorn.clear()
		unicorn.set_pixel(0,0,255,0,0)
		unicorn.show()
		print "Missing health data, or timeout"
		pass
	return()

#
# refresh session cookie
#

def refreshSession(oldcook):
	url = 'https://%s/api/aaaRefresh.json' % apic
	print "\n---------------\n"
	r = None
	while r is None:
		try:
			r = requests.get(url, cookies=oldcook,timeout=10,verify=False)
			newcook = r.cookies
			print "got a new cookie"
			print "\n---------------\n"
		except:
			unicorn.clear()
			unicorn.set_pixel(0,0,0,0,255)
			unicorn.show()
			print "timeout refreshing cookie"
			print "\n---------------\n"
			newcook = loginAPIC()
			pass
	return(newcook)

#
#  display the health score
#

def show_unicorn(health):
	if health == 100:
		colour=green
       		level=8
	elif 90 <= health <= 99:
        	colour=green
        	level=7
	elif 60 <= health <= 89:
        	colour=orange
        	level=6
	elif 50 <= health <= 59:
        	colour=orange
        	level=5
	elif 30 <= health <= 49:
        	colour=orange
        	level=4
	elif 20 <= health <= 29:
        	colour=red
        	level=2
	else:
        	colour=red
        	level=1
	
	print "level",level
	print "colour",colour

        for y in range(level):
                for x in range(width):
                        r=colour[0]
                        g=colour[1]
                        b=colour[2]
                        unicorn.set_pixel(y,x,r,g,b)
                unicorn.show()
		time.sleep(0.05)
	return()

def loginAPIC():
	headers={'content-type':'application/json'}
	auth = {'aaaUser': {'attributes': {'name':username,'pwd':password}}}	
	url = 'https://%s/api/aaaLogin.json' % apic
	r = None
	while r is None:
        	try:
                	r = requests.post( url, data=json.dumps(auth), timeout=5, verify=False )
                	print "logging in, status ",r.status_code
                	cook = r.cookies
        	except:
                	unicorn.clear()
                	unicorn.set_pixel(0,0,255,255,0)
                	unicorn.show()
                	print "timeout logging in, but we will keep trying"
			show_ip(5)
                	pass
	
	return(cook)

# --------------------------------------------------------------------------
# Main program loop starts here
# --------------------------------------------------------------------------

print "Stared monitorig script..."

show_icon(1)

print "waiting for network"

while len(filter(None, commands.getoutput("hostname -I").split(" "))) < 1:
	print "Waiting for at least 1 ip"

print "got an ip address"

# show ip addresses for 10s (1s delay between if more IPs found)

show_ip(10)

# Perform initial login, later we will need to refresh the cookie frequently

cook = loginAPIC()

while True:
	for num in range(0,8):
		unicorn.clear()
		unicorn.set_pixel(0,0,255,128,0)
		unicorn.show()
		getdata()
		time.sleep(5)
	print "Refreshing cookie"
	cook = refreshSession(cook)
