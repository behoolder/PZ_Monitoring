import urllib
import urllib2
import time
import uuid
import sqlite3
import os
import mysql.connector
from threading import Thread
from flask import Flask, request, redirect, abort, session, escape

class Subscription:
    """
    Klasa ta jest zwyklym kontenerem dla subskrypcji.
    """

    def __init__(self, user, metric, sensor):
        """
        Konstruktor klasy Subscription.

        metric - monitorowane metryki
        sensor - adres wraz z portem sensora
        """
        
        self.metric = metric
        self.sensor = sensor
        self.user = user

    def get_metric(self):
        """
        Zwraca metryki wybrane w subskrypcji.
        """
        
        return self.metric

    def get_sensor(self):
        """
        Zwraca adres i port sensora.
        """
        
        return self.sensor

    def get_user(self):
        """
        Zwraca nazwe uzytkownika na ktorego subskrypcja zostala zarejestrowana.
        """
        
        return self.user

    
class Monitor(Thread):
    """
    Klasa monitora. Przechowuje ona informacje na temat zarejestrowanych sensorow oraz utworzonych subskrypcji.
    """

    def __init__(self, delay = 5):
        """
        Konstruktor klasy Monitor.

        delay - opoznienie z jakim wywolywane jest 'keep alive' do sensorow
        """
        Thread.__init__(self)
        self.sensors = {}
        self.delay = delay
        self.subscriptions = {}

        self.mysql = {}        
        self.mysql["host"] = "db4free.net"
        self.mysql["user"] = "prgzsp"
        self.mysql["passwd"] = "123321"
        self.mysql["db"] = "prgzspdb"

        #Wygenerowanie ID
        self.id = uuid.uuid1()

        #Wczytanie subskrypcji z bazy sqllite
        self.load_subscriptions()

    def add_sensor(self, host, port, hostname):
        """
        Rejestruje nowy sensor.

        host - adres sensora
        port - port sensora
        """

        self.sensors[(host, port)] = hostname
        print "Sensor %s:%s pomyslnie zarejestrowany"%(host, port)

        try:
            db = mysql.connector.Connect(host = self.mysql["host"], user = self.mysql["user"], passwd = self.mysql["passwd"], db = self.mysql["db"])
            cursor = db.cursor()
            cursor.execute("INSERT INTO Sensors(monitorUUID, name, address, port, cpu, ram, hdd) VALUES(%s, %s, %s, %s, %s, %s, %s)", (self.get_id(), hostname, host, port, True, True, True))
        except Exception, e:
            print e
        finally:
            db.close()        

    def keep_alive(self):
        """
        Sprawdza czy wszystkie zarejestrowane sensory sa nadal wlaczone i sprawne.
        Jesli ktorys z sensorow nie odpowiada to zostaje on wyrzucony z listy.
        """

        scp = self.sensors.copy()
        for (host, port) in scp:
            try:
                response = urllib2.urlopen("http://%s:%s/keepalive/"%(host, port))
                
                if response.msg != "OK" or response.code != 200:
                    print "Sensor %s:%s nie odpowiada"%(host, port)
                    self.sensors.pop((host, port))
                    continue

#                if self.sensors[(host, port)] == False:
#                    response = urllib2.urlopen("http://%s:%s/hostname/"%(host, port))
#                    hostname = eval(response.read())
#                    self.sensors[(host, port)] = hostname["Hostname"]

                print "Sensor %s:%s dziala poprawnie"%(host, port)
                        
            except Exception, e:
                print "Sensor %s:%s nie odpowiada"%(host, port)
                print e
                self.sensors.pop((host, port))
                continue

    def run(self):
        """
        Uruchamia keep_alive() w osobnym watku.
        """

        while True:
            self.keep_alive()
            time.sleep(self.delay)

    def get_sensors(self):
        """
        Zwraca wszystkie zarejestrowane sensory.
        """

        return str(self.sensors).replace('\'', '"')

    def get_id(self):
        """
        Zwraca ID monitora.
        """

        return str(self.id)

    def get_mysql(self):
        """
        Zwraca informacje o polaczeniu do bazy danych MySQL.
        """

        return self.mysql

    def create_subscription(self, user, metric, sensor, filename = "subscriptions.db"): 
        """
        Tworzy nowa subskrypcje.

        user - nazwa uzytkownika
        metric - monitorowane metryki
        sensor - monitorowany sensor
        filename - nazwa pliku z baza danych
        """

        self.subscriptions[max(self.subscriptions) + 1] = Subscription(user, metric, sensor)

        try: 
            con = sqlite3.connect(filename)
            cur = con.cursor()

            cur.execute("INSERT INTO subscriptions VALUES (?, ?, ?, ?)", (None, user, str(sensor), str(metric))) 
            con.commit()

        except sqlite3.Error, e:
            print "Database error: %s"%e.args[0]

        finally:
            if con:
                con.close()

        return max(self.subscriptions)

    def delete_subscription(self, user, sid, filename = "subscriptions.db"):
        """
        Usuwa subskrypcje.

        user - nazwa uzytkownika
        sid - numer subskrypcji
        filename - nazwa pliku z baza danych
        """

        if not sid in self.subscriptions:
            raise KeyError
        if self.subscriptions[sid].get_user() != user:
            raise ValueError

        try: 
            con = sqlite3.connect(filename)
            cur = con.cursor()

            cur.execute("DELETE FROM subscriptions WHERE id = ?", sid)

            con.commit()

        except sqlite3.Error, e:
            print "Database error: %s"%e.args[0]

        finally:
            if con:
                con.close()        

        del self.subscriptions[sid]

    def load_subscriptions(self, filename = "subscriptions.db"):
        """
        Laduje subskrypcje z bazy danych (SQLite). Jesli plik z baza nie istnieje to 
        tworzy nowa baze oraz odpowiednie tabele.

        filename - nazwa pliku z baza danych
        """

        exists = os.path.exists(filename)

        try: 
            con = sqlite3.connect(filename)
            cur = con.cursor()

            if not exists:
                cur.execute("CREATE TABLE subscriptions (id INTEGER PRIMARY KEY AUTOINCREMENT, user TEXT, sensor TEXT, metric TEXT);")
                con.commit()
            else:
                cur.execute("SELECT * FROM subscriptions")                
                for row in cur:
                    self.subscriptions[row[0]] = Subscription(row[1], eval(row[3]), eval(row[2])) 

        except sqlite3.Error, e:
            print "Database error: %s" % e.args[0]

        finally:
            if con:
                con.close()

    def subscription_list(self, user):
        """
        Zwraca liste subskrypcji dla danego uzytkownika.

        user - nazwa uzytkownika
        """
        
        sl = []
        
        for s in self.subscriptions:
            if self.subscriptions[s].get_user() == user:
                sl.append({"id" : s, "sensor" : self.subscriptions[s].get_sensor(), "metric" : self.subscriptions[s].get_metric()})

        ret = {user : sl}
        return str(ret)

    def get_data(self, user, sid): 
        """
        Zwraca dane z sensora.

        user - nazwa uzytkownika
        sid - numer subskrypcji
        """

        if not sid in self.subscriptions:
            raise KeyError
        if self.subscriptions[sid].get_user() != user:
            raise ValueError

        host, port = self.subscriptions[sid].get_sensor()
        ret = []

        for metric in self.subscriptions[sid].get_metric():
            request  = urllib2.Request("http://%s:%s/%s/"%(host, port, metric), urllib.urlencode({'id' : self.id}))
            response = urllib2.urlopen(request)

            if response.code == 200:
                ret.append(response.read())

        return ret


class MonitorHTTP:
    """
    Klasa serwera HTTP dla monitora.
    """

    app = Flask("monitor")
    monitor = Monitor()

    app.secret_key = os.urandom(24)
    
    def __init__(self, port):
        """
        Konstruktor klasy MonitorHTTP.

        port - port na ktorym ma zostac uruchomiony serwer
        """

        self.port = port

    @app.route('/login/', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            try:
                session['username'] = request.form['username']
                return redirect('/subscription_list/')
            except Exception, e:
                print e
        else:
            return '''<form action="" method="post">
                  <p><input type=text name=username>
                  <p><input type=submit value=Login>
                  </form>'''

    @app.route('/sensors/', methods=['GET'])
    def sensors():
        """
        Zwraca informacje o zarejestrowanych w monitorze sensorach.
        Dostep: GET
        """

        return MonitorHTTP.monitor.get_sensors()

    @app.route('/register/', methods=['POST'])
    def register():
        """
        Rejestruje nowy sensor w monitorze.
        Dostep: POST
        """

        MonitorHTTP.monitor.add_sensor(str(request.remote_addr), request.form["port"], request.form["hostname"])
        return MonitorHTTP.monitor.get_id()

    @app.route('/subscribe/', methods=['GET']) #TODO: POST!
    def subscribe():
        """
        Tworzy nowa subskrypcje. Wymaga wczesniejszego zalogowania.
        Dostep: POST
        """
        if 'username' in session:
            sid = MonitorHTTP.monitor.create_subscription(session["username"], ['cpu', 'ram'], ('localhost', '5001')) #TODO: POST info
            return redirect('/subscriptions/' + str(sid) + '/')
        else:
            return 'Nie jestes zalogowany!'

    @app.route('/subscription_list/', methods=['GET']) 
    def subscription_list():
        """
        Zwraca liste subskrypcji. Wymaga wczesniejszego zalogowania.
        Dostep: GET
        """

        if 'username' in session:
            return MonitorHTTP.monitor.subscription_list(session["username"])

        else:
            return 'Nie jestes zalogowany!'

    @app.route('/subscriptions/<sid>/', methods=['GET', 'DELETE'])
    def subscriptions(sid):
        """
        Wymaga wczesniejszego zalogowania.
        GET: Zwraca odpowiednie dane z sensora przypisane do konkretnej subskrypcji.
        DELETE: Usuwa subskrypcje.

        sid - numer subskrypcji
        """

        if 'username' not in session:
            return 'Nie jestes zalogowany!'

        try:
            if request.method == 'GET':
                data = MonitorHTTP.monitor.get_data(session["username"], int(sid))
            else:
                data = MonitorHTTP.monitor.delete_subscription(session["username"], int(sid))
        except ValueError, e:
            print e
            abort(403)
        except KeyError, e:
            print e
            abort(404)
        else:
            if request.method == 'GET':
                return "".join(data)
            else:
                return "Subskrypcja zostala usunieta!"

    def db_register(self):
        """
        Dodaje informacje o nowym monitorze do katalogu.
        """

        data = MonitorHTTP.monitor.get_mysql()

        try:
            db = mysql.connector.Connect(host = data["host"], user = data["user"], passwd = data["passwd"], db = data["db"])
            cursor = db.cursor()
            cursor.execute("INSERT INTO Monitors(address, port, uuid) VALUES(SUBSTRING_INDEX((SELECT host FROM information_schema.processlist WHERE ID=CONNECTION_ID()), ':', 1), %s, %s)", (self.port, MonitorHTTP.monitor.get_id()))
        except Exception, e:
            print e
        finally:
            db.close()

    def start(self, debug = False):
        """
        Uruchamia monitor oraz serwer HTTP.
        
        debug - ustala czy serwer HTTP ma byc uruchomiony w trybie debugowania.
        """

        self.db_register()

#        MonitorHTTP.monitor.start()
        MonitorHTTP.app.debug = debug
        MonitorHTTP.app.run(host = "0.0.0.0", port = self.port)


if __name__ == "__main__":
    pass
