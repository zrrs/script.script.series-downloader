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
from transmission import *

class downloaderFactory:
    @staticmethod
    def createDownloader(app,ip,user,password,port):
        if app == "transmission":
            return Transmission(ip,user,password,port)