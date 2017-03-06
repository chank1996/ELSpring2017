#!/usr/bin/python
import os 
import time
import sqlite3 as mydb 

def readTemp():
	tempfile = open("/sys/bus/w1/devices/28-000006979949/w1_slave")
	tempfile_text = tempfile.read()
	currentTime = time.strftime('%x %X %Z')
	tempfile.close()
	tempC = float(tempfile_text.split("\n")[1].split("t=")[1])/1000
	tempF = tempC*9.0/5.0 + 32.0
	return [currentTime, tempC, tempF]

def logTemp():
	con = mydb.connect('/home/pi/Databases/temp.db')
	with con:
		try:
			[t,C,F] = readTemp()
			print "Current temperature is: %s F" %F
			cur = con.cursor()
			cur.execute('insert into TempData values(?,?,?)',(t,C,F))
			print "Temperature logged"
		except:
			print "Error"

def tempTimer():
	x = 0.0
	while True:
		print x
		if x == 10.0:
			break
		time.sleep(30)		
		logTemp()
		x += 0.5

#print readTemp()
#logTemp()
tempTimer()
