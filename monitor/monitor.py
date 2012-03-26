import urllib2
import time
from threading import Thread
from flask import request
from flask import Flask

class Monitor(Thread):

    def __init__(self, delay = 5):
        Thread.__init__(self)
        self.sensors = {}
        self.delay = delay

    def add_sensor(self, host, port):
        self.sensors[host] = port

    def keep_alive(self):
        sensors_cp = self.sensors.copy()
        for key in sensors_cp:
            try:
                f = urllib2.urlopen("http://%s:%s/keepalive/"%(key,self.sensors[key]))

                if f.msg != "OK" or f.code != 200:
                    self.sensors.pop(key)

                print "Sensor %s:%s jest OK"%(key, self.sensors[key])

            except Exception, e:
                print "Sensor %s:%s nie odpowiada"%(key, self.sensors[key])
                print e
                self.sensors.pop(key)
                continue

    def run(self):
        while True:
            self.keep_alive()
            time.sleep(self.delay)

    def get(self, uri):
        #f = urllib2.urlopen("http://" + self.sensors + "/" + uri)
        self.response = f.read()
        return self.response

monitor = Monitor()
monitor.start()

app = Flask(__name__)

@app.route('/register/', methods=['POST'])
def register():
    monitor.add_sensor(str(request.remote_addr), "5000")
    return 'OK'

app.run(host = "0.0.0.0", port = 5001)

#print c.get(0, "get_data/")
