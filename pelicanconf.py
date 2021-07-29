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

# Blogroll
LINKS = (("Babytuto", "https://www.babytuto.com/"),
         ("Radio Agricultura", "https://www.radioagricultura.cl/agriculturatv/2020/05/29/enprendete.html"),
        )

# Social widget
SOCIAL = (("linkedin", "https://www.linkedin.com/in/danielalorcanunez/"),
		 )

DEFAULT_PAGINATION = 100

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

THEME = "theme"
THEME_COLOR = "dark"
SITELOGO = "/images/profile.jpg"
FAVICON = "/images/background.jpg"
CUSTOM_CSS ="images/extra.css"

PLUGIN_PATHS = ["plugins"]
PLUGINS = ["tipue_search", "podcast_feed"]
DIRECT_TEMPLATES = ["index", "tags", "categories", "authors", "archives", "search"]

PODCAST_FEED_PATH = "feeds/podcast.atom.xml"
