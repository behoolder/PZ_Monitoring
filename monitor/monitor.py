import urllib2
import time
from threading import Thread

class Monitor(Thread):

    def __init__(self, delay = 5):
        Thread.__init__(self)
        self.sensors = {}
        self.delay = delay

    def add_sensor(self, host, port):
        self.sensors[host] = port

    def keep_alive(self):
        scp = self.sensors.copy()
        for key in scp:
            try:
                f = urllib2.urlopen("http://%s:%s/keepalive/"%(key,self.sensors[key]))

                if f.msg != "OK" or f.code != 200:
                    self.sensors.pop(key)

                print "Sensor %s:%s dziala poprawnie"%(key, self.sensors[key])

            except Exception, e:
                print "Sensor %s:%s nie odpowiada"%(key, self.sensors[key])
                print e
                self.sensors.pop(key)
                continue

    def run(self):
        while True:
            self.keep_alive()
            time.sleep(self.delay)

    def get_sensors(self):
        return str(self.sensors).replace('\'', '"')

