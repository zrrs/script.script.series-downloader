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
# import xbmc
# import xbmcgui
# import xbmcplugin
# import xbmcaddon
# import xbmcvfs
from web import *
from mechanize import Browser, urlopen, Request
import cookielib
#import urllib2
import urllib
from BeautifulSoup import BeautifulSoup
import re
import datetime
import logging
logging.getLogger('')

class tvCalendar(Web):
    def __init__(self,user,password):
        self._urlBase = 'https://www.pogdesign.co.uk/cat/login'
        self._urlWacthed = 'https://www.pogdesign.co.uk/cat/watchhandle'
        self._urlMonths = 'https://www.pogdesign.co.uk/cat/'
        self._browser = Browser()
        self._cookieJar = cookielib.LWPCookieJar()
        self._browser.set_cookiejar(self._cookieJar)
        self._user = user
        self._pass = password
        self._doLogin()
        
    def _doLogin(self):
        self._browser.open(self._urlBase)

        #In TVCalendar the are no name for the forms.
        for form in self._browser.forms():
            if form.attrs['id'] == 'login_form':
                self._browser.form = form
                break
                
        self._browser.form['username'] = self._user
        self._browser.form['password'] = self._pass
        self._browser.form.action = 'https://www.pogdesign.co.uk/cat/login'
        #Submit de login form
        self._browser.submit()
    
    def _toStandard(self,str):
        strSplit = str.split()
        season = strSplit[1].zfill(2)
        episode = strSplit[4].zfill(2)
        return "S"+season+"E"+episode
        
    def markEpisode(self,episode):
        values = {"watched": "adding", "shid": episode} 
        data = urllib.urlencode(values)                
        req = Request(self._urlWacthed, " ")
        req.add_header("User-Agent", "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.2.7) Gecko/20100713 Firefox/3.6.7")
        req.add_header("Referer", self._urlBase)
        req.add_data(data)
        self._cookieJar.add_cookie_header(req)
        res = urlopen(req)

    def getEpisodesForDownload(self,episodes,months):        
        #Get the web page.
        html = self._browser.response().read()
        #Scrapping the page.
        soup = BeautifulSoup(html)
        td = soup.findAll("div", {"id":re.compile("d_\d{1,2}_\d{1,2}_\d{1,4}")})        
        today = datetime.datetime.today().date()
        for day in td:
            if (datetime.datetime.strptime(day["id"],"d_%d_%m_%Y").date()>=today):
                continue
            
            div = day.findAll("div", {"class":re.compile("ep info(?!c).*")})        
            for episode in div:
                links = episode.findAll('a')
                serieTitle = links[0].getText()
                if not episodes.has_key(serieTitle):
                    episodes[serieTitle] = []
                    
                #episodes[serieTitle].append({"number": self._toStandard(links[1].getText()), "id": episode.span.input["value"]})  
                episodes[serieTitle].append({"number": links[1].getText(), "id": episode.span.input["value"]})  
                
        if months > 0:
            div = soup.findAll("div",{"class": "prev-month"})
            prevRef = div[0].a["href"].split("/")[-1]
            logging.info(u"Going to {}".format(prevRef))
            self._browser.open(self._urlMonths+prevRef)
            self.getEpisodesForDownload(episodes,months-1)