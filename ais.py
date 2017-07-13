#author Christopher Millar 

from bs4 import BeautifulSoup
import urllib2
import re
from compiler.ast import flatten
import time
from datetime import datetime
start_time = datetime.now()

#Gathers AIS data from a selected port 
#Data contains MMSI, Name of Ship, Latitude, Longitude, Heading, Course Over Ground, Speed Over Ground, Size, ETA, Last Update Time (Full Timestamp)  
#Can upload to database, write to file or intergrate into the back end with jython

def checkList(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]

while True:
	#storing mmsi data 
	my_list4 =[]
	
	#selected port
	website = "http://www.aishub.net/source-statistics.php?source=2313&sname=Broadstairs,%20Kent"  

	web = urllib2.urlopen(website).read()  #whole page 
	soup = BeautifulSoup(web, "html.parser")

	#find number of pages of data 
	data = soup.find_all('table', attrs={'style':'margin-bottom: 5px;'})
	data =  str(data).split(">",7)[6] 
	numberOfPages =  str(data).split("<",1)[0] 
	numberOfPages = int(numberOfPages)/10

	#loop for getting mmsis from data table
	#range is number of pages in table colleted from  
	for i in range(1,numberOfPages):
		my_list=[]
		my_list2 =[]

		#which port location 
		website = "http://www.aishub.net/source-statistics.php?source=2313&sname=Broadstairs,%20Kent&page=" + str(i) 

		web = urllib2.urlopen(website).read()  #whole page 
		soup = BeautifulSoup(web, "html.parser")
		
		#find MMSIS	
		pattern = '[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]' 
		for match in re.findall(pattern, str(soup)):
			 my_list.append(match)
			

		#delete duplicate MMSIS, waste of time and data to include 
		lines_seen = set() # holds lines already seen
		outfile = my_list2
		for line in my_list:
			if line not in lines_seen: # not a duplicate
				my_list2.append(line)
				lines_seen.add(line)
		
		#limit to 10 MMSIS on page 
		my_list3 =[]
		k = 0
		while(k < 10):
			j = my_list2[k]
			my_list3.append(j)
			k+=1
			continue
		my_list4.append(my_list3)

	#make list 1d and remove duplicates
	my_list4 = flatten(my_list4)
	my_list4 = checkList(my_list4)

	#store AIS data values 
	mmsi = my_list4
	latitude=[]
	longitude =[]
	sizeX1=[]
	sizeY1 =[]
	time=[]
	sog=[]
	heading=[]
	cog=[]
	eta=[]
	name=[]
	
	#gathers AIS data from the mmsis of ships
	for MMSI in my_list4:
		website = "http://www.aishub.net/ais-hub-vessel-information.php?mmsi=" +str(MMSI)  

		web = urllib2.urlopen(website).read()  #whole page 
		soup = BeautifulSoup(web, "html.parser")
				
		patternLA = '[5][0-9][.][0-9][0-9][0-9]*'

		for match in re.findall(patternLA, str(soup)):
			try:
				latitude.append(match)
			except IndexError:
				continue

		l =[]
		lo1=[]
		
		lng=[]
		longitude1=[]
		for row in soup.find_all('tr'):
			for col in row.find_all('td'):
				l.append(col)
		longpat1 = '[L][O][N][G][I][T][U][D][E][:].*'
		longpat2 = '[-]?[0-9]+[.][0-9]+'

		for match in re.findall(longpat1, str(l)):
			lng.append(match)
		
		for match in re.findall(longpat2, str(lng)):
			longitude1.append(match)
			
		try:
			longitude.append(longitude1[0])	
		except IndexError:
			continue
			
		sizeX = []
		sizeY =[]
			
		patternSI = '[0-9]*[\s][x]'

		for match in re.findall(patternSI, str(l)):
			try:
				sizeX.append(match)
			except IndexError:
				continue
			 
		patternSI1 = '[x][\s][0-9]+'

		for match in re.findall(patternSI1, str(l)):
			try:
				sizeY.append(match)
			except IndexError:
				continue
				 
		strX = str(sizeX)
		strY = str(sizeY)

		patternNUM = '[0-9]+'

		for match in re.findall(patternNUM, strX):
			 sizeX1.append(match)
			 
		for match in re.findall(patternNUM, strY):
			 sizeY1.append(match)
		time1=[]
		
		
		timepat = '[L][A][S][T][\s][U][P][D][A][T][E][:].*'
		timepat2 = '[0-9][0-0[-][0-9][0-9][-][0-9]*[\s][0-9]+[:][0-9]+'

		for match in re.findall(timepat, str(l)):
			try:
				time1.append(match)
			except IndexError:
				continue
		
		for match in re.findall(timepat2, str(time1)):
			try:
				time.append(match)
			except IndexError:
				continue		
		
		sog1=[]
	
		patternSOG = '[S][O][G][:].*'
		patternSOG2 = '[0-9]+[.]?[0-9]?[\s][k][n]'

		for match in re.findall(patternSOG, str(soup)):
			try:
				sog1.append(match)
			except IndexError:
				continue
		for match in re.findall(patternSOG2, str(sog1)):
			try:
				sog.append(match)
			except IndexError:
				continue		
				
		head1=[]
		
		patternHEAD = '[0-9]+'

		for match in re.findall(patternHEAD, str(l)):
			try:
				head1.append(match)
			except IndexError:
				continue
		try:
			heading.append(head1[-1])
		except IndexError:
			continue	
		
		cog1=[]
		
		patternCOG = '[C][O][G][:].*'
		patternCOG2 = '[0-9]+[.]?[0-9]?'

		for match in re.findall(patternCOG, str(soup)):
			try:
				cog1.append(match)
			except IndexError:
				continue
		
		for match in re.findall(patternCOG2, str(cog1)):
			try:
				cog.append(match)
			except IndexError:
				continue
		eta1=[]
		etapat = '[E][T][A][:].*'
		etapat2 = '[0-9]+[-][0-9]+[\s][0-9]+[:][0-9]+'

		for match in re.findall(etapat, str(l)):
			try:
				eta1.append(match)
			except IndexError:
				continue
		
		for match in re.findall(etapat2, str(eta1)):
			try:
				eta.append(match)
			except IndexError:
				continue
		
		nameIncludingTag = soup.find('h1', {'style': 'margin-bottom: 25px;'})
		nameIncludingTag2 =  str(nameIncludingTag).split(">",3)[2] 
		try:
				name.append(str(nameIncludingTag2).split("<",1)[0])		
		except IndexError:
			continue
		
	#print all data 
		
	print "mmsis of ships: number = " +  str(len(mmsi))		
	print mmsi
				
	print "Number of name values in list: " + str(len(name))
	print name 
				
	print "Number of latitude values in list: " + str(len(latitude))
	print latitude
			 
	print "Number of longitude values in list: " + str(len(longitude))		 
	print longitude	
	 
	print "Number of last update time values in list: " + str(len(time))
	print time

	print "Number of ETA values in list: " + str(len(eta))
	print eta

	print "Number of size X values in list: " + str(len(sizeX1))
	print sizeX1

	print "Number of size Y values in list: " + str(len(sizeY1))
	print sizeY1
		
	print "Number of COG values in list: " + str(len(cog))
	print cog

	print "Number of SOG values in list: " + str(len(sog))
	print sog

	print "Number of heading values in list: " + str(len(heading))
	print heading 

	end_time = datetime.now()
	print('Duration: {}'.format(end_time - start_time))	