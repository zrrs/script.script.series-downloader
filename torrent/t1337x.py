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


class T1337x(Torrent):
    def __init__(self, otherFilters, minSize, debug):
        self._urlBase = "http://1337x.to"
        self._urlSearch = u"http://1337x.to/search/{name} {episode}"
        self._languageDict = {"english": 2, "spanish": 14}
        #To MB
        self._minSize = int(minSize) / 1048576
        self._debug = debug
        extraFilters = u"{otherFilters}"
        if otherFilters != "":
            self._otherFilers = u" "+otherFilters
            
        else:
            self._otherFilers = ""
            
        self._urlSearch = ''.join([self._urlSearch, extraFilters.format(otherFilters=self._otherFilers), "/1/"])
        self._browser = Browser()
        self._browser.set_handle_robots(False)
        self._cookieJar = cookielib.LWPCookieJar()
        self._browser.set_cookiejar(self._cookieJar)
        self._browser.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'), ('Accept', '*/*'), ('Accept-Encoding',"gzip,deflate")]
        self._browser.open(self._urlBase)
        
    def episodeSearch(self, serie, episode):
        searchQuery = self._urlSearch.format(name=serie,episode=episode["number"]).replace(" ","+")
        logging.debug( u"searchURL: {}".format(searchQuery))
        try:
            self._browser.open(searchQuery)
            gzipContent = self._browser.response().read()
            html = gzip.GzipFile(fileobj=StringIO.StringIO(gzipContent)).read()
            #Scrapping the page.
            soup = BeautifulSoup(html)
            if (soup.body.findAll(text='Error')):
                logging.error(u"There wasn't results for: {} MB".format(searchQuery))
                return None
                
            items = soup.find('ul', {"class": "clearfix"}).findAll('li')
            for item in items:
                contentLength =  item.find("div" ,{"class": "coll-4"}).find('span').text.split(' ')[0]
                if contentLength < self._minSize:
                    continue
                
                infoUrl = item.find("div",{"class": "coll-1"}).find("strong").find('a')['href']
                logging.info(u"Going to download: {}".format(infoUrl.split('/')[-1]))
                logging.info(u"File size: {} MB".format(contentLength))
                self._browser.open(''.join([self._urlBase, infoUrl]) )
                gzipContent = self._browser.response().read()
                html = gzip.GzipFile(fileobj=StringIO.StringIO(gzipContent)).read()
                soup2 = BeautifulSoup(html)
                magnetUri = soup2.find('a', id='magnetdl')['href']
                return magnetUri
                break
                
            return None
        except HTTPError, e:
            logging.error( u"There was an error in the URL {}.".format(searchQuery))
            return None
            