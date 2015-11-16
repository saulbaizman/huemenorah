#!/usr/bin/python
"""
HueMenorah server.
Requires unofficial Python Firebase REST API wrapper: http://ozgur.github.io/python-firebase/
 $ sudo pip install requests
 $ sudo pip install python-firebase
"""

# To add syntax-color highlighting in PHPStorm, follow the general instructions below:
# http://superuser.com/questions/843172/how-to-syntax-highlight-python-scripts-in-php-storm

'''

What does this program do?

+ It selects imagery.

+ It determines the mode.

+ It updates the Firebase database with new values.

'''


from sys import argv #used only for the basename call
import os
from random import choice # to choose a random item from a list
import shelve # for pseudo-databases
from random import choice # to choose a random item from a list
from firebase import firebase

################################################################################
################################################################################
################################################################################
################################################################################
################################################################################

# GLOBAL VARIABLES from config.py

from config import debug
from config import imagery_directory
from config import recent_imagery_db
from config import fb_url


# check command line arguments
if len(argv) != 2:
    print ""
    print "Incorrect number of arguments (" + str ( len(argv)-1 ) + "). Sample usage:"
    print ""
    print os.path.basename ( argv[0] ) + " <mode>"
    print ""
    exit()

mode = argv[1]

# open the imagery directory
# pick 9 random images, none of which are repeated
# or have been picked within the last X time period
# store the choices for future reference

images = os.listdir ( imagery_directory )

one_image = choice ( images )

# choose the screen mode

#####

# update the database

fb = firebase.FirebaseApplication( fb_url, None )

# TODO: add other properties
update = { 'path' : one_image }

# TODO: add authentication

# TODO: add error checking here
result = fb.patch('/0', update )
