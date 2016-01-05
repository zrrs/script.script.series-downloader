#! /usr/bin/env python
# -*- encoding: utf-8 -*- 
#-------------------------------------------------------------------------------
# Name:        Series Downloader
# 
# Author:      zrrs
#
# Created:     13/10/2015
#
# ---------------------------------------
# Built-in modules, uncomment if you need.
#
# import xbmc
# import xbmcgui
# import xbmcplugin
# import xbmcaddon
# import xbmcvfs
from web.webfactory import *
from torrent.torrentfactory import *
import configparser
import base64
import datetime
#pip install python-dateutil
from dateutil import relativedelta

#----------------------------------------------------------------------
# Loading config
#----------------------------------------------------------------------
config = configparser.ConfigParser()
config.read('config.ini')

#Calendar options
selected_web = config.get("Web","selected_web")
user = config.get("Web","user")
password = base64.b64decode(config.get("Web","password"))
#Torrent options
selected_torrent = config.get("Torrent","selected_torrent")
language = config.get("Torrent","language")
otherFilters = config.get("Torrent","other_filters")
otherFilters = ' OR '.join(x for x in otherFilters.split("|"))
if config.get("Torrent","verified"):
    verified = True
else: 
    verified = False
minSize = config.get("Torrent","min_size")
#Last execution
lastMonth = config.get("Last","month")
#We now update de month.
actualDate = datetime.date.today()
config.set("Last","month",actualDate.strftime("%Y-%m"))
 #we save the new config.
with open('config.ini', 'w') as configfile:    
    config.write(configfile)

#we need to know how many months since las execution to review all.
months = 0
if lastMonth:
    lastDate = datetime.datetime.strptime(lastMonth,"%Y-%m").date()
    r =  relativedelta.relativedelta(actualDate, lastDate)
    if r.months:
        months = r.months
    if r.years:
        months = months + 12

#Creation of the web object
web =  webFactory.createWeb(selected_web,user,password)
#Creation of the torrent object
torrent = torrentFactory.createTorrent(selected_torrent,language,otherFilters,verified,minSize)
#Look for new episodes
episodes = {}
web.getEpisodesForDownload(episodes,months)
#Porcess of the new episodes.
for serie in episodes:    
    for episode in episodes[serie]:
        print '{tvserie} {episode}'.format(tvserie=serie,episode=episode["number"])
        torrent.episodeSearch(serie,episode)
        #If we have added it to the torrent client, mark as downloaded.
        #web.markEpisode(episode["id"])

