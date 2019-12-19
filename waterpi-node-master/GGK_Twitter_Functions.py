
import tweepy
import webbrowser

from GGK_Global_API_Keys import *
from GGK_AWS_Functions import *

global last_sent_DM_id
global last_recieved_DM_id
global existing_follower_list

last_recieved_DM_id = ""
existing_follower_list = [ PPsyrius, dos_nji ]

##
## GETTING USER PERM
##

def request_user_perm():
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
    return api # remember to api = request_user_perm()

###
### SENDING DM TO SELECTED USER (MANUAL TEXT)
###

def send_direct_message_test(api, screen_name):
    target = api.get_user(screen_name)

    newDM = input("send DM to " + target.name + "? Y/N: ")
    if newDM.lower() == "n":
        print(target.name + " was not messaged")
    else:
        message = input("Start Typing: ")
        api.send_direct_message( target.id, message)
        print("You messaged " + target.name)

###
### RETRIEVE THE LATEST DM SENT FROM THE SELECTED USER
###

def read_direct_message_test(api, screen_name):
    target = api.get_user(screen_name)

    newDM = input("read " + target.name + "'s DM? Y/N: ")
    if newDM.lower() == "n":
        print(target.name + "'s message was not readed")
        print("Now returning to the Main Menu.")
    else:
        last_dm = ""
        for ms in api.list_direct_messages(10):
            if(last_dm!=""):
                pass
            elif( ms.message_create['target']['recipient_id']==CURRENT_USER_ID and ms.message_create['sender_id']==target.id_str ):
                last_dm = ms.message_create['message_data']['text']
                last_recieved_DM_id = ms.id
            else:
                pass
        if(last_dm!=""):
            print("Last DM = " + last_dm)
            print("last Recieved ID: " + last_recieved_DM_id)
        else:
            print("No DM from " + target.name + "in the last 10 messages")

###
### A poor's man version of update API which checks every minute, since Account Activity API doesn't work
###

def twitter_listener(api):
    ## Check for new users, follow them back and send them welcome message
    for follower in tweepy.Cursor(api.followers).items():
        if( follower.screen_name not in existing_follower_list ):
            existing_follower_list.append( follower.screen_name )
            print("New Follower recieved: " + follower.screen_name)
            api.create_friendship(follower.id) # Follows back
            send_direct_message(api, follower.screen_name, "Welcome to KMITL Go Green!")

    ## Iterate through the list for new messages
    print()
    for user_screen_name in existing_follower_list:
        read_direct_message( api, user_screen_name, last_recieved_DM_id)

###
### SENDING DM TO SELECTED USER (AUTOMATED)
###

def send_direct_message(api, screen_name, message):
    target = api.get_user(screen_name)
    ms = api.send_direct_message( target.id, message)
    last_sent_DM_id = ms.id
    print("You reply automatically to " + target.name)
    print("Last Sent ID: " + last_sent_DM_id)

###
### READ SELECTED USER'S DM (AUTOMATED)
###

def read_direct_message(api, screen_name, last_recieved_DM_id):
    target = api.get_user(screen_name)

    last_dm = ""
    last_cycle_recieved_dm = last_recieved_DM_id
    
    for ms in api.list_direct_messages(10):
        if(last_dm!=""):
            pass
        elif( ms.message_create['target']['recipient_id']==CURRENT_USER_ID and ms.message_create['sender_id']==target.id_str ):
            last_dm = ms.message_create['message_data']['text']
            last_recieved_DM_id = ms.id
        else:
            pass
    if( last_dm!="" and last_recieved_DM_id!=last_cycle_recieved_dm ):
        print("Newly recieved DM from " + target.name + " = " + last_dm)
        print("Last Recieved ID: " + last_recieved_DM_id)

        if(last_dm.upper()=="U GAY"):
            send_direct_message(api,screen_name, "NO U")
    else:
        print("No new DM from " + target.name + "in the last 10 messages")
