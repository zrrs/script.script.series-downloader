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

#----------------------------------------------------------------------
# Variables de configuracion
#----------------------------------------------------------------------
config = configparser.ConfigParser()
config.read('config.ini')

#Directorios fuente y destino.
selected_web = config.get("Web","selected_web")
user = config.get("Web","user")
password = config.get("Web","password")


web =  webFactory.createWeb(selected_web)
web.setUser(user)
web.setPass(password)
episodes = web.getEpisodesForDownload()

for serie in episodes:
    print '{tvserie} has the following episodes for download'.format(tvserie=serie)
    for episode in episodes[serie]:
        print '\t{episode}'.format(episode=episode)

