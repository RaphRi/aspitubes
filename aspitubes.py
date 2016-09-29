#!/usr/bin/env python

import urllib,urllib2
import StringIO
import sys
import codecs
import os
import subprocess

from HTMLParser import *

class ChartParser(HTMLParser):
'''

'''	
	def __init__(self, tubes):
		HTMLParser.__init__(self)
		self.parseon = False
		self.parselevel = 0
		self.datalevel = 0
		self.auth = ""
		self.title = ""
		self.tubes = tubes
		self.oldtubes = []
	
	def handle_starttag(self, tag, attrs):
		if self.parseon == False:
			for attr in attrs:
				#b572 class is where dongs names are displayed
				#we activate parse
				if "b572" in attr: 
					self.parseon = True
				
		if self.parseon == True:
			if "img" != tag:
				self.parselevel+=1 #increase level each new tag, unless for img tag
			for attr in attrs:
				if "c1_td5" in attr: #the div where data need to be extracted
					self.datalevel =1
			#print "Encountered a start tag: ,level", tag, attrs, self.parselevel

	def handle_endtag(self, tag):
		if self.parseon == True:
			self.parselevel-=1 #decrease tag level each end tag
			#print "Encountered an end tag :", tag, self.parselevel
			if self.parselevel == 0:
				self.parseon = False #disable parsing when first leve closed
    
	def handle_data(self, data):
		'''get author (level1) then title (level2) from data
		add result in tubes list'''
		if self.datalevel == 1:
			#print "Encountered some data  :", data
			self.auth = data.replace('/', '').replace(':',' ').replace('?',' ').replace('"','')
			self.datalevel+= 1
			return
		if self.datalevel ==2:
			#print "Encountered some data  :", data
			self.title = data.replace('/','').replace(':',' ').replace('?',' ').replace('"','')
			song = (self.auth,self.title)
			if not song in self.tubes and not song in self.oldtubes:
				self.tubes.append( (self.auth,self.title) )
			self.datalevel = 0
	
	def getOldTubes(self, year):
		if int(year)<=1984:
			return
			
		'''load Tubes list froom past year to avoid duplicates entries'''
		f = codecs.open( str(int(year)-1) + ".list", 'r', 'utf-8')
		lines = f.readlines()
		f.close()
		for line in lines:
			print "line = ",line
			t = line.split('-')
			self.oldtubes.append( (t[0].strip(), t[1].strip()))
		
	def getTubes():
		return tubes
		
def getCharts(year):
	'''get hits from chartsinfrance.net official best-selling singles since 1984 in France
	
	@parms year: year from which song titles will be extracted'''
	
	tubes = []
	CP = ChartParser(tubes)
	CP.getOldTubes( year )
	print CP.oldtubes
	
	for i in range(1,52): #each page list year and week number
		#print "http://www.chartsinfrance.net/charts/%s%02d/singles.php" % (year[2:4],i)
		resp = urllib2.urlopen("http://www.chartsinfrance.net/charts/%s%02d/singles.php" % (year[2:4],i))
		encoding = resp.headers.getparam('charset')
		htm = resp.read().decode(encoding)
		htm = htm.replace('&','and')
		CP.feed( htm)
		print "nombre tubes : " , len(tubes)
	
	#print "tubes = ",CP.tubes
	#print "oldtubes =", CP.oldtubes
	
	f1 = codecs.open(year+'.list','w','utf-8')
	f2 = codecs.open(year+'.yt','w','utf-8')
	f3 = codecs.open(year+'.sh','w','utf-8')
	subprocess.call('mkdir -p %s' % year,shell=True)
	for tube in CP.tubes:
		print "got %s - %s" %  (tube[0] , tube[1])
		f1.write( "%s - %s\n" % (tube[0] , tube[1]))
		#print year + "/%s-%s.mp3" % (tube[0] , tube[1])
		if os.path.isfile( year + '/%s-%s.mp3' % (tube[0] , tube[1])):
			print "ALready exists ! Ignore"
		else:
			yt = getFirstYTResult( "http://www.youtube.com/results?search_query=%s - %s - HQ" % (tube[0] , tube[1]))
			f2.write( "https://www.youtube.com/watch?v=" + yt + "\n")
			f3.write( "youtube-dl --extract-audio --audio-format=mp3 --audio-quality=160k -o \"%s-%s.mp4\" http://www.youtube.com/watch?v=%s\n" % (tube[0] , tube[1],yt))
	f1.close()
	f2.close()
	f3.close()
	os.chdir( year)
	subprocess.call("sh ../%s.sh" % year,shell=True)

def getFirstYTResult( yt_url):
	'''
	get youtube's first result id of the search url
	@parms: yt_url: Youtube search url
	'''
	
#	print "yt_url",yt_url
	
	#extract search query and quote it
	ys = yt_url
	posq = ys.find("search_query")
	posqe = ys.find("&",posq)
	ys2 = "http://www.youtube.com/results?search_query=%s&search=Search" % urllib.quote(ys[posq+13:posqe-1].encode('utf-8'))
	
#	print ys2
	resp = urllib2.urlopen(ys2)
#	encoding = resp.headers.getparams('charset')
	htm = resp.read()
	resultattr = "data-context-item-id"
	
	posd = htm.find(resultattr)
	posd2 = htm.find("\"", posd)
	pose = htm.find("\"", posd2+1)
	#print "posd : " , posd ,posd2,pose
	ytid = htm[posd2+1:pose]
	#print "ytid=",ytid
	
	if  "video_id" in ytid:
		posd = htm.find(resultattr,pose)
		posd2 = htm.find("\"", posd)
		pose = htm.find("\"", posd2+1)
		ytid = htm[posd2+1:pose]
		
	return ytid		

'''
DEPRECATED
This part used www.lyrics.glob3z.com to get some older hits
Not tested
'''
def getYear( year ):
	'''
	deprectaed
	get year's hit html page from www.lyrics.glob3z.com 
	'''
	resp = urllib2.urlopen('http://www.lyrics.glob3z.com/tubes' + year + '.php')
	htm = resp.read()
	#print htm
	return htmb
	
def getTubeList ( html):
	'''
	Extract hits list from page
	'''
	tl = []
	lines = html.split('\n')
	for line in lines:
		if "viewlyric" in line:
			posd = line.find("viewlyric")
			pose = line.find("\"",posd)
			tl.append( line[posd:pose])
	return tl
	
def getClip( url):
	'''
		returns song's youtube search url
	'''
	resp = urllib2.urlopen('http://www.lyrics.glob3z.com/' + url)
	htm = resp.read()
#	print htm
	posd = htm.find('http://www.youtube.com')
	pose = htm.find('\'',posd)
	pose2 = htm.find('\"',posd)
	youtubeURL = htm[posd: min(pose,pose2)]
	if "search" in youtubeURL:
		pose = htm.find('target' , posd) -2
		#print "pos=",pose,posd
		yt_id= htm[posd:pose]
		ys = getFirstYTResult(yt_id)
	else:
		posd = youtubeURL.find("/v/")
		pose = youtubeURL.find("&")
		ys = youtubeURL[posd+3:pose]
	#print "yt = ",youtubeURL
	#print "ytid=" , yt_id
	return ys
'''
End www.lyrics.glob3z.com part
'''	


	
print __name__
if __name__ == "__main__":
	
	'''tubepage = getYear(sys.argv[1])
	tublist = getTubeList(tubepage)
	f = open(sys.argv[1] + ".dl",'w')
	for t in tublist :
		ytid= getClip(t)
		f.write( "https://www.youtube.com/watch?v=" + ytid + "\n")
	f.close()
	'''
	'''f = open(sys.argv[1] + ".dl",'r')
	content = f.read()
	for l in content:
		print l,
	f.close()
	'''
	
	getCharts(sys.argv[1])
	#print getFirstYTResult("http://www.youtube.com/results?search_query=Claude Barzotti+Beau, J's'rais Jamais Beau&search=Search")
	
