#!usr/bin/python
import datetime
import sqlite3

#reads time and puts into list
def readTime():
	#sets date and time into seperate attributes
	year = datetime.datetime.now().strftime("%Y-%m-%d")
	time = datetime.datetime.now().strftime("%H-%M-%S")
	
	#create list
	logList = [year, time]

	#return list
	return logList

#records time into db and displats table
def logTime():
	#takes list from readTime()
	dateList=readTime()

	#sets connection with database
	conn = sqlite3.connect('/home/pi/testTime.db')
	conn.text_factory = str
	curs = conn.cursor()
	
	#inserts data from list
	curs.execute("""INSERT INTO testTime VALUES (?,?)""", (dateList[0],dateList[1]))

	#commits changes
	conn.commit()
	
	#displays database table
	for row in curs.execute("""SELECT * FROM testTime"""):
		print row
	
	conn.close()
#runs logTime()
logTime()
 
