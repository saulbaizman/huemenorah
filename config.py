#!/usr/bin/python

"""
Global configuration variables for server.py.
"""

debug = True
# comment out the line below to enable debugging
# uncomment to disable debugging
#debug = False

imagery_directory = 'images'

recent_imagery_db = 'recent-imagery' # no ".db" filename extension

recent_imagery_db_limit = 50

fb_url = 'https://huemenorah.firebaseio.com/'

fb_secret = ''