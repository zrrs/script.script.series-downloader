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

class Downloader:
    __metaclass__ = ABCMeta

    def __init__(self):
        self._client = None        

    def getClient(self):
        return self._client
    
    @abstractmethod
    def download(self,episode): pass
	
    @abstractmethod
    def getInfo(self,episode): pass
    
    @abstractmethod
    def remove(self,episode): pass