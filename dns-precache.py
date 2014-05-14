#! /usr/bin/python
########################################################################
# Downloads top 500 websites list and caches them in dns with dig.
# Copyright (C) 2014  Carl J Smith
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
########################################################################
import os, sys, re, urllib2
########################################################################
def writeFile(fileName,contentToWrite):
	# figure out the file path
	filepath = fileName.split(os.sep)
	filepath.pop()
	filepath = os.sep.join(filepath)
	# check if path exists
	if os.path.exists(filepath):
		try:
			fileObject = open(fileName,'w')
			fileObject.write(contentToWrite)
			fileObject.close()
			print 'Wrote file:',fileName
		except:
			print 'Failed to write file:',fileName
			return False
	else:
		print 'Failed to write file, path:',filepath,'does not exist!'
		return False
########################################################################
def loadFile(fileName):
	try:
		print "Loading :",fileName
		fileObject=open(fileName,'r');
	except:
		print "Failed to load :",fileName
		return False
	fileText=''
	lineCount = 0
	for line in fileObject:
		fileText += line
		sys.stdout.write('Loading line '+str(lineCount)+'...\r')
		lineCount += 1
	print "Finished Loading :",fileName
	fileObject.close()
	if fileText == None:
		return False
	else:
		return fileText
	#if somehow everything fails return fail
	print 'Nothing worked!'
	return False
#####################################################################$#$
def replaceLineInFile(fileName,stringToSearchForInLine,replacementText):
	# open file
	temp = loadFile(fileName).split('\n')
	# if file exists append, if not write
	newFileText = ''
	if temp != False:
		for line in temp:
			if line.find(stringToSearchForInLine) == -1:
				newFileText += line+'\n'
			else:
				if replacementText != '':
					print 'Replacing line:',line
					print 'With:',replacementText
					newFileText += replacementText+'\n'
				else:
					print 'Deleting line:',line
	else:
		return False
	writeFile(fileName,newFileText)
########################################################################
def downloadFile(fileAddress):
	if fileAddress.find('http') == -1:
		print 'ERROR: Address must be http or https!'
		return False 
	try:
		print "Downloading :",fileAddress
		downloadedFileObject = urllib2.urlopen(str(fileAddress))
	except:
		print "Failed to download :",fileAddress
		return False
	lineCount = 0
	fileText = ''
	for line in downloadedFileObject:
		fileText += line
		sys.stdout.write('Loading line '+str(lineCount)+'...\r')
		lineCount+=1
	downloadedFileObject.close()
	print "Finished Loading :",fileAddress
	return fileText
########################################################################
def pullXmlValue(xmlString,valueToPull):
	start = xmlString.find("<"+valueToPull+">")
	if start == -1:
		return False
	start += len("<"+valueToPull+">")
	splitString = xmlString[start:]
	end = splitString.find('</'+valueToPull+'>')
	if end == -1:
		return False
	splitString = splitString[:end]
	return splitString
########################################################################
def downloadFile(fileAddress):
	try:
		print "Downloading :",fileAddress
		downloadedFileObject = urllib2.urlopen(str(fileAddress))
	except:
		print "Failed to download :",fileAddress
		return False
	lineCount = 0
	fileText = ''
	for line in downloadedFileObject:
		fileText += line
		sys.stdout.write('Loading line '+str(lineCount)+'...\r')
		lineCount+=1
	downloadedFileObject.close()
	print "Finished Loading :",fileAddress
	return fileText
########################################################################
# program pulls top 500 websites and caches them into dnsmasq
########################################################################
def updateCache():
	# download top 500 if it does not exist to a config
	data = downloadFile('http://moz.com/top500/domains/csv')
	if data == False:
		print 'ERROR: failed to download domains!'
		return False
	print type(data)
	# clean up the file to show just the domain names
	data = re.sub('.*\,\"','',data)
	data = re.sub('[1234567890,."]{2,50}','',data)
	data = re.sub('/','',data)
	# write the downloaded file
	temp = writeFile('/etc/dns-precache/top500.list',data)
	if temp == True:
		return True
	else:
		print 'ERROR: failed to write config file!'
		return False
	#~ os.system('wget http://moz.com/top500/domains/csv -O /etc/dnsPrecache/top500')
def preCache():
	# this is the main function, the below stuff just figures out command
	# line arguments
	if os.path.exists('/etc/dns-precache/top500.list'):
		data = loadFile('/etc/dns-precache/top500.list')
	else:
		# download top 500 if it does not exist
		updateCache()
		data = loadFile('/etc/dns-precache/top500.list')
	if os.path.exists('/etc/dns-precache/default.list'):
		# load up the default with the downloaded one this makes shure
		# that even if the site is fucked up the cache will still cache 
		# some sites
		temp = loadFile('/etc/dns-precache/default.list')
		if temp == False:
			print 'ERROR: failed to load default.list'
		else:
			# add default list to main list
			data += '\n'+temp
	if data == False:
		print 'File could not be loaded!'
	else:
		# split website into an array for reading
		data = data.split('\n')
		for website in data:
			# if website is not blank and has a . in it eg .com cache it
			if website != '' and (website.find('.') != -1):
				# launch dig to pull sites into the dns cache, use & so all
				# the processes are launched at once (lil hardcore mode)
				os.system('dig '+website+' &')

# use os.system('dig domainname.net') for each site to precache the dns
# precache arguments
defaultRun = True
inputs = ' '.join(sys.argv).replace('--','-').split('-')
for arg in inputs:
	temp = arg.split(' ')
	if ((('h' == temp[0])) or (('help' == temp[0]))):
		defaultRun = False
		print "DNS-Precache does just what it says."
		print "Copyright (C) 2014  Carl J Smith"
		print ""
		print "This program is free software: you can redistribute it and/or modify"
		print "it under the terms of the GNU General Public License as published by"
		print "the Free Software Foundation, either version 3 of the License, or"
		print "(at your option) any later version."
		print ""
		print "This program is distributed in the hope that it will be useful,"
		print "but WITHOUT ANY WARRANTY; without even the implied warranty of"
		print "MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the"
		print "GNU General Public License for more details."
		print ""
		print "You should have received a copy of the GNU General Public License"
		print "along with this program.  If not, see <http://www.gnu.org/licenses/>."
		print "#############################################################"
		print "-h or --help"
		print "    Displays this menu"
		print "-u or --update"
		print "    Download the newest version of the top websites list."
		print '#############################################################'
	elif ((('u' == temp[0])) or (('update' == temp[0]))):
		defaultRun = False
		# update the list by downloading the newest version of top 500
		# websites 
		updateCache()
	elif ((('p' == temp[0])) or (('precache' == temp[0]))):
		defaultRun = False
		# just run the precache procedure
		preCache()
if defaultRun == True:
	# by default build the cache with the already downloaded website 
	# list
	preCache()
