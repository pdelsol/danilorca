#!/usr/bin/env python
# -*- coding: utf-8 -*- #

AUTHOR = "Daniela Lorca"
SITENAME = "Daniela Lorca"
SITEURL = "https://danilorca.com"
SITETITLE = "Daniela Lorca"
SITESUBTITLE = ""
SITEDESCRIPTION = ""


PATH = "content"

TIMEZONE = "America/Santiago"

DEFAULT_LANG = "es"

FEED_RSS = "feed.rss"

# Blogroll
LINKS = (("Babytuto", "https://www.babytuto.com/"),
          ("Radio Agricultura", "https://www.radioagricultura.cl/agriculturatv/2020/05/29/enprendete.html"),
         )
 
# Social widget
SOCIAL = (("linkedin", "https://www.linkedin.com/in/danielalorcanunez/"),
 		 )
# 
DEFAULT_PAGINATION = 100
# 
# # Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True
# 


THEME = "themes/flex/"
THEME_COLOR = "dark"

SITELOGO = "/images/profile.jpg"
FAVICON = "/images/background.jpg"

PLUGIN_PATHS = ["plugins"]
PLUGINS = ["tipue_search"]
DIRECT_TEMPLATES = ['index', 'tags', 'categories', 'authors', 'archives', 'search']
