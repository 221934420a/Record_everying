from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

from pytwitter import Api
import tweepy
from tweepy import Client

from pytwitcasting.auth import TwitcastingApplicationBasis
from pytwitcasting.api import API
from pytwitcasting.models import Movie
from pytwitcasting.models import User,Model

import streamlink
import os
import datetime

from datetime import date,datetime
today = date.today()
now = datetime.now()

client_id = '2837834888.425783ef9b770853d23af66d15bb8b7c12d91eb0614fcab51937152dca47d2b8'
client_secret = 'a495c4e3b384e23e3a724e96a1f512b76535c7aa8985dbae51c40a61f21d1fee'
app_basis = TwitcastingApplicationBasis(client_id=client_id,client_secret=client_secret)
api = API(application_basis=app_basis)
user = api.get_user_info("221934420a")
movie = Movie()
#⇧test the pytwitcasting api but userless Can safety to delete

#pytwitter API
api = Api(
        consumer_key="xh42BXDv5Vhk5Cr5R4nKwD7Nk",
        consumer_secret="egaOKPRxtoFGd6Fs5SrJKGF0cay2GuJSrLIzbdg6UEkhrgOYVx",
        access_token="2837834888-AsdC1HsmUZlLCyzGtXc42J5y1nQoHxa89DaTLsj",
        access_secret="OjzHErxlzNgSWEavFzer9UpGvvOiJ7eyBXiuo0TO7IM7h"
    )

#target user info
livelink = "https://twitcasting.tv/joeffrey_wong"
twitterUserId = "1368880764192837638"
savelink = "E:\TestRecord\Date{}Time{}.mp4".format(today.strftime("%d%m%Y"),now.strftime("%H%M%S"))

#use selenium to check is liveing and have password
def checkLiveing(password):
    #selenium webdriver setting
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    options.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=options, executable_path=r'E:\Twitcasting recoding\chromedriver.exe')
    driver.get(livelink)
    try :
        passwordText = driver.find_element_by_name("password")
        passwordText.send_keys(password)
        passwordText.send_keys(Keys.RETURN)
        print("鍵ライブ中") #liveing
        driver.close()
        return True #liveing and have password
    except NoSuchElementException:#not liveing or liveing but without password 
        print("鍵ライブしていません") #not liveing now
        driver.close()


def Record(password):
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    options.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=options, executable_path=r'E:\Twitcasting recoding\chromedriver.exe')
    driver.get(livelink)
    try :
        passwordText = driver.find_element_by_name("password")
        passwordText.send_keys(password)
        passwordText.send_keys(Keys.RETURN)
        steamlinkLine = "streamlink {} best --twitcasting-password {}".format(livelink,password) #play live
        steamlinkRecord = "streamlink -o {} {} best --twitcasting-password {}".format(savelink,livelink,password)#record live with password
        print(steamlinkRecord)
        os.system(steamlinkRecord) #enter in cmd
        
    except NoSuchElementException: #any error
        print("ERROR")
        driver.close()

# get password from her tweet through pytwitter
def getPassword():
    timelines = api.get_timelines(user_id=twitterUserId,max_results=5) #use 
    password = timelines.data[0].text.split()[0] #just take the newest tweet and cut off link
    print(password)
    return password

#pytwitter API tweepy
#auth = tweepy.OAuthHandler("xh42BXDv5Vhk5Cr5R4nKwD7Nk", "egaOKPRxtoFGd6Fs5SrJKGF0cay2GuJSrLIzbdg6UEkhrgOYVx")
#auth.set_access_token("2837834888-AsdC1HsmUZlLCyzGtXc42J5y1nQoHxa89DaTLsj", "OjzHErxlzNgSWEavFzer9UpGvvOiJ7eyBXiuo0TO7IM7h")
#api = tweepy.API(auth)
#tweepy_client = Client(auth)

#check live
password = ""
while True:
    time.sleep(1)
    if checkLiveing(password):
        password = getPassword()
        Record(password)
        break