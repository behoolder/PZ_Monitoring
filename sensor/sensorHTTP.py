#-*- coding: utf-8 -*-

from flask import Flask, request, abort
import os

class SensorHTTP:
    '''
    Klasa obsługująca działanie serwera HTTP sensora.
    '''

    app             = Flask(__name__)
    monitor_id      = None
    sensor          = None

    def __init__(self, sensor_port):
        '''
        Konstruktor klasy SensorHTTP.\n
        
        sensor_port - port na którym uruchomiony zostanie sensor\n
        '''
        
        self.sensor_port = sensor_port
        
        if os.name == 'posix':
            from linux.linux import Linux
            SensorHTTP.sensor = Linux()
        elif os.name == 'nt':
            from windows.windows import Windows
            SensorHTTP.sensor = Windows()
        else :
            print 'Nie rozpoznano systemu, sensor zostanie wylaczony.'
            exit()    

    def add_monitor_id(self, monitor_id):
        SensorHTTP.monitor_id = monitor_id

    @app.route("/keepalive/", methods=['GET'])
    def keepalive():
        '''
        Zwraca informacje kontrolna dla monitora o działaniu.
        '''
        
        return 'OK'  

    @app.route("/cpu/", methods=['GET'])
    def get_cpu():
        '''
        Zwraca informacje o zużyciu procesora.
        '''
        
        SensorHTTP.check_monitor_id(request.headers["id"])
        return str(SensorHTTP.sensor.cpu_usage())
                
    @app.route("/ram/", methods=['GET'])
    def get_ram():
        '''
        Zwraca informacje o zuzyciu pamieci
        '''
        
        SensorHTTP.check_monitor_id(request.headers["id"])
        return str(SensorHTTP.sensor.ram_usage())
                
    @app.route("/hdd/", methods=['GET'])
    def get_hdd():
        '''
        Zwraca informacje o dysku twardym.
        '''
        try:
            SensorHTTP.check_monitor_id(request.headers["id"])
        except Exception, e:
            print e
        return str(SensorHTTP.sensor.disk_space())

    @app.route("/hostname/", methods=['GET'])
    def get_hostname():
        '''
        Zwraca informacje o nazwie hosta.
        '''
   
        return str(SensorHTTP.sensor.hostname())

    def get_metrics(self):
        '''
        Zwraca informacje o nazwie hosta lokalnie.
        '''
        
        return SensorHTTP.sensor.metrics()

    def start(self):
        '''
        Uruchamia działanie serwera HTTP.
        '''
        
        SensorHTTP.app.run(host = '0.0.0.0', port = int(self.sensor_port))

    def check_monitor_id(monitor_id):
        '''
        Sprawdza czy monitor może pobrać dane z sensora, porównując ID.
        '''

        if not monitor_id == SensorHTTP.monitor_id:
            abort(403)

    check_monitor_id = staticmethod(check_monitor_id)

if __name__ == "__main__":
    pass
