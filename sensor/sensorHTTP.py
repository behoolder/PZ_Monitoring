from flask import request
from flask import Flask
import os

class SensorHTTP:
    '''
    Klasa obslugujaca dzialanie serwera HTTP sensora
    '''

    app             = Flask(__name__)
    monitor_id      = None
    sensor          = None

    def __init__(self, sensor_port, monitor_id):
        '''
        Konstruktor klasy SensorHTTP
        
        sensor_port - port na ktorym uruchomiony zostanie sensor
        monitor_id  - ID monitora ktory bedzie otrzymywac informacje z sensora
        '''
        
        self.sensor_port = sensor_port

        SensorHTTP.monitor_id = monitor_id
        
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
        '''
        Zwraca informacje kontrolna dla monitora o dzialaniu
        '''
        
        return 'OK'  

    @app.route("/cpu/", methods=['POST'])
    def get_cpu():
        '''
        Zwraca informacje o zuzyciu procesora
        '''
        
        SensorHTTP.check_monitor_id(request.form["id"])
        return str(SensorHTTP.sensor.cpu_usage())
                
    @app.route("/ram/", methods=['POST'])
    def get_ram():
        '''
        Zwraca informacje o zuzyciu pamieci
        '''
        
        SensorHTTP.check_monitor_id(request.form["id"])
        return str(SensorHTTP.sensor.ram_usage())
                
    @app.route("/hdd/", methods=['POST'])
    def get_hdd():
        '''
        Zwraca informacje o dysku twardym
        '''
        
        SensorHTTP.check_monitor_id(request.form["id"])
        return str(SensorHTTP.sensor.disk_space())

    @app.route("/hostname/", methods=['POST'])
    def get_hostname():
        '''
        Zwraca informacje o nazwie hosta
        '''
        
        SensorHTTP.check_monitor_id(request.form["id"])
        return str(SensorHTTP.sensor.hostname())
                
    @app.route("/data/", methods=['POST'])
    def get_data():
        '''
        Zwraca wszystkie dane z sensora
        '''
        
        SensorHTTP.check_monitor_id(request.form["id"])
        return str(SensorHTTP.sensor.get_data())

    def start(self):
        '''
        Uruchamia dzialanie serwera HTTP
        '''
        
        SensorHTTP.app.run(host = '0.0.0.0', port = int(self.sensor_port))

    def check_monitor_id(monitor_id):
        '''
        Sprawdza czy monitor moze pobrac dane z sensora, porownujac ID
        '''

        if not monitor_id == SensorHTTP.monitor_id:
            SensorHTTP.app.abort(403)
        else:
            pass
    check_monitor_id = staticmethod(check_monitor_id)

if __name__ == "__main__":
    pass
