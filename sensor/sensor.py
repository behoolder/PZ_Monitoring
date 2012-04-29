from sensorHTTP import SensorHTTP
import urllib
import urllib2

class Sensor:
    '''
    Klasa uruchamiajaca sensor, sprawdza polaczenie z monitorem i w zaleznosci od wyniku, uruchamia wlasciwe dzialanie sensora, lub nie.
    '''
    
    def __init__(self, sensor_port, monitor_address):
        '''
        Konstruktor klasy Sensor
        
        sensor_port     - port na ktorym uruchomiony zostanie sensor
        monitor_address - Adres IP monitora, ktory bedzie komunikowac sie z sensorem (IP:PORT)
        '''
        
        self.sensor_port     = sensor_port
        self.monitor_address = monitor_address
        self.shttp           = SensorHTTP(self.sensor_port)
        
    def start(self):
        '''
        Inicjuje dzialanie sensora, sprawdza czy monitor istnieje
        '''
        
        try :
            d = {'port' : self.sensor_port}
            m = self.shttp.get_metrics()
            
            for key in m.keys():
                d[key] = m[key]

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
                self.shttp.add_monitor_id(self.monitor_id)
                self.shttp.start()
            else:
                print 'Brak odpowiedzi monitora'
                exit()

if __name__ == "__main__":
    pass
