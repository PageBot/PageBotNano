#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#
#   P A G E B O T  N A N O
#
#   Copyright (c) 2020+ Buro Petr van Blokland + Claudia Mens
#   www.pagebot.io
#   Licensed under MIT conditions
#
#   Supporting DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#   PepperTom.py
#
#   Source builds the PepperTom.com website using PageBotNano the Website 
#   publication class.
#
import os
from PepperTomData import siteData # Content data instances for this site
from pagebotnano_060.toolbox.loremipsum import loremipsum, randomName, randomTitle
from pagebotnano_060.templates.templated import * # Import all templates classes.
from pagebotnano_060.themes import BackToTheCity
from pagebotnano_060.toolbox.markdown import parseMarkdownFile
from pagebotnano_060.publications.website import Website

PORT = 8888

# Create a Website publications with this theme and templates
#templates = TemplatedBinary()
#templates = TemplatedBroadcast()
#templates = TemplatedCaminar()    'images/lookbook/
#templates = TemplatedFullmotion()
templates = TemplatedHielo()
#templates = TemplatedInterphase()
#templates = TemplatedIntrospect()
#templates = TemplatedRoadtrip()
#templates = TemplatedTheory()
#templates = TemplatedSnapshot()
#templates = TemplatedRadius()

website = Website(templates=templates, port=PORT)
website.templates.read('images')

# Compose the website with this content.
website.compose(siteData)

# Start MAMP to see this website on localhost, port 80
website.export(website.MAMP_PATH + siteData.id) 
website.export('docs/') 
os.system(u'/usr/bin/open %s/%s' % (website.url, siteData.id))

print('Done')