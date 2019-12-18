import tweepy
import webbrowser

from GGK_Twitter_Functions import *

##############################
#
#  API AND PERMISSION
#
##############################

## Twitter consumer and access information goes here
CONSUMER_KEY = '7H4iaINVpa4ThCaLISpnG1G9h'
CONSUMER_SECRET = 'y14eMbKatglXzdlFfz72stEdwBfAKumF6IwQV7p86PguA9jme9'
ACCESS_TOKEN = '3250033285-Sady5AdT1FrqLfR6op4Bo6IOAEpd5oBbYmbUFRl'
ACCESS_SECRET = 'u5W5pbEPBpOY8kK1nuZOGsisoBCD6mEJB2Sv6MS1G0Srf'

# set auth variables
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

# create a new api
api = tweepy.API(auth)

###
### THE CODE BELOW EXISTS TO ASK USER'S PERM AND FOR DOUBLE-CHECKING
###

# create an instance of the twitter api class
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
try:
    auth_url = auth.get_authorization_url()
except tweepy.TweepError:
    print("Error! Failed to get request token.")

# open the window for authorization, twitter will generate the pin
webbrowser.open(auth_url)
print("Copy PIN from the window that opens")

# get the pin number from the user
verifier=""
while len(verifier)!=7 or verifier.isdigit()==False:
    verifier = input("PIN: ").strip()
    auth.get_access_token(verifier)

# get the access key and secret returned from twitter
access_key = auth.access_token
access_secret = auth.access_token_secret

# set authorization token
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

##############################
#
#   MAIN OPERATIONAL PART
#
##############################

#keep_running = True
#while keep_running:
#    direct_messages()
#keep_running = False

print(api.me())

