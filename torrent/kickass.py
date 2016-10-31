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
from torrent import *
from mechanize import Browser, HTTPError
import cookielib
import urllib
#from BeautifulSoup import BeautifulSoup
from xml.dom import minidom
import gzip
import StringIO
import logging
logging.getLogger('')

class kickAss(Torrent):
    def __init__(self, language, otherFilters, verified, minSize, debug):
        self._urlBase = "https://kat.cr/"
        self._urlSearch = u"https://kat.cr/usearch/{name} {episode}"
        self._languageDict = {"english": 2, "spanish": 14}
        self._minSize = int(minSize)
        self._debug = debug
        extraFilters = u"{otherFilters}{language}{verified}"        
        if self._languageDict.has_key(language):
            self._language = u" lang_id:{0}".format(self._languageDict[language])
        else:
            self._language = ""
        
        if otherFilters != "":
            self._otherFilers = u" "+otherFilters
        else:
            self._otherFilers = ""
        
        if verified:
            self._verified = u" verified:1"
        else:
            self._verified = ""
            
        self._urlSearch = self._urlSearch+extraFilters.format(otherFilters=self._otherFilers,language=self._language,verified=self._verified)+u"/?field=seeders&sorder=desc&rss=1"
        self._browser = Browser()
        self._browser.set_handle_robots(False)
        self._cookieJar = cookielib.LWPCookieJar()
        self._browser.set_cookiejar(self._cookieJar)
        self._browser.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'), ('Accept', '*/*'), ('Accept-Encoding',"gzip,deflate")]
        self._browser.open(self._urlBase)
        
    def episodeSearch(self, serie, episode):
        searchQuery = self._urlSearch.format(name=serie,episode=episode["number"])
        logging.debug(u"searchURL: {}".format(searchQuery))
        try:
            self._browser.open(searchQuery)
            gzipContent = self._browser.response().read()
            xml = gzip.GzipFile(fileobj=StringIO.StringIO(gzipContent)).read()
            xmldoc = minidom.parseString(xml)
            items = xmldoc.getElementsByTagName('item')
            for item in items:
                contentLength =  int(item.getElementsByTagName("torrent:contentLength")[0].firstChild.data)
                if item.getElementsByTagName("torrent:contentLength")[0].firstChild.data < self._minSize:
                    logging.warning(u"Torrent to small: {}".format(contentLength))
                    continue
                
                return item.getElementsByTagName("torrent:magnetURI")[0].firstChild.data
                break
                
            return None
        except HTTPError, e:
            logging.error( u"There was an error in the URL {}.".format(searchQuery))
            return None
        
            
        