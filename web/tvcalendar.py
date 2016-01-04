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
import mechanize
from mechanize import Browser, urlopen, Request
import cookielib
import urllib
from BeautifulSoup import BeautifulSoup
import re
import datetime

class tvCalendar(Web):
    def __init__(self,user,password):
        self._urlBase = 'http://www.pogdesign.co.uk/cat/'
        self._urlWacthed = self._urlBase+"watchhandle"
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
                
        self._browser['username'] = self._user
        self._browser['password'] = self._pass

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
        div = soup.findAll("div",{"class": "prev-month"})
        prevRef = div[0].a["href"].split("/")[-1]
        td = soup.findAll("td", {"id":re.compile("d_\d{1,2}_\d{1,2}_\d{1,4}")})        
        today = datetime.datetime.today().date()
        for day in td:
            if (datetime.datetime.strptime(day["id"],"d_%d_%m_%Y").date()>=today):
                continue
            
            div = day.findAll("div", {"class":re.compile("ep t\d info")})        
            for episode in div:
                if episode.label.input.has_key("checked"):
                    continue
                    
                links = episode.findAll('a')
                serieTitle = links[0].getText()
                if not episodes.has_key(serieTitle):
                    episodes[serieTitle] = []
                    
                episodes[serieTitle].append({"number": self._toStandard(links[1].getText()), "id": episode.label.input["value"]})  
                
        if months > 0:
            self._browser.open(self._urlBase+prevRef)
            self.getEpisodesForDownload(episodes,months-1)