#!/usr/bin/python
#
# Copyright (C) 2011
#
# Douglas Schilling Landgraf
# Thanks to Marcelo Barbosa for help/tests
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 2 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

import urllib2
import base64
import sys
import feedparser

# Example
URL       = "https://www.google.com/accounts/ClientLogin"

# Note if your username includes the character ".", like USER.NAME use USER%2ENAME
# %40 = @ 

#Example:
#AUTH_DATA = "&Email=dougsland%40mydomain%2Ecom&Passwd=T0pSecreT!&accountType=HOSTED&service=apps"
AUTH_DATA = "&Email=USERNAME%40DOMAIN%2Ecom&Passwd=YOUR_PASSWORD&accountType=HOSTED&service=apps"

TOKEN     = ""

def request_token():

	global TOKEN

	request = urllib2.Request(URL, AUTH_DATA)
	print "Connecting to: " + URL

	request.add_header('Content-Type', 'application/x-www-form-urlencoded')
	request.get_method = lambda: 'POST'

	try:
		ret = urllib2.urlopen(request)
	except urllib2.URLError, e:
		print "%s" %(e)
		sys.exit(-1)

	print "Done!"

	# To see the response from the server 
	response = ret.read()

	# DEBUG
	#print "============="
	#print response
	#print "============="

	TOKEN = response.split("Auth=")[1].strip()

def request_groups():

	global TOKEN 
	request = urllib2.Request("https://apps-apis.google.com/a/feeds/group/2.0/YOURDOMAIN.com")

	login = "GoogleLogin auth=" + TOKEN
	request.add_header("Authorization", login)
	request.add_header('Content-Type', 'application/atom+xml')

	try:
		ret = urllib2.urlopen(request)
	except urllib2.URLError, e:
		print "%s" %(e)
		sys.exit(-1)

	return ret.read()

if __name__ == "__main__":

	request_token()
	xmldata = request_groups()

	print xmldata
