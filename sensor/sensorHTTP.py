from flask import request
from flask import Flask
from sensor import Sensor
from sys import argv
import urllib
import urllib2
'''
Klasa obslugujaca dzialanie serwera HTTP sensora
'''
class SensorHTTP:

    sensor = Sensor()

    def __init__(self, sensor_port, monitor_address):
        self.sensor_port     = sensor_port
        self.monitor_address = "http://" + monitor_address + "/register/"
        
    def start(self, debug = False):
        try :
            d = {'port' : self.sensor_port}

            data     = urllib.urlencode(d)
            request  = urllib2.Request(self.monitor_address, data)
            response = urllib2.urlopen(request)
            html     = response.read()

        except Exception, e:
            print 'Nie ma polaczenia'
            print str(e)
            exit()
    
        else :
            if response.code == 200 :
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
                        a = self.sensor.get_sensor().get_data().get_str_info()
                    except Exception, e:
                        print e
                    else:
                        return a

                app.run(host = '0.0.0.0', port = int(self.sensor_port))
        
            else :
                exit()

if __name__ == "__main__":
    pass
