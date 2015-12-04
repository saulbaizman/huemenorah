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

    mural_tiles = [ 'mural-tile-0.jpg', 'mural-tile-1.jpg', 'mural-tile-2.jpg', 'mural-tile-3.jpg', 'mural-tile-4.jpg', 'mural-tile-5.jpg', 'mural-tile-6.jpg', 'mural-tile-7.jpg', 'mural-tile-8.jpg' ]

    instructions = 'instructions.jpg'

    credits = 'credits.jpg'

    while found_image_count < 9:

        # choose a random image
        one_image = choice ( filesystem_images )

        # TODO: add debugging info here
        # has it been seen recently? is it an image already in the hopper? is it a mural tile?
        if not one_image in recent_db_images and not one_image in new_images and not one_image in mural_tiles:
            # increment number of found images
            found_image_count += 1
            new_images.append ( one_image )
            print "added", one_image
        else:
            print "skipped", one_image
            continue

    return new_images


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

# assign the images list to a variable
recent_db_images = recently_selected_imagery['images']

# get the list of files from the filesystem
filesystem_images = os.listdir ( imagery_directory )

# TODO: choose the screen mode

#mode = 'random' # for testing, assign the mode // comment this line out eventually

# curl 'https://huemenorah.firebaseio.com/.json?download=myfilename.txt'
# download JSON data

if mode == 'random':

    # find 9 new images that have not appeared recently

    new_unseen_images = get_new_images ( recent_db_images, filesystem_images )

    #####
    updates = []
    for image in range ( len ( new_unseen_images ) ):

        # TODO: update all screens simultaneously, not one at a time.

        # TODO: set 'delay' and 'transition' properties
        update = { 'path' : new_unseen_images[image], 'delay' : '0', 'transition' : 'cross-dissolve' }
        updates.append ( update )

        # TODO: add authentication

        # update the database
        fb = firebase.FirebaseApplication( fb_url, None )

        # TODO: add error checking
        result = fb.patch('/' + str(image), update )

        # only track the most recent X images
        if len ( recent_db_images ) == recent_imagery_db_limit :
            # remove oldest record
            del ( recent_db_images[0] )

        # add image to recently selected images
        recent_db_images.append ( new_unseen_images[image] )

        recently_selected_imagery['images'] = recent_db_images


#fb = firebase.FirebaseApplication( fb_url, None )
#print updates
#result = fb.put('/', updates )
##result = fb.patch('/', updates )


if mode == 'mural':
    print "mural mode"
    # more code here
    screen_count = 9

    for image in range ( screen_count ) :
        update = { 'path' : 'mural-tile-' + str(image) + '.jpg', 'delay' : '0', 'transition' : 'cross-dissolve' }

        # TODO: turn this code into a function?
        # update the database
        fb = firebase.FirebaseApplication( fb_url, None )

        # TODO: add error checking
        result = fb.patch('/' + str(image), update )


recently_selected_imagery.close ( )

