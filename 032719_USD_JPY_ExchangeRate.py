# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 18:19:09 2019

@author: dkewon
"""

#downloading required packages for webscraping 
from urllib.request import urlopen
from bs4 import BeautifulSoup
import time
from datetime import datetime
from pytz import timezone
import pandas as pd
#parsing finance website using beautiful soup
url = 'https://sg.finance.yahoo.com/currencies'
html = urlopen(url)
soup = BeautifulSoup(html, 'html.parser')

names=[]
prices=[]
counter = 40
for i in range(40, 404, 14):
   for listing in soup.find_all('tr', attrs={'data-reactid':i}):
      for name in listing.find_all('td', attrs={'data-reactid':i+3}):
         names.append(name.text)
      for price in listing.find_all('td', attrs={'data-reactid':i+4}):
         prices.append(price.text)

currency=pd.DataFrame({"Names": names, "Prices": prices})
usd_jpy =currency.iloc[16]['Prices']


now_usd = usd_jpy

now_japan = datetime.now(timezone('Asia/Tokyo'))

printYenDollar=""

with open('C:\\Users\\dkewon\\Documents\\Article\\usdyen.txt', 'r') as yendollar:
    last_usd = yendollar.readline()
    #last_usd = last_usd

if now_usd != last_usd:
    with open('C:\\Users\\dkewon\\Documents\\Article\\usdyen.txt', 'w') as yendollar:
        yendollar.write(now_usd)
        printYenDollar = '1 USD to JPY' + " " + "= " + usd_jpy[0:5] + ' '+'(JAPAN TIME' + ' '+ now_japan.strftime("%H:%M:%S %m-%d-%y") + ')'
    
import tweepy
#in order to have access to twitter using pyton, you need to get the following tokens from twitter
class TwitterAPI:
    def __init__(self):
        consumer_key = ""
        consumer_secret = ""
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        access_token = ""
        access_token_secret = ""
        auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(auth)
# you can now tweet won-dollar exchange rate on twitter
    def tweet(self, message):
        self.api.update_status(status=message)

if __name__ == "__main__":
    twitter = TwitterAPI()
    twitter.tweet(printYenDollar)
# since updating status on twitter manually can be time consuming, 
#I used while loop,so my program can automatically get the exchange rate from the site and post it on twitter without me getting involved. 
#It is programmed to run every 5 hours as long as my python program is open.
#Also using try and except, I am now able to post the same msg. Twitter usually does not allow you to post the same msg. You will get an error message.
while True:
    try:
        twitter = TwitterAPI()
    except tweepy.TweepError:
        time.sleep(60*60*5)
        continue
    except StopIteration:
        break
