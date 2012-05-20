#-*- coding: utf-8 -*-

import mysql.connector
from commons.config import Config
from flask import Flask, request, redirect, abort, session, escape, make_response

class Catalog:
    """
    Klasa katalogu. Odpowiada za komunikację z bazą danych.\n
    """
    
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
                cursor.execute("SELECT * FROM Sensors WHERE monitorUUID = (SELECT uuid FROM Monitors WHERE monitorID = %s)", mid)
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

    @app.route('/sensors/', methods=['GET'])
    def sensors():
        """
        Zwraca informację o wszystkich działających sensorach.\n
        Dostęp: GET\n
        """
        
        try:
            response = make_response()
            if 'Origin' in request.headers:
                response.headers['Access-Control-Allow-Origin'] = request.headers['Origin']
            else:
                response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Credentials'] = 'true'
            response.data = CatalogHTTP.catalog.get_sensors()
        except Exception, e:
            print e
        else:
            return response

    @app.route('/monitors/', methods=['GET'])
    def sensors():
        """
        Zwraca informację o wszystkich działających monitorach.\n
        Dostęp: GET\n
        """
        
        try:
            response = make_response()
            if 'Origin' in request.headers:
                response.headers['Access-Control-Allow-Origin'] = request.headers['Origin']
            else:
                response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Credentials'] = 'true'
            response.data = CatalogHTTP.catalog.get_monitors()
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
        
        CatalogHTTP.app.debug = debug
        CatalogHTTP.app.run(host = "0.0.0.0", port = self.port)


if __name__ == "__main__":
    pass
