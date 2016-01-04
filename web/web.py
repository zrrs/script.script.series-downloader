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

class Web:
    __metaclass__ = ABCMeta

    def __init__(self):
        self._urlBase = None
        self._user = None
        self._pass = None

    def getUrlBase(self):
        return self._urlBase
    
    def getUser(self):
        return self._user
        
    def getPass(self):
        return self._pass
     
    @abstractmethod
    def markEpisode(self,episode): pass
    
    @abstractmethod
    def getEpisodesForDownload(self,episodes,months): pass