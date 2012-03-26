#!/usr/bin/env python

from flask import request
from flask import Flask
from sensor.sensor import get_sensor
from sys import argv
import urllib
import urllib2

if len(argv) < 3 :
    print "Brakujacy parametr podczas uruchomienia!"
    print "%s [port sensora] [adres i port monitora]" % (argv[0])
    exit()

sensor_port     = argv[1]
monitor_address = "http://" + argv[2] + "/register/"

try :
    d = {'port' : sensor_port}

    data     = urllib.urlencode(d)
    request  = urllib2.Request(monitor_address, data)
    response = urllib2.urlopen(request)
    html     = response.read()

except Exception, e:
    print 'Nie ma polaczenia'
    print str(e)
    exit()
    
else :
    if str(html) == 'OK' :
        app = Flask(__name__)

        @app.route("/")
        def index():
            return 'Serwer HTTP dziala'

        @app.route("/keepalive/")
        def keepalive():
            return 'OK'	
	
        @app.route("/get_data/")
        def get_data():
            try:
                a = get_sensor().get_data().get_str_info()
            except Exception, e:
                print e
            else:
                return a

        app.run(host = '0.0.0.0', port = int(sensor_port))
		
    else :
        exit()