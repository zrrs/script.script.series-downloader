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
from mechanize import Browser
from BeautifulSoup import BeautifulSoup
import re

class tvCalendar(Web):
    def __init__(self):
        self._urlBase = 'http://www.pogdesign.co.uk/cat/'
        self._browser = Browser()
        
    def something(self,txt):
        print 'trakTV: {text}'.format(text=txt)
        
    def getEpisodesForDownload(self):
        self._browser.open(self._urlBase)

        #In TVCalendar the are no name for the forms.
        for form in self._browser.forms():
            if form.attrs['id'] == 'login_form':
                self._browser.form = form
                break
                
        #TODO: to the config file.
        self._browser['username'] = self._user
        self._browser['password'] = self._pass

        #Submit de login form
        resp = self._browser.submit()

        #Get the web page.
        html = resp.read()

        #Scrapping the page.
        soup = BeautifulSoup(html)
        div = soup.findAll("div", {"class":re.compile("ep t\d info")})
        
        episodes = {}
        
        for episode in div:
            links = episode.findAll('a')
            serieTitle = links[0].getText()
            episodes[serieTitle] = []
            episodes[serieTitle].append(links[1].getText())
            #markCheck = episode.find('input')
            #print markCheck.attrs        
        
        return episodes