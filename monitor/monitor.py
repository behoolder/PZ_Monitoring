import urllib
import urllib2
import time
import uuid
from threading import Thread
from flask import Flask, request, redirect, abort

class Subscription:
    """
    Klasa ta jest zwyklym kontenerem dla subskrypcji.
    """

    def __init__(self, metric, sensor):
        """
        Konstruktor klasy Subscription.

        metric - monitorowane metryki
        sensor - adres wraz z portem sensora
        """
        
        self.metric = metric
        self.sensor = sensor

    def get_metric(self):
        """
        Zwraca metryki wybrane w subskrypcji.
        """
        
        return self.metric

    def get_sensor(self):
        """
        Zwraca adres i port sensora.
        """
        
        return self.sensor

    
class Monitor(Thread):
    """
    Klasa monitora. Przechowuje ona informacje na temat zarejestrowanych sensorow oraz utworzonych subskrypcji.
    """

    def __init__(self, delay = 5):
        """
        Konstruktor klasy Monitor.

        delay - opoznienie z jakim wywolywane jest 'keep alive' do sensorow
        """
        Thread.__init__(self)
        self.sensors = {}
        self.delay = delay
        self.subscriptions = {}

        #Wygenerowanie ID
        self.id = uuid.uuid1()

    def add_sensor(self, host, port):
        """
        Rejestruje nowy sensor.

        host - adres sensora
        port - port sensora
        """

        self.sensors[(host, port)] = ''
        print "Sensor %s:%s pomyslnie zarejestrowany"%(host, port)

    def keep_alive(self):
        """
        Sprawdza czy wszystkie zarejestrowane sensory sa nadal wlaczone i sprawne.
        Jesli ktorys z sensorow nie odpowiada to zostaje on wyrzucony z listy.
        """

        scp = self.sensors.copy()
        for (host, port) in scp:
            try:
                response = urllib2.urlopen("http://%s:%s/keepalive/"%(host, port))
                
                if response.msg != "OK" or response.code != 200:
                    print "Sensor %s:%s nie odpowiada"%(host, port)
                    self.sensors.pop((host, port))
                    continue
                    
                print "Sensor %s:%s dziala poprawnie"%(host, port)
                        
            except Exception, e:
                print "Sensor %s:%s nie odpowiada"%(host, port)
                print e
                self.sensors.pop((host, port))
                continue

    def run(self):
        """
        Uruchamia keep_alive() w osobnym watku.
        """

        while True:
            self.keep_alive()
            time.sleep(self.delay)

    def get_sensors(self):
        """
        Zwraca wszystkie zarejestrowane sensory.
        """

        return str(self.sensors.keys()).replace('\'', '"')

    def get_id(self):
        """
        Zwraca ID monitora.
        """

        return str(self.id)

    def create_subscription(self, metric, sensor): 
        """
        Tworzy nowa subskrypcje.

        metric - monitorowane metryki
        sensor - monitorowany sensor
        """

        self.subscriptions[len(self.subscriptions) + 1] = Subscription(metric, sensor)
        return len(self.subscriptions)

    def get_data(self, sid): 
        """
        Zwraca dane z sensora.

        sid - numer subskrypcji
        """

        if not sid in self.subscriptions:
            raise KeyError

        host, port = self.subscriptions[sid].get_sensor()
        ret = []

        for metric in self.subscriptions[sid].get_metric():
            request  = urllib2.Request("http://%s:%s/%s/"%(host, port, metric), urllib.urlencode({'id' : self.id}))
            response = urllib2.urlopen(request)

            if response.code == 200:
                ret.append(response.read())

        return ret


class MonitorHTTP:
    """
    Klasa serwera HTTP dla monitora.
    """

    app = Flask("monitor")
    monitor = Monitor()
    
    def __init__(self, port):
        """
        Konstruktor klasy MonitorHTTP.

        port - port na ktorym ma zostac uruchomiony serwer
        """

        self.port = port

    @app.route('/sensors/', methods=['GET'])
    def sensors():
        """
        Zwraca informacje o zarejestrowanych w monitorze sensorach.
        Dostep: GET
        """

        return MonitorHTTP.monitor.get_sensors()

    @app.route('/register/', methods=['POST'])
    def register():
        """
        Rejestruje nowy sensor w monitorze.
        Dostep: POST
        """

        MonitorHTTP.monitor.add_sensor(str(request.remote_addr), request.form["port"])
        return MonitorHTTP.monitor.get_id()

    @app.route('/subscribe/', methods=['GET']) #TODO: POST!
    def subscribe():
        """
        Tworzy nowa subskrypcje.
        Dostep: POST
        """

        sid = MonitorHTTP.monitor.create_subscription(['cpu', 'ram'], ('localhost', '5001')) #TODO: POST info
        return redirect('/subscriptions/' + str(sid) + '/')

    @app.route('/subscriptions/<sid>/', methods=['GET'])
    def subscriptions(sid):
        """
        Zwraca odpowiednie dane z sensora przypisane do konkretnej subskrypcji.

        sid - numer subskrypcji
        """

        try:
            data = MonitorHTTP.monitor.get_data(int(sid))
        except Exception, e:
            print e
            abort(404)
        else:
            return "".join(data)

    def start(self, debug = False):
        """
        Uruchamia monitor oraz serwer HTTP.
        
        debug - ustala czy serwer HTTP ma byc uruchomiony w trybie debugowania.
        """

        MonitorHTTP.monitor.start()
        MonitorHTTP.app.debug = debug
        MonitorHTTP.app.run(host = "0.0.0.0", port = self.port)


if __name__ == "__main__":
    pass
