#author Christopher Millar 

from bs4 import BeautifulSoup
import urllib2
import re
from compiler.ast import flatten
import time
from datetime import datetime
start_time = datetime.now()

#gathers AIS data from a port on ships 

#storing mmsi data 
my_list4 =[]

#loop for getting mmsis 
#range is number of pages in table colleted from  
for i in range(1,4):
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
		

	#delete duplicate MMSIS 
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

#make list 1d	
my_list4 = flatten(my_list4)

#store data values 
latitude=[]
longitude =[]
sizeX1=[]
sizeY1 =[]
time=[]
sog=[]
heading=[]
cog=[]
eta=[]
#take longitude and latitude data 
for z in my_list4:
	website = "http://www.aishub.net/ais-hub-vessel-information.php?mmsi=" +str(z)  

	web = urllib2.urlopen(website).read()  #whole page 
	soup = BeautifulSoup(web, "html.parser")
			
	patternLA = '[5][0-9][.][0-9][0-9][0-9]*'

	for match in re.findall(patternLA, str(soup)):
		 latitude.append(match)

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
	longitude.append(longitude1[0])	
	
	sizeX = []
	sizeY =[]
	

			
	patternSI = '[0-9]*[\s][x]'

	for match in re.findall(patternSI, str(l)):
		 sizeX.append(match)
		 
	patternSI1 = '[x][\s][0-9]+'

	for match in re.findall(patternSI1, str(l)):
		 sizeY.append(match)
			 
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
		time1.append(match)
	
	for match in re.findall(timepat2, str(time1)):
		time.append(match)	
	
	
	patternSOG = '[0-9]?[.]?[0-9]+[\s][k][n]'

	for match in re.findall(patternSOG, str(l)):
		sog.append(match)	
		
	head1=[]
	
	
	patternHEAD = '[0-9]+'

	for match in re.findall(patternHEAD, str(l)):
		head1.append(match)
	heading.append(head1[-1])
	
	cog1=[]
	
	patternCOG = '[C][O][G][:].*'
	patternCOG2 = '[0-9]+[.]?[0-9]?'

	for match in re.findall(patternCOG, str(soup)):
		cog1.append(match)
	
	for match in re.findall(patternCOG2, str(cog1)):
		cog.append(match)	
	eta1=[]
	etapat = '[E][T][A][:].*'
	etapat2 = '[0-9]+[-][0-9]+[\s][0-9]+[:][0-9]+'

	for match in re.findall(etapat, str(l)):
		eta1.append(match)
	
	for match in re.findall(etapat2, str(eta1)):
		eta.append(match)			
	
	
#print all data 
	
print "mmsis of ships: number = " +  str(len(my_list4))		
print my_list4
			
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