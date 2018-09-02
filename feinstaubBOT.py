#!/usr/bin/env python
# -*- coding: utf-8 -*-
# depends: python-requests

import json
import time
import requests
import tweepy
import configparser

import logging
logger = logging.getLogger('feinstaub')
hdlr = logging.FileHandler('/var/tmp/feinstaub.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.DEBUG)



def pick_values(sensor):
        # Sensordaten für SDS011 und DHT11 abfragen
        # dazu die api von luftdaten.info nutzen
        # Peter Fürle @Alpensichtung Hotzenwald 04/2017
        r = requests.get(sensor)
        json_string = r.text
        parsed_json = json.loads(json_string)
        # pretty print um überhaupt zu verstehen was da passiert
        #print json.dumps(parsed_json, sort_keys=True, indent=4, separators=(',',':'))
        l = len(parsed_json)-1
        if l:
                try:
                        b = len(parsed_json[l]['sensordatavalues'])
                except IndexError:
                        a = "0"
                else:
                        a = len(parsed_json[l]['sensordatavalues'])
		
    
                if a == 1:
                        result=(parsed_json[l]['sensordatavalues'][0]['value'])
                        return(result)
                if a == 2:
                        result=(parsed_json[l-1]['sensordatavalues'][0]['value'])
                        result2=(parsed_json[l]['sensordatavalues'][1]['value'])

                        wert1 = result
                        wert2 = result2
                        return(result)

        return (0)


def pick_2values(sensor):
        # Sensordaten für SDS011 und DHT11 abfragen
        # dazu die api von luftdaten.info nutzen
        # Peter Fürle @Alpensichtung Hotzenwald 04/2017
        r = requests.get(sensor)
        json_string = r.text
        parsed_json = json.loads(json_string)
        # pretty print um überhaupt zu verstehen was da passiert
        #print json.dumps(parsed_json, sort_keys=True, indent=4, separators=(',',':'))
        l = len(parsed_json)-1
        if l:
                try:
                        b = len(parsed_json[l]['sensordatavalues'])
                except IndexError:
                        a = "0"
                else:
                        a = len(parsed_json[l]['sensordatavalues'])


                if a == 1:
                        result=(parsed_json[l]['sensordatavalues'][0]['value'])
                        return (result)

                if a == 2:
                        result=(parsed_json[l-1]['sensordatavalues'][0]['value'])
                        result2=(parsed_json[l]['sensordatavalues'][1]['value'])

                        wert1 = result
                        wert2 = result2
                        return (result2)

                if a == 4:
                        return (0)

        return (0)



# Sensornummern, einfach neu dazugekommene hier an die Liste dranh  ngen
sd = [691, 761, 996, 1262, 1569, 1575, 2856, 3111, 3177, 3423, 3731, 3777, 3945, 4585, 5065, 5497, 6326, 6699, 6761, 7098, 8228, 9469, 10643, 11054, 11799, 11976, 12954, 13102, 13415, 13656, 13728, 15268, 16027, 16173,]

maxlist = []
for x in sd:
        print(x)
        xx = x + 1
        url1 = 'http://api.luftdaten.info/static/v1/sensor/' + str(x) + '/'
        url2 = 'http://api.luftdaten.info/static/v1/sensor/' + str(xx) + '/'
    
        tweetx = pick_values(url1)
        try:
                tweetx = tweetx + " " + pick_values(url2)
        except TypeError:
                tweetx = tweetx
                #logger.error('%s Keine Sonsordaten' %(x))
        else:
                tweetx = tweetx + " " + pick_values(url2)
        tweetz = pick_values(url1)
        tweett = pick_2values(url2)
    

        tweet_p1 = pick_values(url1)
        tweet_p2 = pick_2values(url1)
    
        try:
                tweet_t = pick_values(url2)
        except TypeError:
                logger.error('%s Keine Temperatursensordaten'  %(xx))
                tweet_t = "0"
        else:
                tweet_t = pick_values(url2)

        try:
                tweet_h = pick_2values(url2)
        except TypeError:
                logger.error('%s Keine Luftfeuchtigkeitssensordaten'  %(xx))
                tweet_h = "0"
	
        else:
                tweet_h = pick_2values(url2)

        if tweetx != 0:
		

                dattime = (time.strftime("%H:%M %d.%m.%Y")) 

	
        
                p10 = float(tweet_p1)
        
                p25 = float(tweet_p2)
        
	
                if not tweet_t == 0:
                        t = tweet_t
	    
                if tweet_t == 0:
	                logger.info('%s Keine Temperatursensordaten'  %(xx))
                if not tweet_h == 0:
                        h = tweet_h

                if tweet_h == 0:
                        logger.info('%s Keine Luftfeuchtigkeitssensordaten'  %(xx))
	        
                alarm = False
	        # hier kannst du den Maxwert anpassen
                tweettext = ""
                if 30 < p10 < 50:
                        tweettext = '⚠️ Vorsicht Frankfurt !!! \n{} \nFeinstaubwert erhöht\n- Sensor: {} ist bei {} µg/m³ PM10 ({} µg/m³ PM2,5)\n- aktuelle Feinstaub und Temperaturwerte des Sensor: https://feinstaub.rexfue.de/{} \n- Mach mit! Mehr Infos auf https://luftdaten.info'.format(dattime, x, p10,p25,x)
                        # hier den Tweet ausloesen
                        alarm = True

                if 50 < p10 < 100:
                        tweettext = '⚠️ Achtung Frankfurt !!! \n{} \nFeinstaubwert hoch\n- Sensor: {} ist bei {} µg/m³ PM10 ({} µg/m³ PM2,5)\n- aktuelle Feinstaub und Temperaturwerte des Sensor: https://feinstaub.rexfue.de/{} \n- Mach mit! Mehr Infos auf https://luftdaten.info'.format(dattime, x, p10,p25,x)
                        # hier den Tweet ausloesen
                        alarm = True

                if p10 > 100:
                        tweettext = '⚠  ⚠  ⚠️ Achtung Frankfurt !!! ⚠  ⚠  ⚠  \n{} \nFeinstaubwert sehr hoch\n- Sensor: {} ist bei {} µg/m³ PM10 ({} µg/m³ PM2,5)\n- aktuelle Feinstaub und Temperaturwerte des Sensor: https://feinstaub.rexfue.de/{} \n- Mach mit! Mehr Infos auf https://luftdaten.info'.format(dattime, x, p10,p25,x)
                        # hier den Tweet ausloesen
                        alarm = True
                logger.info('%s P10 = %s P2,5 = %s'  %(xx, p10, p25 ))
		
        if tweetx == 0:
                logger.error('%s Keine Sonsordaten'  %(x))
		
        print (tweettext)

	# Twitter acess tokens laden
	config = configparser.ConfigParser()
	config.readfp(open(r'feinstaubBot.cfg'))

	CONSUMER_KEY = config.get('twitter-config', 'CONSUMER_KEY')
	CONSUMER_SECRET = config.get('twitter-config', 'CONSUMER_SECRET')
	ACCESS_KEY = config.get('twitter-config', 'ACCESS_KEY')
	ACCESS_SECRET = config.get('twitter-config', 'ACCESS_SECRET')
	
        # OAuth process, using the keys and tokens
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

        # Creation of the actual interface, using authentication
        api = tweepy.API(auth)

        # twittern nur Text
        if alarm:
                api.update_status(status=tweettext)
