import urllib2
import csv
from bs4 import BeautifulSoup

url = "http://www.espncricinfo.com/indian-premier-league-2015/engine/series/791129.html"
page = urllib2.urlopen(url).read()
soup = BeautifulSoup(page)

anchors = soup.findAll('a')
lists = []
ipl_lists = {}
year = 2015
name = "ipl_"+str(year)
for i in anchors:
	if(i.getText()=='Scorecard'):	
		lists.append("http://www.espncricinfo.com"+str(i.get('href'))+"?view=pvp")
ipl_lists.update({name:lists})
		

#date = soup.findAll('title')[0].getText().split('|')[0].split(',')[1] + soup.findAll('title')[0].getText().split('|')[0].split(',')[2]  
year = 2015
for ipl_year in sorted(ipl_lists.iterkeys()):
	name =1	
	for match_url in ipl_lists[ipl_year]:
		page = urllib2.urlopen(match_url).read()
		soup = 	BeautifulSoup(page)
		tables = soup.findAll('table')
		batsmen = []
		for i in soup.findAll('caption'):
			batsmen.append(i.getText())
		title = "ipl_"+str(year)+"match"+str(name)	
		match = open((title+".csv"),'wb')
		f = csv.writer(match)
#file.write(date + '\n')
		f.writerow(["Batsman","Bowler","0s","1s","2s","3s","4s","5s","65s","7+","Dismissal","Runs","Balls","SR"])
		for i in tables :
	#file.write(batsmen[tables.index(i)].split("-")[0] + "\n")
			for row in i.findAll('tr')[1:]:
             			batsman_row=batsmen[tables.index(i)].split("-")[0]
	     			col = row.findAll('td')
             			bowler = col[0].getText()
             			zeros = col[1].getText()
             			ones = col[2].getText()
             			twos = col[3].getText()
             			threes = col[4].getText()
             			fours = col[5].getText()
             			fives = col[6].getText()
             			sixes = col[7].getText()
             			sevens = col[8].getText()
             			dismissal = col[9].getText()
             			runs = col[10].getText()
             			balls = col[11].getText()
             			sr = col[12].getText()
             			data = (batsman_row,bowler,zeros,ones,twos,threes,fours,fives,sixes,sevens,dismissal,runs,balls,sr)
             			f.writerow(data)
		name = name+1
