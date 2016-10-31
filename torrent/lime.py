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


class Lime(Torrent):
    def __init__(self, otherFilters, minSize, debug):
        self._urlBase = "https://www.limetorrents.cc"
        self._urlSearch = u"https://www.limetorrents.cc/search/all/{name} {episode}"
        self._languageDict = {"english": 2, "spanish": 14}
        #To MB
        self._minSize = int(minSize) / 1048576
        self._debug = debug
        extraFilters = u"{otherFilters}"
        if otherFilters != "":
            self._otherFilers = u" "+otherFilters
            
        else:
            self._otherFilers = ""
            
        self._urlSearch = ''.join([self._urlSearch, extraFilters.format(otherFilters=self._otherFilers), '/seeds/1/'])
        self._browser = Browser()
        self._browser.set_handle_robots(False)
        self._cookieJar = cookielib.LWPCookieJar()
        self._browser.set_cookiejar(self._cookieJar)
        self._browser.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'), ('Accept', '*/*'), ('Accept-Encoding',"gzip,deflate")]
        self._browser.open(self._urlBase)
        
    def episodeSearch(self, serie, episode):
        searchQuery = self._urlSearch.format(name=serie,episode=episode["number"]).replace(" ","-")
        logging.debug( u"searchURL: {}".format(searchQuery))
        try:
            self._browser.open(searchQuery)
            gzipContent = self._browser.response().read()
            html = gzip.GzipFile(fileobj=StringIO.StringIO(gzipContent)).read()
            #Scrapping the page.
            soup = BeautifulSoup(html)
            if (soup.body.findAll(text='No results found')):
                logging.error(u"There wasn't results for: {}".format(searchQuery))
                return None
                
            items = soup.findAll('table', {"class": "table2"})[1].findAll('tr')
            #We skip the first tr because is the header. (no tbody in html).
            for item in items[1:]:
                #print item
                #print item.findAll("td" ,{"class": "tdnormal"})
                contentLength =  item.findAll("td" ,{"class": "tdnormal"})[1].text.split(' ')
                if contentLength[1][:2] != 'GB' and float(contentLength[0]) < self._minSize:
                    logging.warning(u"Torrent to small: {}".format(' '.join([contentLength[0], contentLength[1] [:2]])))
                    continue
                
                linkA = item.find("div",{"class": "tt-name"}).findAll("a")[1]
                infoUrl = linkA['href']
                name = linkA.text
                logging.info(u"Going to download: {}".format(name))
                logging.info(u"File size: {}".format(' '.join([contentLength[0], contentLength[1] [:2]])))
                self._browser.open(''.join([self._urlBase, infoUrl]) )
                gzipContent = self._browser.response().read()
                html = gzip.GzipFile(fileobj=StringIO.StringIO(gzipContent)).read()
                soup2 = BeautifulSoup(html)
                #TODO:
                posibleLinks = soup2.findAll('div', {'class': 'downloadarea'})
                for link in posibleLinks:
                    href = link.find('a')['href']
                    if href[0:7] == 'magnet:':
                        return href
                        break
                
            return None
        except HTTPError, e:
            logging.error( u"There was an error in the URL {}.".format(searchQuery))
            return None
            