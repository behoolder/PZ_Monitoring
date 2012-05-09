#-*- coding: utf-8 -*-

from sensorHTTP import SensorHTTP
import urllib
import urllib2

class Sensor:
    '''
    Klasa uruchamiająca sensor, sprawdza połaczenie z monitorem i w zależności od wyniku, uruchamia właściwe działanie sensora, lub nie.
    '''
    
    def __init__(self, sensor_port, monitor_address):
        '''
        Konstruktor klasy Sensor.\n
        
        sensor_port     - port na którym uruchomiony zostanie sensor\n
        monitor_address - Adres IP monitora, który będzie komunikować sie z sensorem (IP:PORT)\n
        '''
        
        self.sensor_port     = sensor_port
        self.monitor_address = monitor_address
        self.shttp           = SensorHTTP(self.sensor_port)
        
    def start(self):
        '''
        Inicjuje działanie sensora, sprawdza czy monitor istnieje.
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
