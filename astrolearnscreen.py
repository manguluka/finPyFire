#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 18 01:15:39 2017

@author: Nick
"""

import pandas as pd
from yahoo_finance import Share
import quandl 
import math
from sklearn import preprocessing, cross_validation, svm
from sklearn.linear_model import LinearRegression, Ridge
import numpy as np
from gravity import pull, avg_pull
import ephem
from datetime import date, timedelta, datetime 
from getsyms import get_symbols

quandl.ApiConfig.api_key = 'your api key'
quandl.ApiConfig.api_version = '2015-04-09'

def get_3_18():
    data = pd.read_csv('easyp_3_18.txt')
    return data

def illuminated(date, planet):
    planets = {'mars':ephem.Mars(date), 'mercury':ephem.Mercury(date), 'saturn':ephem.Saturn(date), 'jupiter':ephem.Jupiter(date),
               'neptune':ephem.Neptune(date), 'uranus':ephem.Uranus(date), 'venus':ephem.Venus(date), 
               'moon':ephem.Moon(date), 'sun':ephem.Sun(date)}
    p = planets[planet]
    return p.phase
def planetconst(date, planet):
    planets = {'mars':ephem.Mars(date), 'mercury':ephem.Mercury(date), 'saturn':ephem.Saturn(date), 'jupiter':ephem.Jupiter(date),
               'neptune':ephem.Neptune(date), 'uranus':ephem.Uranus(date), 'venus':ephem.Venus(date), 
               'moon':ephem.Moon(date), 'sun':ephem.Sun(date)}
    p = planets[planet]
    return ephem.constellation(p)[1]   
def symbols():
    full = []
    with open('wikisyms.txt', 'r') as f:
        
        for i in range(1,len(get_symbols())):
            full.append(f.readline(i)[:-1])
    #full = full[5:]
    #full = [x for x in full if x != '']
    return full
    
def gravitycols(data, dates):
    planets = ('moon', 'mercury', 'saturn', 'jupiter')
    avg = 50
    for p in planets:
        illum = [illuminated(d, p) for d in dates]
        se2 = pd.Series(illum)
        data['%s illuminations' %(p)] = se2.values
        dif = [diff(pull(d, p),avg_pull(d,avg, p))/100000 for d in dates]
        se3 = pd.Series(dif)
        data['%s grav_difference' %(p)] = se3.values
        elong = [planetelong(d, p) for d in dates]
        se4 = pd.Series(elong)
        data['%s grav_difference' %(p)] = se4.values    
    
def diff(x,y):
    return x-y

def planetelong(date, planet):
    planets = {'mars':ephem.Mars(date), 'mercury':ephem.Mercury(date), 'saturn':ephem.Saturn(date), 'jupiter':ephem.Jupiter(date),
               'neptune':ephem.Neptune(date), 'uranus':ephem.Uranus(date), 'venus':ephem.Venus(date), 
               'moon':ephem.Moon(date), 'sun':ephem.Sun(date)}
    p = planets[planet]
    return p.elong
    
#five_daysf = [date.today()+timedelta(days=i) for i in range(0,6)]

               
def getscore_getnext(symbol, days_ahead):
    try:
        df = quandl.get("WIKI/%s" %(symbol),start_date="2015-01-01", end_date=date.today())
    except:
        print 'error'
        return
    df = df[['Open',  'High',  'Low',  'Close', 'Volume']]

    high = 32
    mid = 16
    low = 4

    gravitycols(df, df.index)

    df['rollinghigh2'] = df['Close'].rolling(window = high, center=False).mean()
    df['rollinghigh'] = df['Close'].rolling(window = mid, center=False).mean()
    df['rollinglow'] = df['Close'].rolling(window = low, center=False).mean()
    if (df['rollinglow'][-1]>df['rollinghigh'][-1]):
        forecast_val = days_ahead

        forecast_col = 'Close'
        df.fillna(value=-99999, inplace=True)
        df['label'] = df[forecast_col].shift(-forecast_val)




        #X = X[:-forecast_val]



        X = np.array(df.drop(['label'], 1))
        
        X = preprocessing.scale(X)



        futureX = X[-1:]
        X = X[:-forecast_val]
        df.dropna(inplace=True)
            
        y = np.array(df['label'])
            
        X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.15)
            
        clf = LinearRegression(n_jobs=1)
            
        clf.fit(X_train, y_train)
            
        confidence = clf.score(X_test, y_test)
        #print "accuracy with 1.0 being perfect:", (confidence)
        futureval = clf.predict(futureX)
        return (confidence, futureval)
        #print 'last price:', quandl.get("WIKI/%s.4" %(symbol), rows=1)
        #print 'next %d close prices for %s' %(forecast_val, symbol), futureval
    else: 
        pass 

slist = []
'''
with open('easyp_13_18.txt', 'w') as f:
    f.write('symbol,score,percent_change,next_price\n')
    for x in symbols():
        try:    
            last = float(quandl.get("WIKI/%s.4" %(x), rows=1)['Close'])
        except:
            print 'error'
            pass
        if 13 < last <18:
            p = getscore_getnext(x, 2)
            if type(p) == tuple:
                per = ((last-p[1])/last)*100
                if (p[1]>10):
                    print x,'last', last, 'next', p[1], 'score', p[0]
                    f.write('%s,%f,%f,%f\n' % (x, p[0], per, p[1]))
'''
                    
def pricefilter(p1,p2):
    with open('%s_%s.txt'%(p1,p2), 'w') as f:
        f.write('symbol,score,percent_change,next_price\n')
        for x in symbols():
            try:    
                last = float(quandl.get("WIKI/%s.4" %(x), rows=1)['Close'])
                if p1 < last < p2:
                    print'%s' %(x)
                    p = getscore_getnext(x, 1)
                    if type(p) == tuple:
                        per = ((p[1]-last)/last)*100
                        if (p[0] > 0.99) and (per>0.0):
                            print x,'last', last, 'next', p[1], 'score', p[0], per
                            f.write('%s,%f,%f,%f\n' % (x, p[0], per, p[1]))
                        else: pass
            except:
                print 'error'
                pass
pricefilter(5,10)
