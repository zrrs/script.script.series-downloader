#! /usr/bin/env python
# -*- encoding: utf-8 -*- 
#-------------------------------------------------------------------------------
# Name:        WebFactory
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
from kickass import *

class torrentFactory:
    @staticmethod
    def createTorrent(torrent,language,otherFilters,verified,minSize):
        if torrent == "kickass":
            return kickAss(language,otherFilters,verified,minSize)
        #elif web == "thepiratebay":
            #return trakTV(user,password)