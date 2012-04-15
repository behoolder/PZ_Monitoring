from sensorHTTP import SensorHTTP
import urllib
import urllib2

class Sensor:
    '''
    Klasa uruchamiajaca sensor, sprawdza polaczenie z monitorem i w zaleznosci od wyniku, uruchamia wlasciwe dzialanie sensora, lub nie.
    '''
    
    def __init__(self, sensor_port, monitor_address):
        self.sensor_port     = sensor_port
        self.monitor_address = monitor_address
        
    def start(self):
        try :
            d = {'port' : self.sensor_port}

            data     = urllib.urlencode(d)
            request  = urllib2.Request("http://" + self.monitor_address + "/register/", data)
            response = urllib2.urlopen(request)

            self.monitor_id = response.read()

        except Exception, e:
            print 'Nie ma polaczenia z monitorem na adresie: ', self.monitor_address
            print 'Informacje o bledach:'
            print str(e)
            exit()
    
        else :
            if response.code == 200:
                shttp = SensorHTTP(self.sensor_port, self.monitor_id)
                shttp.start()
            else:
                print 'Brak odpowiedzi monitora'
                exit()

if __name__ == "__main__":
    pass