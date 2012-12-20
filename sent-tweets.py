#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Copyright (c) <2012> Ahmad AlTwaijiry <ahmadt@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy of this 
software and associated documentation files (the "Software"), to deal in the Software 
without restriction, including without limitation the rights to use, copy, modify, 
merge, publish, distribute, sublicense, and/or sell copies of the Software, and to 
permit persons to whom the Software is furnished to do so, subject to the following 
conditions:

The above copyright notice and this permission notice shall be included in all 
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR 
A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT 
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF 
CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE 
OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

sender = '441111111111' # Your Mobile (Must be already registered with Whatsapp)
password = 'Zpv31ld1L2zR3456714678888BM=' # Your Whatsapp password (version 2)


##########
# Twitter settings (optional, you don't need to change it)
##########
consumer_key = ''
consumer_secret = ''
access_key = ''
access_secret = ''
include_rts=1 #check https://dev.twitter.com/docs/api/1/get/statuses/user_timeline
exclude_replies=0  #check https://dev.twitter.com/docs/api/1/get/statuses/user_timeline
totalTweets = 3  #check (count) https://dev.twitter.com/docs/api/1/get/statuses/user_timeline



import argparse, sys, os, threading,time,datetime, base64
from twitter import *

from Yowsup.Common.utilities import Utilities
from Yowsup.Common.constants import Constants
from Yowsup.Registration.v1.coderequest import WACodeRequest
from Yowsup.Registration.v1.regrequest import WARegRequest
from Yowsup.Registration.v1.existsrequest import WAExistsRequest
from Yowsup.Registration.v2.existsrequest import WAExistsRequest as WAExistsRequestV2
from Yowsup.Registration.v2.coderequest import WACodeRequest as WACodeRequestV2
from Yowsup.Registration.v2.regrequest import WARegRequest as WARegRequestV2

from WhatsClient import WhatsappWhatsClient


parser = argparse.ArgumentParser(description='Process twitter to whatsapp.')
parser.add_argument('screenname', metavar='screenname',nargs='+',help='twitter screen name')
parser.add_argument('phone', metavar='phone', type=int, nargs='+',help='phone')

args = parser.parse_args()
screenname= args.screenname[0]
phone = str(args.phone[0])
password = base64.b64decode(password)
cachefile = os.path.dirname(os.path.realpath(__file__))+'/cache/'+str(phone) +'.'+ str(screenname)+'.id'


# create twitter API object
#twitter = Twitter(auth = OAuth(access_key, access_secret, consumer_key, consumer_secret),domain="search.twitter.com",api_version='1.1')
twitter = Twitter(auth = OAuth(access_key, access_secret, consumer_key, consumer_secret))


#read cache file for last tweet id
if os.path.isfile(cachefile):
    try:
        f = open(cachefile, "r")
        try:
            since_id = f.readline()
        finally:
            f.close()
    except IOError:
        since_id=1
        pass
else:
    since_id=1


statuses = twitter.statuses.user_timeline(count = totalTweets, screen_name = screenname, trim_user=0, include_rts=include_rts, exclude_replies=exclude_replies, contributor_details=0,since_id=since_id)

since_id = 1 #we use this to save only the last tweet id
for status in statuses:
    if since_id == 1:  #we use this to save only the last tweet id
        since_id = status['id_str']
        try:
            # This will create a new file or **overwrite an existing file**.
            f = open(cachefile, "w")
            try:
                f.write(since_id) # Write a string to a file
            finally:
                f.close()
        except IOError:
            pass
    try:
        tweet =  "%s (@%s):\nRT: %s (@%s):\n%s" % (status["user"]["name"],status["user"]["screen_name"],status["retweeted_status"]["user"]["name"],status["retweeted_status"]["user"]["screen_name"],status["retweeted_status"]["text"])
    except:
        tweet =  "%s (@%s):\n%s" % (status["user"]["name"],status["user"]["screen_name"],status["text"])
        
    tweet = tweet.encode("utf8","ignore")
    wa = WhatsappWhatsClient(phone, tweet, False)
    wa.login(sender, password)


#qsearch =  u"#عاجل"
#statuses = twitter.search(q=qsearch,result_type='popular',rpp='3',include_entities='0')
#for status in statuses["results"]:
#    #print status
#    tweet =  "%s (@%s):\n%s" % (status["from_user_name"],status["from_user"],status["text"])
#    wa = WhatsappWhatsClient(phone, tweet, False)
#    wa.login(sender, password)
