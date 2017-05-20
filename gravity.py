# -*- coding: utf-8 -*-
"""
Created on Sat Jan 14 16:58:03 2017

@author: Nick
"""
import matplotlib   
import matplotlib.pyplot as plt
from math import pow
import ephem
from datetime import date, timedelta, datetime 
from yahoo_finance import Share



indexplanets = ('moon', 'mercury', 'saturn', 'jupiter', 'neptune', 'uranus',
    'venus','mars')
    
def dateparse(date):
    date = str(date)
    return date.replace('-','/')
   
    
def planet_dist(date, planet):
    planets = {'mars':ephem.Mars(date), 'mercury':ephem.Mercury(date), 'saturn':ephem.Saturn(date), 'jupiter':ephem.Jupiter(date),
               'neptune':ephem.Neptune(date), 'uranus':ephem.Uranus(date), 'venus':ephem.Venus(date), 
               'moon':ephem.Moon(date), 'sun':ephem.Sun(date)}
    p = planets[planet]
    p.compute() 
    return p.earth_distance

def dist_to_earth(dist, planet):
    coredist = {'jupiter':(6.98*pow(10,7)),'moon':(1.71*pow(10,6)),
                'saturn': (120.984*pow(10,6))/2, 'mercury': (48.79*pow(10,5))/2,
                'mars': (6.792*pow(10,6))/2, 'venus': (12.104*pow(10,6))/2,
                'uranus': (51.18*pow(10,6))/2, 'neptune': 24.764*pow(10,6)}
    return (dist + coredist[planet]+(6.38*pow(10,6)))                               #Third value is dist to earths center

def pull(date, planet):
    coredist = dist_to_earth(planet_dist(date,planet),planet)
    massdict = {'earth': (5.98*pow(10,24)), 'moon':(7.34*pow(10,22)), 'jupiter':(1.901*pow(10,27)),
                'saturn': (568*pow(10,24)), 'neptune': 102*pow(10,24), 'uranus':86.2*pow(10,24),
                'venus': (4.87*pow(10,24)), 'mars': 0.642*pow(10,24), 'mercury': 0.33*pow(10,24)}
    g = 6.673 * pow(10,-11)
    pull = ((g*massdict['earth']*massdict[planet])/pow(coredist,2))
    return pull

def avg_pull(date, days, planet):
    total = 0 
    count = days
    for x in range(0,days):
        total+=pull((date - timedelta(days=x)), planet)
        #print total
    return total/count
  
def avg_pull_30():
    total = {'moon': 0, "jupiter": 0}
    count = 0
    for x in range(1,30):
        count +=1
        day = dateparse(date.today() + timedelta(days=x))
        for p in indexplanets:
            if p == 'moon' or p == 'jupiter':
                total[p] += pull(day, p)
    avg = {'moon': (total['moon']/count), 'jupiter':(total['jupiter']/count)}
    return avg

def get_history(symbol):
    stock = Share(symbol).get_historical(str((date.today()-timedelta(days=4000))), str(date.today()))
    return stock
  


#matplotlib.use('TkAgg')
#fig = plt.figure()
# make up some data
#x = [(date.today()-timedelta(days=347)) + timedelta(days = i) for i in range(1,343)]
'''
spy = get_history('SPY')

x2 = []
for d in range(len(spy)):
    graphd = datetime.strptime(spy[d]['Date'], '%Y-%m-%d').date()
    x2.append(graphd)
y3 = [spy[d]['Close'] for d in range(0,len(spy))]
plt.subplot(len(indexplanets)+1,1,1)
plt.plot(x2[49:],y3[49:])
plt.title('XLE close')
# beautify the x-labels
plt.gcf().autofmt_xdate()
plotcount = 2
for i in range(0,len(indexplanets)):
    plt.subplot(len(indexplanets)+1,1,(plotcount+i))
    y = [pull(d,indexplanets[i]) for d in x2]
    y2 = []
    x3 = []
    for p in range(49,len(y)):
        total = 0
        count = 0
        for m in range(0,50):
            total += y[p-m]
            count +=1
        print count
        avg = total/50.0
        y2.append(avg)
        x3.append(x2[p])
    print len(x3), len(y[49:])
    plt.plot(x3,y[49:],'r', x3,y2,'g')
    plt.title('%s gravitational pull on earth based on daily distance' %(indexplanets[i]))
    plt.gcf().autofmt_xdate()
'''
# plot
#plt.plot(x2,y1)
#plt.title('Saturn gravitational pull on earth based on daily distance')
#plt.gcf().autofmt_xdate()
#plt.subplot(3,1,2)
#plt.plot(x2,y2)
#plt.title('Moon gravitational pull on earth based on daily distance')
#plt.gcf().autofmt_xdate()


#plt.show()
