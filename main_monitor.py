from sys import argv
from monitor import Monitor
from flask import request
from flask import Flask

if len(argv) < 2 :
    print "Brakujacy parametr podczas uruchomienia!"
    print "%s [port]"%(argv[0],)
    exit()

monitor = Monitor()

#Uruchomienie monitora
#monitor.start()

app = Flask(__name__)

@app.route('/sensors/', methods=['GET'])
def register():
    return monitor.get_sensors()

@app.route('/register/', methods=['POST'])
def register():
    monitor.add_sensor(str(request.remote_addr), "5000")
    return 'OK'

#Uruchomienie serwera http
if __name__ == "__main__":
    app.debug = True
    app.run(host = "0.0.0.0", port = int(argv[1]))

