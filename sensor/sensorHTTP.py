from flask import request
from flask import Flask
import os

class SensorHTTP:
    '''
    Klasa obslugujaca dzialanie serwera HTTP sensora
    '''

    app             = Flask(__name__)
    monitor_id_list = []
    sensor          = None

    def __init__(self, sensor_port, monitor_id):
        self.sensor_port = sensor_port

        SensorHTTP.monitor_id_list.append(monitor_id)
        
        if os.name == 'posix':
            from linux.linux import Linux
            SensorHTTP.sensor = Linux()
        elif os.name == 'nt':
            from windows.windows import Windows
            SensorHTTP.sensor = Windows()
        else :
            print 'Nie rozpoznano systemu, sensor zostanie wylaczony.'
            exit()        

    @app.route("/keepalive/", methods=['GET'])
    def keepalive():
        return 'OK'  

    @app.route("/cpu/", methods=['POST'])
    def get_cpu():
        SensorHTTP.check_monitor_id(request.form["id"])
        return str(SensorHTTP.sensor.cpu_usage())
                
    @app.route("/ram/", methods=['POST'])
    def get_ram():
        SensorHTTP.check_monitor_id(request.form["id"])
        return str(SensorHTTP.sensor.ram_usage())
                
    @app.route("/hdd/", methods=['POST'])
    def get_hdd():
        SensorHTTP.check_monitor_id(request.form["id"])
        return str(SensorHTTP.sensor.disk_space())
                
    @app.route("/data/", methods=['POST'])
    def get_data():
        SensorHTTP.check_monitor_id(request.form["id"])
        return str(SensorHTTP.sensor.get_data())

    def start(self):
        SensorHTTP.app.run(host = '0.0.0.0', port = int(self.sensor_port))

    def check_monitor_id(monitor_id):
        if monitor_id not in SensorHTTP.monitor_id_list:
            SensorHTTP.app.abort(403)
        else:
            pass
    check_monitor_id = staticmethod(check_monitor_id)

if __name__ == "__main__":
    pass
