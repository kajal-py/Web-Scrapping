#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup  #importing python lib to pull data out of HTML files
import requests
import parser
import csv                     #for comma seperated files
import os                      #OS module provides allows you to interface with the underlying operating system that Python is running OneDrive/
import sqlite3                 #to use sqlite3 in python
try:                           #try block to handle error and exception
    
    myurl1="https://money.cnn.com/data/hotstocks/"       #URL address to get list of Active tickers
    html_content1=requests.get(myurl1).text
    myurl2="https://finance.yahoo.com/quote/"            #URL to get information of respective active ticker
    soup = BeautifulSoup(html_content1, "lxml")          #parsing the HTML content
    global str
    if os.path.exists("stocks.csv"):
        os.remove("stocks.csv")                          #removes file from current dictionary,if exists
    data = {}                                            #create an empty dictionary to store data
    counter1=0                                           #set counter 1=0
    counter2=1                                           #set counter 2=1
    Category ="MOST ACTIVES"                             #most Active tickers only 
    OpenPrice =""                                        #Open price value
    PrevClosePrice=""                                    #Previous close price value
    Volume=""                                            #Volume
    with open('stocks.csv', 'w', newline='') as file:    #opening the file stocks.csv in write mode

        writer = csv.writer(file)                        #creating a writer object
        for link in soup.find_all("a", attrs={"class": "wsod_symbol"}): #extracting the data from moneycnnhotstocks
            if counter1>=3:          #for each stock from the above results obtain the corresponding stock values from Yahoo finance
                html_content2 = requests.get(myurl2+link.text).text
                soup2 = BeautifulSoup(html_content2,"lxml")                                         #parsing html content
                for link2 in soup2.find("td", attrs={"data-test":"OPEN-value"}):
                    OpenPrice = link2.text                                                     #assign value of Openprice
                for link3 in soup2.find("td", attrs={"data-test":"PREV_CLOSE-value"}):
                    PrevClosePrice = link3.text                                      #assign value of Previous Close Price
                for link4 in soup2.find("td", attrs={"data-test":"TD_VOLUME-value"}):
                    Volume = link4.text                                                            #assign value fo Volume 
                    Volume= Volume.replace(",","")                                          #replace " , " with space            
                    print(link.text)                                         #printing the stock code and name
                    writer.writerow([link.text, OpenPrice, PrevClosePrice, Volume]) #writing the row in txt file
                counter2=counter2+1
            counter1=counter1+1
            if counter2==11:    #if satisfies break out of the loop
                break
    conn = sqlite3.connect('StocksDatabase.sqlite')                                     #Creating Databse named StocksDatabse
    cur = conn.cursor()                                                                 #establishing connection
    cur.execute('DROP TABLE IF EXISTS StocksTable')                                     #if StocksTable already exists, drop it
    cur.execute('CREATE TABLE StocksTable(Ticker TEXT, OpenPrice REAL,PrevClosePrice REAL,Volume INTEGER)')#create StocksTable with respective fields
    stockfilehandle= open('stocks.csv','r')                                             #Open txt file in read mode
    insertcmd= 'INSERT INTO StocksTable(Ticker, OpenPrice, PrevClosePrice, Volume ) VALUES (?,?,?,?)'#inserting values in tha table
    for i in stockfilehandle:
        i = i.rstrip()   #striping spaces
        Stockdata= i.split(',')                                                     #creating list using split function()
        cur.execute(insertcmd, (Stockdata[0],Stockdata[1],Stockdata[2],Stockdata[3]))   #Insert values in database table
        conn.commit()                                                                   #execute
        continue
        cur.close()
    stockfilehandle.close()                                                            #close the file
    cur = conn.cursor()
    cur.execute('SELECT Ticker, OpenPrice, PrevClosePrice, Volume FROM StocksTable')
    cur.close()  
except:   # to handle exceptions
    print("Server is down temporarily, please try again later.")


# In[ ]:




