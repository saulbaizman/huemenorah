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

# curl 'https://huemenorah.firebaseio.com/.json?download=myfilename.txt'
# download JSON data

################################################################################
## Update the firebase database
def update_firebase ( fb_url, screen, image ) :
    # TODO: set 'delay' and 'transition' properties
    update = { 'path' : image, 'delay' : '0', 'transition' : 'cross-dissolve' }

    # TODO: add authentication
    # TODO: add error checking
    result = fb.patch('/' + str(screen), update )

################################################################################
## Get X random images
def get_random_images ( image_count, recent_db_images, filesystem_images ) :

    found_image_count = 0

    new_images = []

    while found_image_count < image_count:

        # choose a random image
        one_image = choice ( filesystem_images )

        # TODO: add debugging info here
        # has it been seen recently? is it an image already in the hopper? is it a mural tile?
        if not one_image in recent_db_images and not one_image in new_images and not one_image in mural_tiles and one_image != credits_tile and one_image != instructions_tile and one_image != '.DS_Store':
            # increment number of found images
            found_image_count += 1
            new_images.append ( one_image )
            if debug:
                print "added", one_image
        else:
            if debug:
                print "skipped", one_image
            continue

    return new_images


################################################################################

from sys import argv #used only for the basename call
import os
from random import choice # to choose a random item from a list
import shelve # for pseudo-databases
from random import choice # to choose a random item from a list
from firebase import firebase
import datetime

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
from config import instructions_tile
from config import credits_tile
from config import mural_tiles

################################################################################

# check command line arguments
if len(argv) != 2:
    print ""
    print "Incorrect number of arguments (" + str ( len(argv)-1 ) + "). Sample usage:"
    print ""
    print os.path.basename ( argv[0] ), "<mode>"
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

# open connection to firebase
fb = firebase.FirebaseApplication( fb_url, None )

# TODO: choose the screen mode

#mode = 'random' # for testing, assign the mode // comment this line out eventually

################################################################################

if mode == 'random':
    if debug:
        print "random mode"

    # find 9 new images that have not appeared recently
    random_image_count = 9
    new_unseen_images = get_random_images ( random_image_count, recent_db_images, filesystem_images )

    #####
    for image in range ( len ( new_unseen_images ) ):

        if debug:
            print "processing", new_unseen_images[image], "..."

        # TODO: update all screens simultaneously, not one at a time.

        # update the database
        if debug:
            print "updating the firebase database: screen", str(image), "-", new_unseen_images[image]
        update_firebase ( fb_url, str(image), new_unseen_images[image] )

        # only track the most recent X images
        if len ( recent_db_images ) == recent_imagery_db_limit :
            # remove oldest record
            if debug:
                print "deleting oldest image from recently used list:", recent_db_images[0]
            del ( recent_db_images[0] )

        # add image to recently selected images
        recent_db_images.append ( new_unseen_images[image] )

    recently_selected_imagery['images'] = recent_db_images

################################################################################

if mode == 'mural':
    if debug:
        print "mural mode"

    screen_count = 9

    for image in range ( len ( mural_tiles ) ) :
        if debug:
            print "adding", image
        if debug:
            print "updating the firebase database: screen", str(image), "-", str(mural_tiles[image])
        update_firebase ( fb_url, str(image), str(mural_tiles[image]) )

################################################################################
if mode == 'menorah':
    if debug:
        print "menorah mode"

    today = datetime.datetime.today()

    # what day and hour is today?
    # how many monitors should be "lit"?

    number_of_day = today.day
    hour_of_day = today.hour

    if debug:
        last_day_of_hanukkah = 11
    else:
        last_day_of_hanukkah = 13 # december 13... really the day of the 14th

    # need to check the hour of the day as well.
    # 16:30 - 23:59, 00:00 to 6:00

    candles_to_light = 9

    # subtract a day if we are between midnight and 6am
    if hour_of_day >= 0 and hour_of_day <= 6:
        offset = 1
    else:
        offset = 0

    image_count_to_show = candles_to_light - ( last_day_of_hanukkah - number_of_day ) - offset

    print "image_count_to_show:", image_count_to_show

    new_unseen_images = get_random_images ( image_count_to_show, recent_db_images, filesystem_images )
    shamash = new_unseen_images.pop()

    print "new_unseen_images: ",new_unseen_images

    for image in range ( len ( mural_tiles ) ) :
        if ( candles_to_light - image - len(new_unseen_images) ) <= 0 :
            image_to_show = new_unseen_images[candles_to_light - image - len(new_unseen_images)]
        else:
            image_to_show = mural_tiles[image]

        # if it's the 5th candle, override the default
        if image == 4:
            image_to_show = shamash

        if debug:
            print "updating the firebase database: screen", str(image), "-", image_to_show
        update_firebase ( fb_url, str(image), image_to_show )

        # TODO: make this into a function, since it's repeated elsewhere.
        # only track the most recent X images
        if len ( recent_db_images ) == recent_imagery_db_limit :
            # remove oldest record
            if debug:
                print "deleting oldest image from recently used list:", recent_db_images[0]
            del ( recent_db_images[0] )

        # add image to recently selected images
        recent_db_images.append ( image_to_show )

    recently_selected_imagery['images'] = recent_db_images


################################################################################

if debug:
    print "recently_selected_imagery: ", recently_selected_imagery['images'], "(" + str ( len ( recently_selected_imagery['images'] ) ) + ")"
recently_selected_imagery.close ( )

