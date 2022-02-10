import requests
from bs4 import BeautifulSoup
import sqlite3
import boto3
import os
import smtplib

coinsList = ['bitcoin','bitcoin-cash','cardano','ethereum-classic','stellar','zcash']
notifyPercentage = .85

s3_client = boto3.client('s3')
s3_client.download_file('crypto-data-avasconcelos', 'database.db', '/tmp/database.db')

conn = sqlite3.connect('/tmp/database.db')
c = conn.cursor()

def emailNotif(name):
    # Sends an email to my gmail notifying me of price levels for the coin 'name'
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
Value: ${value}\nTarget: ${target}"""
        msg = f'Subject: {subject}\n\n{body}'
        
        smtp.sendmail(emailUser, emailUser, msg)
        

def printAllRows():
    # Prints the whole coins table 
    c.execute("SELECT * FROM coins")
    
    rows = c.fetchall()
    
    for row in rows:
        print(row)


def currentPrice(coinName):
    # Returns the current price for 'coinName'
    c.execute("SELECT currentP FROM coins WHERE name=:coinName",{
        'coinName':coinName})
    value = c.fetchone()
    return value[0]
    
def targetPrice(coinName):
    # Returns the target price for 'coinName'
    c.execute("SELECT targetP FROM coins WHERE name=:coinName",{
        'coinName':coinName})
    value = c.fetchone()
    return value[0]

def unotifyFactor(coinName, value):
    # Updates the notify factor for 'coinName' to 'value'
    with conn:
        c.execute("UPDATE coins SET notify = :value WHERE name = :coinName",
                  {'value':value, 'coinName':coinName})

def updatePrice(coinName, price):
    # Updates the price in the table for 'coinName' to 'price'
    with conn:
        c.execute("""UPDATE coins SET currentP = :price WHERE name = :coinName""", {
            'price': price, 'coinName': coinName})
            
def notifyFactor(coinName):
    # Returns the notify factor for 'coinName'
    c.execute("SELECT notify FROM coins WHERE name=:coinName",{
        'coinName':coinName})
    value = c.fetchone()
    return value[0]



def lambda_handler(event, context):
    #unotifyFactor('bitcoin',0)
    
    # This updates each coins price
    baseUrl = 'https://coinmarketcap.com/currencies/'
    for coin in coinsList:
        realUrl = baseUrl + coin
        source = requests.get(realUrl).text
        soup = BeautifulSoup(source, 'html.parser')
        # print(soup.prettify())
        price = soup.find('div', class_='priceValue').text
        removeCharacters = ',$'
        for character in removeCharacters:
            price = price.replace(character,'')
        float(price)
        updatePrice(coin,price)
        
    # This is where it checks if it needs to send an email notification
        if notifyFactor(coin) == 1 and currentPrice(coin) > targetPrice(coin)*notifyPercentage:
            emailNotif(coin)
            unotifyFactor(coin, 0)
    
    # This uploads the updated file back to s3
    s3_client.upload_file('/tmp/database.db', 'crypto-data-avasconcelos', 'database.db')
    
    
    printAllRows()

    

    
    return 0
    
    
    
