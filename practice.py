from bs4 import BeautifulSoup
import requests 														#module to get url
import os

def get_sol_id(problemlink):
	url='http://www.codechef.com'+problemlink+'?sort_by=Time&sorting_order=asc&language=All&status=15&Submit=GO'
	
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
	except :
		print 'Error'
		return 

def download(sol_link,lang,path):
	url='http://www.codechef.com'+sol_link
	print url
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

print "Scrapper to download most time efficient solution to a practice problem by given user."
print "The info U enter below will be case-sensitive"
global username
username=raw_input("Username:")					

global problem
problem=raw_input("Problem:")

link="/status/"+problem+","+username
try:
	print link
	print "Getting id of solution..."
	sol_link,lang,time=get_sol_id(link)
except :
	print "Unable to find AC solution of given user to the given problem in practice section."
else :
	print "Attempting download..."
	path=problem
	download(sol_link,lang,path)
	print "Success"