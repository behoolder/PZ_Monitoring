import urllib
import urllib2
import time
import uuid
import sqlite3
import os
from threading import Thread
from flask import Flask, request, redirect, abort

class Subscription: #TODO: User
    """
    Klasa ta jest zwyklym kontenerem dla subskrypcji.
    """

    def __init__(self, metric, sensor):
        """
        Konstruktor klasy Subscription.

        metric - monitorowane metryki
        sensor - adres wraz z portem sensora
        """
        
        self.metric = metric
        self.sensor = sensor

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
        self.mysql["host"] = "localhost"
        self.mysql["user"] = "root"
        self.mysql["passwd"] = "root"
        self.mysql["db"] = "PZDB"

        #Wygenerowanie ID
        self.id = uuid.uuid1()

        self.load_subscriptions()

    def add_sensor(self, host, port):
        """
        Rejestruje nowy sensor.

        host - adres sensora
        port - port sensora
        """

        self.sensors[(host, port)] = False
        print "Sensor %s:%s pomyslnie zarejestrowany"%(host, port)

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

                if self.sensors[(host, port)] == False:
                    response = urllib2.urlopen("http://%s:%s/hostname/"%(host, port))
                    hostname = eval(response.read())
                    self.sensors[(host, port)] = hostname["Hostname"]

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

    def create_subscription(self, metric, sensor, filename = "subscriptions.db"): 
        """
        Tworzy nowa subskrypcje.

        metric - monitorowane metryki
        sensor - monitorowany sensor
        filename - nazwa pliku z baza danych
        """

        self.subscriptions[max(self.subscriptions) + 1] = Subscription(metric, sensor)

        try: 
            con = sqlite3.connect(filename)
            cur = con.cursor()

            cur.execute("INSERT INTO subscriptions VALUES (?, ?, ?, ?)", (None, 'user', str(sensor), str(metric))) #TODO: User            
            con.commit()

        except sqlite3.Error, e:
            print "Database error: %s"%e.args[0]

        finally:
            if con:
                con.close()

        return max(self.subscriptions)

    def delete_subscription(self, sid, filename = "subscriptions.db"):
        """
        Usuwa subskrypcje.

        sid - numer subskrypcji
        filename - nazwa pliku z baza danych
        """

        if not sid in self.subscriptions:
            raise KeyError

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
                    self.subscriptions[row[0]] = Subscription(eval(row[3]), eval(row[2])) #TODO: User

        except sqlite3.Error, e:
            print "Database error: %s" % e.args[0]

        finally:
            if con:
                con.close()

    def get_data(self, sid): 
        """
        Zwraca dane z sensora.

        sid - numer subskrypcji
        """

        if not sid in self.subscriptions:
            raise KeyError

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
    
    def __init__(self, port):
        """
        Konstruktor klasy MonitorHTTP.

        port - port na ktorym ma zostac uruchomiony serwer
        """

        self.port = port

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

        MonitorHTTP.monitor.add_sensor(str(request.remote_addr), request.form["port"])
        return MonitorHTTP.monitor.get_id()

    @app.route('/subscribe/', methods=['GET']) #TODO: POST!
    def subscribe():
        """
        Tworzy nowa subskrypcje.
        Dostep: POST
        """

        sid = MonitorHTTP.monitor.create_subscription(['cpu', 'ram'], ('localhost', '5001')) #TODO: POST info
        return redirect('/subscriptions/' + str(sid) + '/')

    @app.route('/subscriptions/<sid>/', methods=['GET', 'DELETE'])
    def subscriptions(sid):
        """
        GET: Zwraca odpowiednie dane z sensora przypisane do konkretnej subskrypcji.
        DELETE: Usuwa subskrypcje.

        sid - numer subskrypcji
        """

        try:
            if request.method == 'GET':
                data = MonitorHTTP.monitor.get_data(int(sid))
            else:
                data = MonitorHTTP.monitor.delete_subscription(sid)
        except Exception, e:
            print e
            abort(404)
        else:
            if request.method == 'GET':
                return "".join(data)
            else:
                return "Subskrypcja zostala usunieta!"

    def start(self, debug = False):
        """
        Uruchamia monitor oraz serwer HTTP.
        
        debug - ustala czy serwer HTTP ma byc uruchomiony w trybie debugowania.
        """

        MonitorHTTP.monitor.start()
        MonitorHTTP.app.debug = debug
        MonitorHTTP.app.run(host = "0.0.0.0", port = self.port)

#        mysql = MonitorHTTP.monitor.get_mysql()

#        db = _mysql.connect(host = mysql["host"], user = mysql["user"], passwd = mysql["passwd"], db = mysql["db"])
#        db.query("INSERT INTO Monitor(URI, CPU, RAM, HDD) VALUES(?, ?, ?, ?)", ("localhost:5000", True, True, True))
#        db.close()


if __name__ == "__main__":
    pass
