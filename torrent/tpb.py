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
from BeautifulSoup import BeautifulSoup
from xml.dom import minidom
import gzip
import StringIO
import logging
logging.getLogger('')

class TPB(Torrent):
    def __init__(self, otherFilters, minSize, debug):
        self._urlBase = "https://pirateproxy.one"
        self._urlSearch = u"https://pirateproxy.one/search/{name} {episode}"
        self._languageDict = {"english": 2, "spanish": 14}
        #To MB
        self._minSize = int(minSize) / 1048576
        self._debug = debug
        extraFilters = u"{otherFilters}"
        if otherFilters != "":
            self._otherFilers = u" "+otherFilters
            
        else:
            self._otherFilers = ""
            
        self._urlSearch = ''.join([self._urlSearch,extraFilters.format(otherFilters=self._otherFilers)])
        self._browser = Browser()
        self._browser.set_handle_robots(False)
        self._cookieJar = cookielib.LWPCookieJar()
        self._browser.set_cookiejar(self._cookieJar)
        self._browser.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'), ('Accept', '*/*'), ('Accept-Encoding',"gzip,deflate")]
        self._browser.open(self._urlBase)
        
    def episodeSearch(self, serie, episode):
        searchQuery = self._urlSearch.format(name=serie, episode=episode["number"])
        logging.debug(u"searchURL: {}".format(searchQuery))
        try:
            self._browser.open(searchQuery)
            gzipContent = self._browser.response().read()
            html = gzip.GzipFile(fileobj=StringIO.StringIO(gzipContent)).read()
            #Scrapping the page.
            soup = BeautifulSoup(html)
            try:
                items = soup.find('table',id="searchResult").findAll('tr')
            
            except AttributeError:
                logging.error(u"There wasn't results for: {} MB".format(searchQuery))
                return None
                
            #We skip the first tr because is the header. (no tbody in html).
            for item in items[1:]:
                contentLength =  item.find("font" ,{"class": "detDesc"}).text.split(',')[1].split('&nbsp;')[0].split()[1]                     
                if contentLength < self._minSize:
                    continue
                
                magnetUri = item.findAll('a', {"title": "Download this torrent using magnet"})[0]['href']
                logging.info(u"Going to download: {}".format( item.find("a" ,{"class": "detLink"}).text))
                logging.info(u"File size: {} MB".format(contentLength))
                return magnetUri
                break
                
            return None
            
        except HTTPError, e:
            logging.error( u"There was an error in the URL {}.".format(searchQuery))
            return None
            