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
import logging
import time
from os import path
#pip install python-dateutil
from dateutil import relativedelta


#----------------------------------------------------------------------
# Loading config
#----------------------------------------------------------------------
FILELOG = path.join(path.dirname(path.realpath(__file__)),'log','seriesDownloader-{fecha}.log').format(fecha=time.strftime('%Y-%m-%d'))

config = configparser.ConfigParser()
config.read('config.ini')

#Debug mode
DEBUGLEVEL = logging.INFO
debug = False
if int(config.get("Debug","debug")) == 1:
    DEBUGLEVEL = logging.DEBUG
    debug = True        
    
    
#Prepare log file.
logging.basicConfig(
    filename = FILELOG,
    format = '%(asctime)-12s;%(process)-5d;%(filename)-15s:%(levelname)-6s;%(message)s',
    level = DEBUGLEVEL,
    )

console = logging.StreamHandler()
console.setLevel(DEBUGLEVEL)
formatter = logging.Formatter('%(asctime)-12s;%(process)-5d;%(filename)-15s:%(levelname)-6s;%(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

logging.debug(u"In mode DEBUG. The config file wont be update.")
    
#Calendar options
selected_web = config.get("Web","selected_web")
user = config.get("Web","user")
password = base64.b64decode(config.get("Web","password"))
filePath = base64.b64decode(config.get("Web","filepath"))

#Torrent options
selected_torrents = config.get("Torrent","selected_torrent").split(',')
language = config.get("Torrent","language")
minSize = config.get("Torrent","min_size")
otherFilters = config.get("Torrent","other_filters")
if config.get("Torrent","verified"):
    verified = True
    
else: 
    verified = False

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
if not debug:
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
web =  webFactory.createWeb(selected_web, user, password, filePath)

#Creation of the torrent object
torrentsList = []
for selected_torrent in selected_torrents:
    logging.debug(u"New torrent object: {}".format(selected_torrent))
        
    torrent = torrentFactory.createTorrent(selected_torrent, language, otherFilters, verified, minSize, debug)
    torrentsList.append(torrent)

#Creation of the downloader object
downloader = downloaderFactory.createDownloader(app,ip,downuser,downpass,port)

#Look for new episodes
episodes = {}
web.getEpisodesForDownload(episodes,months)
#Porcess of the new episodes.
for serie in episodes:    
    logging.info(u"Title: {}".format(serie))
    for episode in episodes[serie]:
        logging.info(u'Episode {episode}'.format(episode=episode["number"]))
        for torrent in torrentsList:
            logging.debug(u"Using: {}".format(torrent.getUrlBase()))
            episode["torrent"] = torrent.episodeSearch(serie,episode)
            if episode["torrent"]:
                logging.debug(u"Mandar descargar : {torrent}".format(torrent=episode["torrent"]))
                if not debug:
                    if downloader.download(episode):  
                        logging.info(u"TORRENT ID: {id}".format(id=episode["torrentid"]))
                        web.markEpisode(episode["id"])
                        
                    else:
                        logging.error(u"No se puso a descargar: {} {}".format(serie, episode["number"]))
                break
                        
            else:
                logging.error("ERROR: No torrents for this episode in {}.".format(torrent.getUrlBase()))
            
#we save the new config.
if not debug:
    with open('config.ini', 'w') as configfile:    
        config.write(configfile)