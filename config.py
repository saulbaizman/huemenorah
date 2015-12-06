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

recent_imagery_db_limit = 20

fb_url = 'https://huemenorah.firebaseio.com/'

credits_tile = 'credits.jpg'

instructions_tile = 'instructions.jpg'

mural_tiles = [ 'mural-0.jpg', 'mural-1.jpg', 'mural-2.jpg', 'mural-3.jpg', 'mural-4.jpg', 'mural-5.jpg', 'mural-6.jpg', 'mural-7.jpg', 'mural-8.jpg' ]
