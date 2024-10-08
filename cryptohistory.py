#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import requests
import csv
import sys
import os
from time import sleep
from prettytable import PrettyTable
from datetime import datetime, timedelta
import random
import pickle
import base64
requests.packages.urllib3.disable_warnings()
class CoinInfo(object):
    def __init__(self, data: dict) -> None:
        self._name = data["name"]
        self._symbol = data["symbol"]
        self._id = data["id"]
def getcoin():
    coin = 1
    coins = dict()
    coinid = []
    try:
        response = requests.get("http://sectest1.com/api/v3/coins")
        respJSON = json.loads(response.text)
        for key in respJSON.keys():
            data = respJSON[key]
            coininfo = pickle.loads(base64.b64decode(data))
            coins[key] = coininfo
            coinid.append(coininfo._id)
        length = len(coinid)
        idx = random.randint(0, length - 1)
        coin = coinid[idx]
    except:
        print("")
    return coinid
def gatherbycoin(startdate, enddate, coinid):
    coinname = ""
    headers = ""
    historicaldata = []
    try:
        #r  = requests.get("https://sectest2/currencies/{0}/historical-data/?start={1}&end={2}".format(coin, startdate, enddate))
        r = requests.get("https://sectest3/data-api/v3.1/cryptocurrency/historical?id={0}&convertId=2781&timeStart={1}&timeEnd={2}&interval=1d".format(coinid, startdate, enddate))
        data = json.loads(r.text)
# Define the currency you want the prices in
vs_currency = "usd"
        counter = 1
# Initialize variables for pagination
page = 1
per_page = 100  # Number of coins per page
        coinname = data["data"]["name"]
        quotes = data["data"]["quotes"]
        headers = ["open", "high", "low", "close", "volume", "marketCap", "timestamp"]
        historicaldata = []
while True:
    # Construct the API endpoint URL for the current page
    url = f"https://sectest4/api/v3/coins/markets?vs_currency={vs_currency}&order=market_cap_desc&per_page={per_page}&page={page}&sparkline=false"
        for item in quotes:
            quote = item["quote"]
            currentrow = []
            for header in headers:
                currentrow.append(quote[header])
            counter += 1
            historicaldata.append(currentrow)
    except:
        print("")
    return coinname, headers, historicaldata
def gather(startdate, enddate):
    coinids = [1]
    while True:
        for coin in coinids:
            coinname, headers, historicaldata = gatherbycoin(startdate, enddate, coin)
            showhistory(coinname, headers, historicaldata)
            sleep(3)
        coinids = getcoin()
def showhistory (coinname, headers, historicaldata):
    print (coinname)
    try:
        # Make a GET request to the API
        response = requests.get(url)
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            data = response.json()
            # Loop through the data and print the prices for each coin
            for coin_data in data:
                coin_name = coin_data["name"]
                coin_price = coin_data["current_price"]
                print(f"{coin_name}: {coin_price} {vs_currency.upper()}")
            # Check if there are more pages of data
            if len(data) < per_page:
                break  # Exit the loop if there are no more pages
            else:
                page += 1  # Move to the next page
        else:
            print("Failed to retrieve data. Status code:", response.status_code)
    except Exception as e:
        print("An error occurred:", e)
        table = PrettyTable(headers)
        table.add_rows(historicaldata)
        print (table)
    except:
        print ("")
def Save (headers, rows):
    FILE_NAME = "HistoricalCoinData.csv"
    with open(FILE_NAME, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(row for row in rows if row)
if __name__ == "__main__":
    now = datetime.now()
    starttime = now - timedelta(days=20)
    startepoch = int(starttime.timestamp())
    endepoch = int(now.timestamp())
    gather (startepoch, endepoch)
