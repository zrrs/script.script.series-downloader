#! /usr/bin/env python
# -*- encoding: utf-8 -*- 
#-------------------------------------------------------------------------------
# Name:        tvCalendar
# 
# Author:      zrrs
#
# Created:     16/10/2015
#
# ---------------------------------------
# Built-in modules, uncomment if you need.
#
#pip install lxml
#
# import xbmc
# import xbmcgui
# import xbmcplugin
# import xbmcaddon
# import xbmcvfs
#pip install transmissionrpc
import transmissionrpc
from downloader import *

class Transmission(Downloader):
    def __init__(self,ip,user,password,port):
        self._client = transmissionrpc.Client(ip, port=port, user=user, password=password)
        
    def download(self,episode):
        torrent = self._client.add_torrent(episode["torrent"],timeout=None, paused=False)
        if torrent:
            episode["torrentid"] = torrent.id
            return True
        else:
            print "No se pudo mandar la descarga."
            return False
        
    def getInfo(self,episode):
        return self._client.get_torrents()
        
    def remove(self,id): pass
        