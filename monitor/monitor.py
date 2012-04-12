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
        self.metric = metric
        self.sensor = sensor

    def get_metric(self):
        return self.metric

    def get_sensor(self):
        return self.sensor

    
class Monitor(Thread):

    def __init__(self, delay = 5):
        Thread.__init__(self)
        self.sensors = {}
        self.delay = delay
        self.subscriptions = {}

        #Wygenerowanie ID
        self.id = uuid.uuid1()

    def add_sensor(self, host, port):
        self.sensors[(host, port)] = ''
        print "Sensor %s:%s pomyslnie zarejestrowany"%(host, port)

    def keep_alive(self):
        scp = self.sensors.copy()
        for (host, port) in scp:
            try:
                response = urllib2.urlopen("http://%s:%s/keepalive/"%(host, port))
                
                if response.msg != "OK" or response.code != 200:
                    self.sensors.pop((host, port))
                    
                print "Sensor %s:%s dziala poprawnie"%(host, port)
                        
            except Exception, e:
                print "Sensor %s:%s nie odpowiada"%(host, port)
                print e
                self.sensors.pop((host, port))
                continue

    def run(self):
        while True:
            self.keep_alive()
            time.sleep(self.delay)

    def get_sensors(self):
        return str(self.sensors.keys()).replace('\'', '"')

    def get_id(self):
        return str(self.id)

    def create_subscription(self, metric, sensor): 
        self.subscriptions[len(self.subscriptions) + 1] = Subscription(metric, sensor)
        return len(self.subscriptions)

    def get_data(self, sid): 
        if not sid in self.subscriptions:
            raise KeyError

        host, port = self.subscriptions[sid].get_sensor()
        ret = []

        for metric in self.subscriptions[sid].get_metric():
            request  = urllib2.Request("http://%s:%s/%s/"%(host, port, metric), urllib.urlencode({'id' : self.id}))
            response = urllib2.urlopen(request)

            if response.code == 200:
                ret.append(response.msg)

        return ret

class MonitorHTTP:

    app = Flask("monitor")
    monitor = Monitor()
    
    def __init__(self, port):
        self.port = port

    @app.route('/sensors/', methods=['GET'])
    def sensors():
        return MonitorHTTP.monitor.get_sensors()

    @app.route('/register/', methods=['POST'])
    def register():
        MonitorHTTP.monitor.add_sensor(str(request.remote_addr), request.form["port"])
        return MonitorHTTP.monitor.get_id()

    @app.route('/subscribe/', methods=['GET']) #TODO: POST!
    def subscribe():
        sid = MonitorHTTP.monitor.create_subscription(['cpu', 'ram'], ('localhost', '5001')) #TODO: POST info
        return redirect('/subscriptions/' + str(sid) + '/')

    @app.route('/subscriptions/<sid>/', methods=['GET'])
    def subscriptions(sid):
        try:
            data = MonitorHTTP.monitor.get_data(int(sid))
        except Exception, e:
            print e
            abort(404)
        else:
            return "".join(data, '\n')

    def start(self, debug = False):
        MonitorHTTP.monitor.start()
        MonitorHTTP.app.debug = debug
        MonitorHTTP.app.run(host = "0.0.0.0", port = self.port)


if __name__ == "__main__":
    pass
