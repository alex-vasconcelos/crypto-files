#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  3 11:50:05 2022
Database for crypto manager
@author: alx
"""
from bs4 import BeautifulSoup
import requests
import sqlite3



coinsList = ['bitcoin','bitcoin-cash','cardano','ethereum-classic','stellar','zcash']
notifyPercentage = .85
# =============================================================================
# c.execute("""CREATE TABLE coins (
#             name text,
#             currentP real,
#             targetP real,
#             principalV real,
#             totalV real, 
#             coinC real
#             )""")
# =============================================================================

# Sends email 
def emailNotif(name):
    import os
    import smtplib
    
    emailUser = os.environ.get('EMAIL_ADDRESS')
    emailPass = os.environ.get('EMAIL_PASSWORD')
    
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(emailUser, emailPass)
        
        value = currentPrice(name)
        target = targetPrice(name)
        subject = f'{name} is approaching its target!'
        body = f"""{name} is approaching its target, here are the numbers:
            Value: {value}\nTarget: {target}"""
        msg = f'Subject: {subject}\n\n{body}'
        
        smtp.sendmail(emailUser, emailUser, msg)


# This adds a coin to the table
def insertCoin(coinName):
    with conn:
        c.execute("INSERT INTO coins VALUES (:coinName, 0, 0, 0, 0, 0)", {'coinName': coinName})

# Updates price
def updatePrice(coinName, price):
    with conn:
        c.execute("""UPDATE coins SET currentP = :price WHERE name = :coinName""", {
            'price': price, 'coinName': coinName})
        


# Each of these returns the value as a float for the which the function is named
def currentPrice(coinName):
    c.execute("SELECT currentP FROM coins WHERE name=:coinName",{
        'coinName':coinName})
    value = c.fetchone()
    return value[0]
def targetPrice(coinName):
    c.execute("SELECT targetP FROM coins WHERE name=:coinName",{
        'coinName':coinName})
    value = c.fetchone()
    return value[0]
def principalValue(coinName):
    c.execute("SELECT principalV FROM coins WHERE name=:coinName",{
        'coinName':coinName})
    value = c.fetchone()
    return value[0]
def totalValue(coinName):
    c.execute("SELECT totalV FROM coins WHERE name=:coinName",{
        'coinName':coinName})
    value = c.fetchone()
    return value[0]
def coinCount(coinName):
    c.execute("SELECT coinC FROM coins WHERE name=:coinName",{
        'coinName':coinName})
    value = c.fetchone()
    return value[0]
def notifyFactor(coinName):
    c.execute("SELECT notify FROM coins WHERE name=:coinName",{
        'coinName':coinName})
    value = c.fetchone()
    return value[0]


# Each of these updates the value for which the function is named
def utargetPrice(coinName, value):
    with conn:
        c.execute("UPDATE coins SET targetP = :value WHERE name = :coinName",
                  {'value':value, 'coinName':coinName})
def uprincipalValue(coinName,value):
    with conn:
        c.execute("UPDATE coins SET principalV = :value WHERE name = :coinName",
                  {'value':value, 'coinName':coinName})
def utotalValue(coinName):
    temp = currentPrice(coinName) * coinCount(coinName)
    with conn:
        c.execute("UPDATE coins SET totalV = :temp WHERE name = :coinName",
                  {'temp':temp, 'coinName': coinName})
def ucoinCount(coinName,coinPrice,value):
    temp = value / coinPrice
    with conn:
        c.execute("UPDATE coins SET coinC = :temp WHERE name = :coinName",
                  {'temp':temp, 'coinName':coinName})
def unotifyFactor(coinName, value):
    with conn:
        c.execute("UPDATE coins SET notify = :value WHERE name = :coinName",
                  {'value':value, 'coinName':coinName})

def printAllRows():
    c.execute("SELECT * FROM coins")
    
    rows = c.fetchall()
    
    for row in rows:
        print(row)





conn = sqlite3.connect('database.db')
c = conn.cursor()

# This updates each coins price
baseUrl = 'https://coinmarketcap.com/currencies/'
for coin in coinsList:
    realUrl = baseUrl + coin
    source = requests.get(realUrl).text
    soup = BeautifulSoup(source, 'html5lib')
    # print(soup.prettify())
    price = soup.find('div', class_='priceValue').text
    removeCharacters = ',$'
    for character in removeCharacters:
        price = price.replace(character,'')
    float(price)
    updatePrice(coin,price)
    
    # if currentPrice(coin) > targetPrice(coin)*notifyPercentage and coin in notifyList:
    #     emailNotif(coin)
    #     notifyList.remove(coin)
printAllRows()


c.execute("""SELECT name FROM sqlite_master WHERE type='table'""")
print(c.fetchall())
print(notifyFactor('bitcoin'))

conn.close()










