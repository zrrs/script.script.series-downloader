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
from webfactory import *
import configparser
import base64

#----------------------------------------------------------------------
# Variables de configuracion
#----------------------------------------------------------------------
config = configparser.ConfigParser()
config.read('config.ini')

selected_web = config.get("Web","selected_web")
user = config.get("Web","user")
password = base64.b64decode(config.get("Web","password"))


web =  webFactory.createWeb(selected_web,user,password)
episodes = web.getEpisodesForDownload()

print 'Episodes to download:'

for serie in episodes:    
    for episode in episodes[serie]:
        print '\t{tvserie} {episode}'.format(tvserie=serie,episode=episode["number"])
        #web.markEpisode(episode["id"])

