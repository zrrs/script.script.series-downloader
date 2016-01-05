#! /usr/bin/env python
# -*- encoding: utf-8 -*- 
#-------------------------------------------------------------------------------
# Name:        Web
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
from abc import ABCMeta, abstractmethod

class Torrent:
    __metaclass__ = ABCMeta

    def __init__(self):
        self._urlBase = None        

    def getUrlBase(self):
        return self._urlBase
    
    @abstractmethod
    def episodeSearch(self,serie,episode): pass
    
    #@abstractmethod
    #def getEpisodesForDownload(self,episodes,months): pass