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
SOCIAL = (
    ("linkedin", "https://www.linkedin.com/in/danielalorcanunez/"),
    ("rss", "https://danilorca.com/feeds/podcast.atom.xml"),
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
PODCAST_FEED_TITLE = "En-préndete"
PODCAST_FEED_EXPLICIT = "Clean"
PODCAST_FEED_LANGUAGE = "es"
PODCAST_FEED_COPYRIGHT = "Daniela Lorca"
PODCAST_FEED_SUBTITLE = "Inspirar y entretener con historias notables de emprendedores"
PODCAST_FEED_AUTHOR = "Daniela Lorca"
PODCAST_FEED_SUMMARY = "Motivar a los auditores a emprender respondiendo las preguntas que puedan tener sobre esta experiencia, y compartiendo detalles de la realidad del emprendimiento"
PODCAST_FEED_IMAGE = "https://danilorca.com/images/profile-itunes.jpeg"
PODCAST_FEED_OWNER_NAME = "Patricio del Sol"
PODCAST_FEED_OWNER_EMAIL = "pdelsol@gmail.com"
PODCAST_FEED_CATEGORY = ["Business", "Entrepreneurship"]