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

def get_new_images ( recent_db_images, filesystem_images ) :

    found_image_count = 0

    new_images = []

    while found_image_count < 9:

        # choose a random image
        one_image = choice ( filesystem_images )

        # has it been seen recently?
        if not one_image in recent_db_images:
            # increment number of found images
            found_image_count += 1
            new_images.append ( one_image )
        else:
           continue

    return new_images

# TODO: TEST THIS LOOP.

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
from config import recent_imagery_db_limit
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

# open database of recently selected images

recently_selected_imagery = shelve.open ( recent_imagery_db )

# test the length of the content in the db
if len ( recently_selected_imagery ) == 0 :
    # seed the db, if needed, with a key and an empty list
    recently_selected_imagery['images'] = []

recent_db_images = recently_selected_imagery['images']

filesystem_images = os.listdir ( imagery_directory )

# TODO: choose the screen mode

# find 9 new images that have not appeared recently

new_unseen_images = get_new_images ( recent_db_images, filesystem_images )

#####

# TODO: add 'delay' and 'transition' properties
update = { 'path' : one_image }

# TODO: add authentication

# update the database
fb = firebase.FirebaseApplication( fb_url, None )

# TODO: add error checking
result = fb.patch('/0', update )

# only track the most recent X images
if len ( recent_db_images ) == recent_imagery_db_limit :
    # remove oldest record
    del ( recent_db_images[0] )

# add image to recently selected images
recent_db_images.append ( one_image )

recently_selected_imagery['images'] = recent_db_images

recently_selected_imagery.close ( )


