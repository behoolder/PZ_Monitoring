#-*- coding: utf-8 -*-

import urllib
import urllib2
import time
import mysql.connector
from commons.config import Config
from flask import Flask, request, redirect, abort, session, escape, make_response
from threading import Thread

class Catalog(Thread):
    """
    Klasa katalogu. Odpowiada za komunikację z bazą danych.\n
    """

    def __init__(self):
        """
        Konstruktor klasy Catalog.\n
        """

        Thread.__init__(self)
        self.delay = 120
    
    def get_sensors(self, mid = None):
        """
        Zwraca pełną informację o wszystkich sensorach znajdujących się w bazie danych.\n
        """

        db = None
        sensors = []

        try:
            db = mysql.connector.Connect(**Config.dbinfo())
            cursor = db.cursor()
            if mid:
                cursor.execute("SELECT * FROM Sensors WHERE monitorUUID = (SELECT uuid FROM Monitors WHERE monitorID = %s)", 
                               (mid,))
            else:
                cursor.execute("SELECT * FROM Sensors")

            for row in cursor.fetchall():
                sensor = {"sensorID" : str(row[0]), "name" : str(row[2]), "address" : str(row[3]), "port" : str(row[4]), 
                          "cpu" : str(row[5]), "ram" : str(row[6]), "hdd" : str(row[7])}
                sensors.append(sensor)

        except Exception, e:
            print e
        finally:
            if db:
                db.close()

        return str('{"sensors" : ' + str(sensors) + '}').replace("'", "\"")

    def get_monitors(self):
        """
        Zwraca pełną informację o wszystkich monitorach znajdujących się w bazie danych.\n
        """

        db = None
        monitors = []

        try:
            db = mysql.connector.Connect(**Config.dbinfo())
            cursor = db.cursor()
            cursor.execute("SELECT * FROM Monitors")

            for row in cursor.fetchall():
                monitor = {"monitorID" : str(row[0]), "address" : str(row[1]), "port" : str(row[2])}
                monitors.append(monitor)

        except Exception, e:
            print e
        finally:
            if db:
                db.close()

        return str('{"monitors" : ' + str(monitors) + '}').replace("'", "\"")

    def m_register(self, address, port, uuid):
        """
        Dodaje informacje o nowym monitorze do katalogu.\n
        """

        db = None

        try:
            db = mysql.connector.Connect(**Config.dbinfo())
            cursor = db.cursor()
            #Usuniecie ewentualnych duplikatow
            cursor.execute("SELECT monitorID, uuid FROM Monitors WHERE address = %s AND port = %s", (address, port))
            for row in cursor.fetchall():
                cursor.execute("DELETE FROM Monitors WHERE monitorID = %s", (row[0],))
                cursor.execute("DELETE FROM Sensors WHERE monitorUUID = %s", (row[1],))

#            cursor.execute("INSERT INTO Monitors(address, port, uuid) VALUES(SUBSTRING_INDEX((SELECT host FROM information_schema.processlist WHERE ID=CONNECTION_ID()), ':', 1), %s, %s)", (self.port, MonitorHTTP.monitor.get_id()))
            cursor.execute("INSERT INTO Monitors(address, port, uuid) VALUES(%s, %s, %s)", (address, port, uuid))
            db.commit()
        except Exception, e:
            print "Database Error: %s"%e
        finally:
            if db:
                db.close()

    def s_register(self, uuid, host, port, hostname, cpu = True, ram = True, hdd = True):
        """
        Rejestruje nowy sensor.\n

        uuid - UUID monitora\n
        host - adres sensora\n
        port - port sensora\n
        hostname - nazwa sensora\n
        cpu - informuje czy sensor monitoruje obciażenie cpu\n
        ram - informuje czy sensor monitoruje zużycie ramu\n
        hdd - informuje czy sensor monitoruje dane o dyskach\n
        """

        db = None

        try:
            db = mysql.connector.Connect(**Config.dbinfo())
            cursor = db.cursor()
            cursor.execute("INSERT INTO Sensors(monitorUUID, name, address, port, cpu, ram, hdd) VALUES(%s, %s, %s, %s, %s, %s, %s)", (uuid, hostname, host, port, cpu, ram, hdd))
            db.commit()
        except Exception, e:
            print e
        finally:
            if db:
                db.close()        

    def run(self):
        """
        Wątek cyklicznie sprawdzający czy zarejestrowane sensory oraz monitory są nadal aktywne.\n
        """

        while True:
            self.check_monitors()
#            self.check_sensors()
            time.sleep(self.delay)

    def check_monitors(self):
        """
        Sprawdza czy zarejestrowane monitory są nadal aktywne.
        """
        
        db = None

        try:
            db = mysql.connector.Connect(**Config.dbinfo())
            cursor = db.cursor()
            cursor.execute("SELECT monitorID, address, port, uuid FROM Monitors")
            rows = cursor.fetchall()
        except Exception, e:
            print e
        finally:
            if db:
                db.close()

        for row in rows:
            try:
                response = urllib2.urlopen("http://%s:%s/keepalive/"%(row[1], row[2]))
                
                if response.msg != "OK" or response.code != 200:
                    raise Exception

                print "Monitor %s:%s dziala poprawnie"%(row[1], row[2])

            except Exception, e:
                print "Monitor %s:%s nie odpowiada"%(row[1], row[2])
                print e
                self.del_monitor(row[0], row[3])
                continue

    def check_sensors(self):
        """
        Sprawdza czy zarejestrowane sensory są nadal aktywne.
        """
        
        db = None

        try:
            db = mysql.connector.Connect(**Config.dbinfo())
            cursor = db.cursor()
            cursor.execute("SELECT sensorID, address, port FROM Sensors")
            rows = cursor.fetchall()
        except Exception, e:
            print e
        finally:
            if db:
                db.close()

        for row in rows:
            try:
                response = urllib2.urlopen("http://%s:%s/keepalive/"%(row[1], row[2]))
                
                if response.msg != "OK" or response.code != 200:
                    raise Exception

                print "Sensor %s:%s dziala poprawnie"%(row[1], row[2])

            except Exception, e:
                print "Sensor %s:%s nie odpowiada"%(row[1], row[2])
                print e
                self.del_sensor(str(row[0]))
                continue

    def del_monitor(self, mid, uuid):
        """
        Usuwa monitor z bazy danych.\n

        mid - numer ID monitora.\n
        uuid - UUID monitora.\n
        """

        db = None

        try:
            db = mysql.connector.Connect(**Config.dbinfo())
            cursor = db.cursor()
            cursor.execute("DELETE FROM Sensors WHERE monitorUUID = %s", (uuid,))
            cursor.execute("DELETE FROM Monitors WHERE monitorID = %s", (mid,))
            db.commit()
        except Exception, e:
            print e
        else:
            print "Monitor o numerze ID: %s, został usuniety" % mid
        finally:
            if db:
                db.close()

    def del_sensor(self, host, port, uuid):
        """
        Usuwa sensor z bazy danych.\n

        sid - numer ID sensora.\n
        """

        db = None

        try:
            db = mysql.connector.Connect(**Config.dbinfo())
            cursor = db.cursor()
            cursor.execute("DELETE FROM Sensors WHERE address = %s AND port = %s AND monitorUUID = %s", (host, port, uuid))
            db.commit()
        except Exception, e:
            print e
        else:
            print "Sensor (%s:%s) został usuniety" % (host, port)
        finally:
            if db:
                db.close()

class CatalogHTTP:
    """
    Klasa serwera HTTP dla katalogu.
    """

    app = Flask("catalog")
    catalog = Catalog()

    def __init__(self, port):
        """
        Konstruktor klasy CatalogHTTP.\n

        port - port na którym ma zostać uruchomiony serwer\n
        """

        self.port = port

    @app.route('/sensors/', methods=['GET', 'POST'])
    def sensors():
        """
        GET: Zwraca informację o wszystkich działających sensorach.\n
        POST: Rejestruje nowy sensor w katalogu.\n
        """
        
        try:
            response = make_response()
            if 'Origin' in request.headers:
                response.headers['Access-Control-Allow-Origin'] = request.headers['Origin']
            else:
                response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Credentials'] = 'true'

            if request.method == 'GET':
                response.data = CatalogHTTP.catalog.get_sensors()
            elif request.method == 'POST':
                CatalogHTTP.catalog.s_register(str(request.form['uuid']), str(request.form['host']), str(request.form['port']), 
                                               str(request.form['hostname'])) 
        except Exception, e:
            print e
        else:
            return response

    @app.route('/monitors/', methods=['GET', 'POST'])
    def monitors():
        """
        GET: Zwraca informację o wszystkich działających monitorach.\n
        POST: Rejestruje nowy monitor w katalogu. \n
        """
        
        try:
            response = make_response()
            if 'Origin' in request.headers:
                response.headers['Access-Control-Allow-Origin'] = request.headers['Origin']
            else:
                response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Credentials'] = 'true'

            if request.method == 'GET':
                response.data = CatalogHTTP.catalog.get_monitors()
            elif request.method == 'POST':
                CatalogHTTP.catalog.m_register(str(request.remote_addr), str(request.form['port']), str(request.form['uuid']))
        except Exception, e:
            print e
        else:
            return response

    @app.route('/monitors/eraser/', methods=['POST'])
    def eraser():
        """
        Usuwa sensor z katalogu.\n

        Dostęp: POST
        """
        
        try:
            response = make_response()
            if 'Origin' in request.headers:
                response.headers['Access-Control-Allow-Origin'] = request.headers['Origin']
            else:
                response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Credentials'] = 'true'
            CatalogHTTP.catalog.del_sensor(str(request.form['host']), str(request.form['port']), str(request.form['uuid']))
        except Exception, e:
            print e
        else:
            return response

    @app.route('/sensors/<mid>/', methods=['GET'])
    def sensors_m(mid):
        """
        Zwraca informację o wszystkich sensorach zarejestrowanych pod konkretnym monitorem.\n
        Dostęp: GET\n
        """
        
        try:
            response = make_response()
            if 'Origin' in request.headers:
                response.headers['Access-Control-Allow-Origin'] = request.headers['Origin']
            else:
                response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Credentials'] = 'true'
            response.data = CatalogHTTP.catalog.get_sensors(mid)
        except Exception, e:
            print e
        else:
            return response

    def start(self, debug = False):
        """
        Uruchamia serwer HTTP zarządzający katalogiem.\n
        
        debug - ustala czy serwer HTTP ma być uruchomiony w trybie debugowania\n
        """

        CatalogHTTP.catalog.start()
        CatalogHTTP.app.debug = debug
        CatalogHTTP.app.run(host = "0.0.0.0", port = self.port)


if __name__ == "__main__":
    pass
