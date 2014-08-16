from bs4 import BeautifulSoup
import requests 														#module to get url
import os

def get_sol_id(problemlink):
	problem=problemlink+'?sort_by=Time&sorting_order=asc&language=All&status=15&Submit=GO'
	url='http://www.codechef.com'+problem

	try:
		r=requests.get(url)

		data=r.text

		soup=BeautifulSoup(data)

		tr=soup.find(class_='kol')

		td=tr.td
		for i in range (0,4):
			td=td.find_next('td')

		time=float(td.string)

		td=td.find_next('td')
		td=td.find_next('td')

		lang=td.string

		if lang=='JAVA':
			lang='.java'
		elif 'C++' in lang:
			lang='.cpp'
		elif 'PYTH' in lang:
			lang='.py'
		elif lang=='C':
			lang='.c'
		else:
			lang='.txt'

		td=td.find_next('td')
		sol_link=td.ul.li.a.get('href')
		return sol_link,lang,time
	except:
		print "Error"
		return

def download(sol_link,lang,path):
	url='http://www.codechef.com'+sol_link

	r=requests.get(url)

	data=r.text

	soup=BeautifulSoup(data)

	file=open(path+lang,'w+')
	ol=soup.ol
	try:
		for li in ol.find_all('li'):
			encoded=li.text.encode('UTF-8')
			file.write(encoded+'\n')
	except:
		print '\t!!!ERROR!!! "solution not public"'
	file.close()

print "Scrapper to download best solution to all problems by a user sorted by time"
print "***Avoid use during any contest.***"
global username
username=raw_input("Username:")					
url='http://www.codechef.com/users/'+username									#url of user profile
r=requests.get(url)				

data=r.text																#gets text of request object

soup=BeautifulSoup(data)												#creates soup object
									
div=soup.select(".profile")[0]											#find div with class profile and save its first element

table=div.table															#1st table in div
table=table.find_next('table')											#switch to required table

tr=table.tr																#1st row in table
for i in range(0,len(list(table.find_all('tr')))-1):					#iterate to reach required row
	tr=tr.find_next('tr')

td=tr.td																#1st td in tr
td=td.find_next('td')													#reach required td

p=td.p 																	#reach para
count=0																	#no. of problems solved in contest
contest=[]																#names of contest problems solved
contestlinks=[]															#contest problems
common=[]																#problems common to practice and contest
file=open('contest.txt','w+')											#save links of contest problems
for i in range(0,len(list(td.find_all("p")))-1):						#iterate through contest problems
	p=p.find_next('p')
	span=p.span
	for link in span.find_all('a'):										#iterate through problems of a contest
		foo=link.get('href')
		contestlinks.append(foo);											
		contest.append((foo.split("/")[3]).split(",")[0])				#save name of problem in contest list
		file.write(foo)													#write link to contest.txt
		file.write('\n')
		count+=1	
file.close()
print 'contests: ',count												

p=td.p 																	#reach para of practice problems
span=p.span
count=0																	#no. of practice problems
practicelinks=[]                          								#links of practice problems
comm=0																	#no. of common problems(practice & contest)
file=open('practice.txt','w+')											#save links of practice problems
for link in span.find_all('a'):											#iterate through every problem link in practice
	foo=(link.get('href').split("/")[2]).split(",")[0]
	if foo not in contest:												#check if problem exists in contest list
		practicelinks.append(link.get('href'))
		file.write(link.get('href'))									#if not then write it to practice.txt
		file.write('\n')
		count+=1
	else :				
		common.append(foo)												#if common, add it to common list
		comm+=1
file.close()
print "practice: ",count

print 'common :',comm

print common

print 'now'

time_contest=[]

if not os.path.exists("contest"):
	os.mkdir("contest",755)
if not os.path.exists("practice"):
	os.mkdir("practice",755)

no=1
print 'Downloading contest solutions...'
for link in contestlinks:
	problem=contest[contestlinks.index(link)]
	sol_link,lang,time=get_sol_id(link)
	time_contest.append(float(time))
	path="contest/"+problem
	print no, problem
	no+=1
	download(sol_link,lang,path)

if(comm!=0):
	print 'Updating common solutions...'
	no=1
	for problem in common:
		path="contest/"+problem
		link='/status/'+problem+','+username
		sol_link,lang,time=get_sol_id(link)
		time_con=time_contest[contest.index(problem)]
		if(time_con>time):
			print no, time, problem
			no+=1
			download(sol_link,lang,path)

print '\nDownloading practice solutions...'
no=1
for link in practicelinks:
	sol_link,lang,time=get_sol_id(link)
	path="practice/"+(link.split("/")[2]).split(",")[0]
	print no, (link.split("/")[2]).split(",")[0]
	no+=1
	download(sol_link,lang,path)

print 'Finished'