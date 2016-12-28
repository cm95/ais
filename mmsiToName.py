#author Christopher Millar 
from bs4 import BeautifulSoup
import urllib2
import re

#return a ships name from mmsi 

mmsi = ["205038000",
"209715000",
"209840000",
"212376000",
"212396000",
"212935000",
"227022800",
"228006800",
"228085000",
"228283700",
"229241000",
"232001040",
"232001060",
"232001470",
"232002785",
"232004784",
"233009000",
"235007880",
"235010500",
"235082716",
"235082717",
"235090599",
"235096859",
"235114599",
"236205000",
"236414000",
"236439000",
"241147000",
"244530000",
"244620571",
"245180000",
"245488000",
"247086800",
"249311000",
"249910000",
"253109000",
"253447000",
"256065000",
"256119000",
"256715000",
"258669000",
"304903000",
"311000500",
"314192000",
"351539000",
"372700000",
"538003481",
"538005139",
"538005773",
"538005920",
"548894000",
"564923000",
"565994000",
"636015421",
"636017052",
"636017435",
"636091012"]
for mmsi in mmsi:
	url ="https://www.vesselfinder.com/vessels?name="+mmsi  

	user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021911 Firefox/3.0.7'

	headers={'User-Agent':user_agent,} 

	request=urllib2.Request(url,None,headers) 
	response = urllib2.urlopen(request)
	data = response.read() 

	soup = BeautifulSoup(data, "lxml")

	table = soup.find("h1", attrs={"class":"subheader"})

	name=[]
	patternLA = '[A-Z]*\w+[\s]*[\<]*'

	for match in re.findall(patternLA, str(table)):
		name.append(match)

	first = name.index("vessels")
	last = name.index("IMO")

	name =(name[first + 1:last])
	str1 = ' '.join(name )
	print str1