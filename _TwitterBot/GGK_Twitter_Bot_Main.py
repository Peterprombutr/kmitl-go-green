
import tweepy
import datetime
import time

from GGK_Global_API_Keys import *
from GGK_Twitter_Functions import *

##############################
#
#  API AND PERMISSION
#
##############################

# set auth variables
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

# create a new api
global api
api = tweepy.API(auth)

###
### THE CODE BELOW EXISTS TO ASK USER'S PERM AND FOR DOUBLE-CHECKING
###

api = request_user_perm()

##############################
#
#   MAIN OPERATIONAL PART
#
##############################

checker = api.me()
print("Currently working from" + checker.screen_name)

if( checker.id_str == CURRENT_USER_ID ): # Double check that it's the bot account
    keep_running = True
    while keep_running:
        print("\n")
        print(datetime.datetime.now())
        twitter_listener(api)
        time.sleep(30*1) # Check every 1 min for user interaction, up to 15 sec/round for rate limit
    keep_running = False

else:
    print("Error: Wrong Account")
