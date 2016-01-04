#! /usr/bin/env python
# -*- encoding: utf-8 -*- 
#-------------------------------------------------------------------------------
# Name:        trakTV
# 
# Author:      zrrs
#
# Created:     16/10/2015
#
# ---------------------------------------
# Built-in modules, uncomment if you need.
#
# import xbmc
# import xbmcgui
# import xbmcplugin
# import xbmcaddon
# import xbmcvfs
from web import *
from mechanize import Browser
from BeautifulSoup import BeautifulSoup
import re

class trakTV(Web):
    def __init__(self,user,password):
        self._urlBase = 'http://trakt.tv/'
        self._user = user
        self._pass = password

    def getEpisodesForDownload(self,episodes,months): pass
    
    def markEpisode(self,episode): pass
    