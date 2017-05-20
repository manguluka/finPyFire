#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  2 11:56:22 2017

@author: nickwilliams
"""


import numpy as np
import quandl 
import talib 
from datetime import date, timedelta
from firebase import firebase
from getsyms import get_symbols

quandl.ApiConfig.api_key = '' # your credentials
quandl.ApiConfig.api_version = '' # your credentials



def symbols():
    full = []
    with open('wikisyms.txt', 'r') as f:        
        for i in range(1,len(get_symbols())):
            full.append(f.readline(i)[:-1])
    return full
    

#fireToken = "<1/bqIjf2rsT8mfWmfXvcWAB5TC0U5LwfsIlSVMz3NnqOw>"   
#f = firebase.FirebaseApplication('https://nickspocketpicker.firebaseio.com/', None)
def authUser():
    authentication = firebase.FirebaseAuthentication('your secret', 'your email', True, True)
    firebaseauth = firebase.FirebaseApplication('db url', authentication)
    return firebaseauth
               
def pushToFirebase(symbol, f):    
    try:    
        df = quandl.get("WIKI/%s" %(symbol),start_date="2006-01-01", end_date=date.today())
    except:
        print 'error'
        return
    df = df[['Open',  'High',  'Low',  'Close', 'Volume']]
    high = 55
    mid = 34
    low = 11
    df['rollinghigh2'] = df['Close'].rolling(window = high, center=False).mean()
    df['rollinghigh'] = df['Close'].rolling(window = mid, center=False).mean()
    df['rollinglow'] = df['Close'].rolling(window = low, center=False).mean()
    df.dropna()
    will = talib.WILLR(np.asarray(df.High.astype(float)), np.asarray(df.Close.astype(float)), np.asarray(df.Low.astype(float)), timeperiod = 5)[-1]
    trix = talib.TRIX(np.asarray(df.Close.astype(float)), timeperiod = 28)[-1]
    rsi = talib.RSI(np.asarray(df.Close.astype(float)), timeperiod = 28)[-1]
    chaik = talib.ADOSC(np.asarray(df.High.astype(float)), np.asarray(df.Close.astype(float)), np.asarray(df.Low.astype(float)), np.asarray(df.Volume.astype(float)), fastperiod=4, slowperiod=16)[-1]
    regangle = talib.LINEARREG_ANGLE(np.asarray(df.Close.astype(float)), timeperiod=14)[-1]
    timeforcaste = talib.TSF(np.asarray(df.Close.astype(float)), timeperiod=27)[-1]
    avrange = talib.ATR(np.asarray(df.High.astype(float)),np.asarray(df.Close.astype(float)), np.asarray(df.Low.astype(float)), timeperiod=23)[-1]
    data = {'55dayAvg': df['rollinghigh2'][-1],
            '34dayAvg': df['rollinghigh'][-1],
            '11dayAvg': df['rollinglow'][-1],
            'willR': will,
            'trix': trix,
            'rsi': rsi,
            'volumeInd': chaik,
            'regAngle' : regangle,
            'forcast': timeforcaste,
            'avgRange': avrange,
            'lastOpen': df['Open'][-1],
            'lastHigh': df['High'][-1],
            'lastLow': df['Low'][-1],
            'lastClose': df['Close'][-1]
            }
    try:    
        f.put('symbols', symbol, data)
        print "success", symbol
        return
    except:
        print 'firebaseError'
        return


        



        

                    
def updateDB():
    tok = authUser()
    for x in symbols(): 
            pushToFirebase(x, tok)


updateDB()