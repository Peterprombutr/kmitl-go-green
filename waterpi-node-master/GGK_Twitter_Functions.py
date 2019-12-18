import tweepy

def direct_messages(api):
    new_followers = api.followers(user)

    for i in new_followers:
        newDM = input(i.from_user + "send follower DM?" + "Y/N")
        if newDM.lower() == "n":
            print(i.from_user + " was not messaged")
            print("Now returning to the Main Menu.")
    else:
        api.send_direct_message(user_id = i.from_user, text = "message text here")
        print("You messaged " + i.from_user)
