#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 20 11:03:45 2017

@author: nickwilliams
"""
from yahoo_finance import Share
import bs4 as bs
import requests
import re




def get_symbols():
    resp = requests.get('https://www.quandl.com/api/v3/datatables/WIKI/PRICES.json?date=20160912&api_key=iExJMAAAhsyQz3vTmgaq')
    soup = str(bs.BeautifulSoup(resp.text))
    ticks = re.findall("([A-Z]{2,})", soup)
    return ticks
    
def savesyms():
    with open('wikisyms.txt', 'w') as f:
        f.write('symbols\n')
        symbols = get_symbols()
        for i in range(0, len(symbols)):
            f.write('%s\n' %(symbols[i]))
