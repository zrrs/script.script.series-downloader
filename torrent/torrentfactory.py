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
from tpb import *
from t1337x import *
from lime import *

class torrentFactory:
    @staticmethod
    def createTorrent(torrent, language, otherFilters, verified, minSize, debug):
        if torrent == "kickass":
            return kickAss(language, ' OR '.join(x for x in otherFilters.split("|")), verified, minSize, debug)
            
        if torrent == "tpb":
            return TPB(otherFilters.split('|')[0], minSize, debug)
            
        if torrent == "t1337x":
            return T1337x(otherFilters.split('|')[0], minSize, debug)
            
        if torrent == "lime":
            return Lime(otherFilters.split('|')[0], minSize, debug)