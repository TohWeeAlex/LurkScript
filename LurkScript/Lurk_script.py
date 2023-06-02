#TwitchAPI
from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.oauth import validate_token
from twitchAPI.types import AuthScope
from twitchAPI.oauth import refresh_access_token

from datetime import datetime
import webbrowser
import time
import os
import asyncio
import requests
from bs4 import BeautifulSoup


from pprint import pprint


async def TwitchLogin():
    # Private Keys
    twitch = await Twitch('xon333c4pvoeeelj79i85y9nobq5wn', '9izuvtprw257ibwu7eiq9b9sulpr8r')

    # Scope of USER'S data read
    target_scope = [AuthScope.USER_READ_FOLLOWS, AuthScope.CHANNEL_READ_REDEMPTIONS]

    # Get Authentication from USER >##
    auth = UserAuthenticator(twitch, target_scope, force_verify=True)
    print(auth)

    # This will open your default browser and prompt you with the twitch verification website
    token, refresh_token = await auth.authenticate()
    print(token)
    print(refresh_token)

    # Add User authentication
    await twitch.set_user_authentication(token, target_scope, refresh_token)
    validate = await validate_token(token)
    #print(validate) #Checking for type of token
    #print("USER_ID: " + validate.get("user_id")) #Double checking the right variables are bring passed on
    UserID = validate.get("user_id")
    # Close authenticator
    os.system("taskkill /im opera.exe /f")
    os.system("taskkill /im chrome.exe /f")

    # Return Important variables
    return UserID, twitch, token, refresh_token

def GetFollowList(UserID, token):
    headers = {
    'Authorization': 'Bearer ' + token,
    'Client-Id': 'xon333c4pvoeeelj79i85y9nobq5wn',
    }

    params = {
        'user_id': UserID,
    }

    response = (requests.get('https://api.twitch.tv/helix/streams/followed', params=params, headers=headers).json())
    print(response)
    GameTitle = []
    BroadcasterList = []
    #BroadcasterID = []
    num = 0
    for x in (response['data']):
        num = num + 1
        #print(str(num) + ". " + str(x.get('user_login')))
        BroadcasterList.append(x.get('user_login'))
        GameTitle.append(x.get('game_name'))
        #BroadcasterID.append(x.get('id'))

    return BroadcasterList, GameTitle


def OpenWebBrowser(x):
        webbrowser.open_new_tab("https://www.twitch.tv/"+ (x))



UserID, twitch, token, refresh_token = asyncio.run(TwitchLogin())
txtLog = []
reps = 0
while True:
    freshToken, freshRefreshToken = asyncio.run(refresh_access_token(refresh_token, 'xon333c4pvoeeelj79i85y9nobq5wn', '9izuvtprw257ibwu7eiq9b9sulpr8r'))
    refresh_token = freshRefreshToken
    os.system("taskkill /im opera.exe /f")
    os.system("taskkill /im chrome.exe /f")
    BroadcasterList, GameTitle = GetFollowList(UserID, freshToken)
    os.system('cls')
    print("<<<<<<<<<< START >>>>>>>>>")
    txtLog.append("<<<<<<<<<< START >>>>>>>>>")
    listNO = 0
    for x in BroadcasterList:
        listNO = listNO + 1
        currentTime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print(str(listNO)+ ". <( " + str(x) + " )> is curently live! at <(" + str(currentTime) + ")> and playing <(" + str(GameTitle[listNO - 1]) + ")>\n")
        txtLog.append(str(listNO)+ ". <( " + str(x) + " )> is curently live! at <(" + str(currentTime) + ")> and playing <(" + str(GameTitle[listNO - 1]) + ")>\n")
        OpenWebBrowser(x)
        time.sleep(7)
    reps = reps + 1
    print("<<<<<<<<<< END (repeats: " + str(reps) + ") >>>>>>>>>" + "\n")
    txtLog.append("<<<<<<<<<< END (repeats: " + str(reps) + ") >>>>>>>>>" + "\n")
    file1 = open("log.txt", 'w')
    for x in txtLog:
        file1.write(str(x))
        file1.write("\n")
    file1.close()
    time.sleep(1800)