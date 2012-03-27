import urllib2
import time
import uuid
from threading import Thread
from flask import request
from flask import Flask

class Monitor(Thread):

    def __init__(self, delay = 5):
        Thread.__init__(self)
        self.sensors = {}
        self.delay = delay

        #Wygenerowanie ID
        self.id = uuid.uuid1()

    def add_sensor(self, host, port):
        self.sensors[(host, port)] = ''
        print "Sensor %s:%s pomyslnie zarejestrowany"%(host, port)

    def keep_alive(self):
        scp = self.sensors.copy()
        for (host, port) in scp:
            try:
                f = urllib2.urlopen("http://%s:%s/keepalive/"%(host, port))
                
                if f.msg != "OK" or f.code != 200:
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

    def start(self, debug = False):
        MonitorHTTP.monitor.start()
        MonitorHTTP.app.debug = debug
        MonitorHTTP.app.run(host = "0.0.0.0", port = self.port)


if __name__ == "__main__":
    pass
