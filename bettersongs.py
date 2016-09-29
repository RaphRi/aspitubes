#!/usr/bin/env python
import os,sys
import subprocess

# This script download again too bad quality songs stored in badSongsDirs got from automatic search
# It prompts for each song a correct youtube Url
badSongsDir="mauvais"

def GetBetterSongs(year):
	os.chdir( badSongsDir + '/' + year)
	for song in os.listdir('.'):
		s = os.path.splitext(song)[0]
		print "chanson : %s" % s
		yt = raw_input ("mettez un lien correct (0=ignorer): ")
		if yt != '0':
			cmd= "youtube-dl --extract-audio --audio-format=mp3 --audio-quality=160k -o \"%s.mp4\" http://www.youtube.com/watch?v=%s\n" % (s ,yt)
			subprocess.call(cmd,shell=True)


if __name__ == "__main__":
 GetBetterSongs ( sys.argv[1])
 
