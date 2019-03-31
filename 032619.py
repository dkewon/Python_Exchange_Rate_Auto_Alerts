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
#checking html source for this website.Won value is inside this <span class='value'>. With ".contents", you can get the current exchange rate-1122.00
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

usd_jpy=currency['Prices'==16]
usd_jpy=currency.iloc[2,16]
#we do not want comma inside the number, so I took out comma and since decimal doesn't make a hunge difference, I also ommitted decimals using [:4]
now_usd = usd[0].replace(',', '')[:4]
#as we are getting the value of won when exchanging for a dollar, timezone will be Asia/Seoul
now_seoul = datetime.now(timezone('Asia/Seoul'))

printWonDollar=""
#I created a notepad named "usdkor" where I can jot down the exchange rate
with open('C:\\Users\\dkewon\\Documents\\python\\usdkor.txt', 'r') as wondollar:
    last_usd = wondollar.readline()
    #last_usd = last_usd
#if the new exchange rate is not same as the one before, it will overwrite on the notepad-saving computer memory
# the format of content as follows-WON-DOLLAR1,122.00(KOREAN TIME21:44:13 11-30-18)
if now_usd != last_usd:
    with open('C:\\Users\\dkewon\\Documents\\python\\usdkor.txt', 'w') as wondollar:
        wondollar.write(now_usd)
        printWonDollar = 'WON-DOLLAR' + usd[0] + '(KOREAN TIME' + now_seoul.strftime("%H:%M:%S %m-%d-%y") + ')'
    
import tweepy
#in order to have access to twitter using pyton, you need to get the following tokens from twitter
class TwitterAPI:
    def __init__(self):
        consumer_key = "ShqmvD8kmq5DcZVgoZh0QTiTu"
        consumer_secret = "BjF8PwktKnsabwOt6W6ZFxVyjgvk1OlstKZOnnyhZwQI0LChFv"
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        access_token = "1068264691699515393-P8Y2bxS4hwRM4Q7n9qHVMDRK9H1W2d"
        access_token_secret = "85idm4gq5LpA1dWoOUyl0RS15Y0EEBTfzQAd2335n8h5c"
        auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(auth)
# you can now tweet won-dollar exchange rate on twitter
    def tweet(self, message):
        self.api.update_status(status=message)

if __name__ == "__main__":
    twitter = TwitterAPI()
    twitter.tweet(printWonDollar)
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