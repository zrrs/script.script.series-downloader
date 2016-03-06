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
from downloader.downloaderfactory import *
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

#Donwloader options
app = config.get("Downloader","app")
ip = config.get("Downloader","ip")
downuser = config.get("Downloader","user")
downpass = base64.b64decode(config.get("Downloader","password"))
port = config.get("Downloader","port")

#Last execution
lastMonth = config.get("Last","month")
#We now update de month.
actualDate = datetime.date.today()
config.set("Last","month",actualDate.strftime("%Y-%m"))

#we need to know how many months since las execution to review all.
months = 0
if lastMonth:
    lastDate = datetime.datetime.strptime(lastMonth,"%Y-%m").date()
    r =  relativedelta.relativedelta(actualDate, lastDate)
    if r.months:
        months = r.months
    if r.years:
        months = months + 12
else:
    #If this is the first execution we will also look in the previous month
    months = 1

#Creation of the web object
web =  webFactory.createWeb(selected_web,user,password)

#Creation of the torrent object
torrent = torrentFactory.createTorrent(selected_torrent,language,otherFilters,verified,minSize)

#Creation of the downloader object
downloader = downloaderFactory.createDownloader(app,ip,downuser,downpass,port)

#Look for new episodes
episodes = {}
web.getEpisodesForDownload(episodes,months)
#Porcess of the new episodes.
for serie in episodes:    
    print u"Title: ",serie
    for episode in episodes[serie]:
        print u'\tEpisode {episode}'.format(episode=episode["number"])
        episode["torrent"] = torrent.episodeSearch(serie,episode)
        if episode["torrent"]:
            print "\tMandar descargar : {torrent}".format(torrent=episode["torrent"])
            if downloader.download(episode):  
                print "\tTORRENT ID: {id}".format(id=episode["torrentid"])
                web.markEpisode(episode["id"])
        else:
            print "\tERROR: No torrents fo this episode."
            
#we save the new config.
with open('config.ini', 'w') as configfile:    
    config.write(configfile)