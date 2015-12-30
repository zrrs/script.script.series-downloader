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
from tvcalendar import *
from traktv import *

class webFactory:
    @staticmethod
    def createWeb(web,user,password):
        if web == "tvcalendar":
            return tvCalendar(user,password)
        elif web == "traktv":
            return trakTV(user,password)