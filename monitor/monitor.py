#-*- coding: utf-8 -*-

import urllib
import urllib2
import time
import uuid
import sqlite3
import os
from threading import Thread
from flask import Flask, request, redirect, abort, session, escape, make_response

class WrongSubscriptionID(Exception):
    """
    Klasa wyjątku informująca o nieistniejącej subskrypcji.
    """
    
    pass

class WrongUser(Exception):
    """
    Klasa wyjątku informująca o próbie dostępu do subskrypcji należącej do innego użytkownika.
    """
    
    pass

class Subscription:
    """
    Klasa ta jest zwykłym kontenerem dla subskrypcji.
    """

    def __init__(self, user, metric, sensor):
        """
        Konstruktor klasy Subscription.\n

        user - nazwa użytkownika\n
        metric - monitorowane metryki\n
        sensor - adres wraz z portem sensora\n
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
        Zwraca nazwę użytkownika na którego subskrypcja została zarejestrowana.
        """
        
        return self.user

    
class Monitor(Thread):
    """
    Klasa monitora. Przechowuje ona informację na temat zarejestrowanych sensorów oraz utworzonych subskrypcji.
    """

    def __init__(self, delay = 5):
        """
        Konstruktor klasy Monitor.\n

        delay - opóźnienie z jakim wywoływane jest 'keep alive' do sensorów\n
        """

        Thread.__init__(self)
        self.sensors = {}
        self.delay = delay
        self.subscriptions = {}

        #Wygenerowanie ID
        self.id = uuid.uuid1()

        #Wczytanie subskrypcji z bazy sqllite
        self.load_subscriptions()

    def add_sensor(self, host, port, hostname, cpu = True, ram = True, hdd = True):
        """
        Rejestruje nowy sensor.\n

        host - adres sensora\n
        port - port sensora\n
        hostname - nazwa sensora\n
        cpu - informuje czy sensor monitoruje obciażenie cpu\n
        ram - informuje czy sensor monitoruje zużycie ramu\n
        hdd - informuje czy sensor monitoruje dane o dyskach\n
        """

        try:
            data = urllib.urlencode({'port' : port, 'uuid' : self.get_id(), 'host' : host, 'hostname' : hostname})
            request  = urllib2.Request("http://%s/sensors/"%(self.catalog), data)
            response = urllib2.urlopen(request)

            if response.code != 200:
                raise Exception
        except Exception, e:
            print e

        self.sensors[(host, port)] = hostname
        print "Sensor %s:%s pomyslnie zarejestrowany"%(host, port)

    def del_sensor(self, host, port):
        """
        Usuwa sensor z monitora.\n

        host - adres sensora\n
        port - port sensora\n
        """

        self.sensors.pop((host, port))

    def keep_alive(self): 
        """
        Sprawdza czy wszystkie zarejestrowane sensory są nadal właczone i sprawne.
        Jeśli ktoryś z sensorów nie odpowiada to zostaje on wyrzucony z listy.
        """

        scp = self.sensors.copy()
        for (host, port) in scp:
            try:
                response = urllib2.urlopen("http://%s:%s/keepalive/"%(host, port))
                
                if response.msg != "OK" or response.code != 200:
                    raise Exception

                print "Sensor %s:%s dziala poprawnie"%(host, port)
                        
            except Exception, e:
                print "Sensor %s:%s nie odpowiada"%(host, port)
                print e
                self.del_sensor(host, port)
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

    def create_subscription(self, user, metric, sensor, filename = "subscriptions.db"): 
        """
        Tworzy nową subskrypcję.\n

        user - nazwa użytkownika\n
        metric - monitorowane metryki\n
        sensor - monitorowany sensor\n
        filename - nazwa pliku z bazą danych\n
        """

        if len(self.subscriptions) == 0:
            self.subscriptions[1] = Subscription(user, metric, sensor)
        else:
            self.subscriptions[max(self.subscriptions) + 1] = Subscription(user, metric, sensor)

        con = None

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
        Usuwa subskrypcję.\n

        user - nazwa użytkownika\n
        sid - numer subskrypcji\n
        filename - nazwa pliku z bazą danych\n
        """

        if not sid in self.subscriptions:
            raise WrongSubscriptionID
        if self.subscriptions[sid].get_user() != user:
            raise WrongUser

        con = None

        try: 
            con = sqlite3.connect(filename)
            cur = con.cursor()

            cur.execute("DELETE FROM subscriptions WHERE id = ?", str(sid))

            con.commit()

        except sqlite3.Error, e:
            print "Database error: %s"%e.args[0]

        finally:
            if con:
                con.close()        

        del self.subscriptions[sid]

    def load_subscriptions(self, filename = "subscriptions.db"):
        """
        Ładuje subskrypcję z bazy danych (SQLite). Jeśli plik z baza nie istnieje to 
        tworzy nową bazę oraz odpowiednie tabele.\n

        filename - nazwa pliku z bazą danych\n
        """

        exists = os.path.exists(filename)
        con = None

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
        Zwraca listę subskrypcji dla danego użytkownika.\n

        user - nazwa użytkownika\n
        """
        
        sl = []
        
        for s in self.subscriptions:
            if self.subscriptions[s].get_user() == user:
                sl.append({"id" : s, "sensor" : self.subscriptions[s].get_sensor(), "metric" : self.subscriptions[s].get_metric()})

        ret = {str(user) : sl}
        return str(ret).replace("(", "[").replace(")", "]")

    def get_data(self, user, sid): 
        """
        Zwraca dane z sensora.\n

        user - nazwa użytkownika\n
        sid - numer subskrypcji\n
        """

        if not sid in self.subscriptions:
            raise WrongSubscriptionID
        if self.subscriptions[sid].get_user() != user:
            raise WrongUser

        host, port = self.subscriptions[sid].get_sensor()
        data = {}

        for metric in self.subscriptions[sid].get_metric():
            request  = urllib2.Request("http://%s:%s/%s/"%(host, port, metric))
            request.add_header('id', self.id)
            response = urllib2.urlopen(request)

            if response.code == 200:
                data.update(eval(response.read()))

        return str({str(self.sensors[(host, port)]) : data})

    def set_catalog(self, catalog):
        """
        Ustawia dane (adres i port) katalogu z którym komunikuje się monitor.\n
        """

        self.catalog = catalog

    def db_register(self, port):
        """
        Wysyła informację do katalogu w celu zarejestrownia nowego monitora.\n

        port - port monitora.\n
        """

        try:
            data = urllib.urlencode({'port' : port, 'uuid' : self.get_id()})
            request  = urllib2.Request("http://%s/monitors/"%(self.catalog), data)
            response = urllib2.urlopen(request)

            if response.code != 200:
                raise Exception
        except Exception, e:
            print e
            print "Nie udalo sie polaczyc z katalogiem!"
            exit(-1)


class MonitorHTTP:
    """
    Klasa serwera HTTP dla monitora.\n
    """

    app = Flask("monitor")
    monitor = Monitor()

    app.secret_key = os.urandom(24)
    
    def __init__(self, port, catalog):
        """
        Konstruktor klasy MonitorHTTP.\n

        port - port na którym ma zostać uruchomiony serwer\n
        """

        self.port = port
        self.catalog = catalog

    @app.route("/keepalive/", methods=['GET'])
    def keepalive():
        '''
        Zwraca informacje kontrolna o działaniu.
        '''
        
        return 'OK'  

    @app.route('/login/', methods=['GET', 'POST'])
    def login():
        """
        Loguje użytkownika na monitorze.\n
        GET: Otwiera stronę z formularzem logowania.\n
        POST: Pobiera nazwę użytkownika oraz loguje go na monitorze.\n
        """

        if request.method == 'POST':
            try:
                session['username'] = request.form['username']
                response = make_response()
                if 'Origin' in request.headers:
                    response.headers['Access-Control-Allow-Origin'] = request.headers['Origin']
                else:
                    response.headers['Access-Control-Allow-Origin'] = '*'
                response.headers['Access-Control-Allow-Credentials'] = 'true' 
#                response.headers['Location'] = '/subscription_list/'
#                response.status_code = 302
                response.data = "{\"msg\" : \"Zalogowano pomyślnie.\"}"
            except Exception, e:
                print e
            else:
                return response
        else:
            return '''<form action="" method="post">
                  <p><input type=text name=username>
                  <p><input type=submit value=Login>
                  </form>'''

    @app.route('/sensors/', methods=['GET'])
    def sensors():
        """
        Zwraca informację o zarejestrowanych w monitorze sensorach.\n
        Dostęp: GET\n
        """
        
        try:
            response = make_response()
            if 'Origin' in request.headers:
                response.headers['Access-Control-Allow-Origin'] = request.headers['Origin']
            else:
                response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Credentials'] = 'true' 
            response.data = MonitorHTTP.monitor.get_sensors()
        except Exception, e:
            print e
        else:
            return response

    @app.route('/register/', methods=['POST'])
    def register():
        """
        Rejestruje nowy sensor w monitorze.\n
        Dostęp: POST\n
        """

        try:
            MonitorHTTP.monitor.add_sensor(str(request.remote_addr), str(request.form['port']), str(request.form['hostname']),
                                           str(request.form['cpu']) == '1', str(request.form['ram']) == '1', 
                                           str(request.form['hdd']) == '1')

            response = make_response()
            if 'Origin' in request.headers:
                response.headers['Access-Control-Allow-Origin'] = request.headers['Origin']
            else:
                response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Credentials'] = 'true' 
            response.data = MonitorHTTP.monitor.get_id()
        except Exception, e:
            print e
        else:
            return response

    @app.route('/subscribe/', methods=['POST']) 
    def subscribe():
        """
        Tworzy nowa subskrypcję. Wymaga wcześniejszego zalogowania.\n
        Dostęp: POST\n
        """

        try:
            response = make_response()
            if 'Origin' in request.headers:
                response.headers['Access-Control-Allow-Origin'] = request.headers['Origin']
            else:
                response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Credentials'] = 'true' 

            if 'username' in session:
                sensor = (str(request.form['host']), str(request.form['port']))
                metric = []
                if str(request.form['cpu']) == '1':
                    metric.append('cpu')
                if str(request.form['ram']) == '1':
                    metric.append('ram')
                if str(request.form['hdd']) == '1':
                    metric.append('hdd')

                sid = MonitorHTTP.monitor.create_subscription(session['username'], metric, sensor) 
                response.data = "{\"id\" : \"" + str(sid) + "\"}"
            else:
                response.data = "{\"error\" : \"Nie jesteś zalogowany!\"}"
        except Exception, e:
            print e
        else:
            return response

    @app.route('/subscription_list/', methods=['GET']) 
    def subscription_list():
        """
        Zwraca listę subskrypcji. Wymaga wcześniejszego zalogowania.\n
        Dostęp: GET\n
        """

        try:
            response = make_response()
            if 'Origin' in request.headers:
                response.headers['Access-Control-Allow-Origin'] = request.headers['Origin']
            else:
                response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Credentials'] = 'true' 
            if 'username' in session:
                response.data = MonitorHTTP.monitor.subscription_list(session['username']).replace("'", "\"")
            else:
                response.data = "{\"error\" : \"Nie jesteś zalogowany!\"}"
        except Exception, e:
            print e
        else:
            return response

    @app.route('/subscriptions/<sid>/', methods=['GET', 'DELETE'])
    def subscriptions(sid):
        """
        Wymaga wcześniejszego zalogowania.\n
        GET: Zwraca odpowiednie dane z sensora przypisane do konkretnej subskrypcji.\n
        DELETE: Usuwa subskrypcję.\n

        sid - numer subskrypcji\n
        """

        try:
            response = make_response()
            if 'Origin' in request.headers:
                response.headers['Access-Control-Allow-Origin'] = request.headers['Origin']
            else:
                response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Credentials'] = 'true' 

            if 'username' not in session:
                response.data = "{\"error\" : \"Nie jesteś zalogowany!\"}"
            elif request.method == 'GET':
                response.data = MonitorHTTP.monitor.get_data(session['username'], int(sid)).replace("'", "\"")
            elif request.method == 'DELETE':
                data = MonitorHTTP.monitor.delete_subscription(session['username'], int(sid))
                response.data = "{\"msg\" : \"Subskrypcja została usunięta!\"}"
        except WrongUser, e:
            print "Brak dostępu do subskrypcji przez danego użytkownika."
            print e
            abort(403)
        except WrongSubscriptionID, e:
            print "Nie istniejący numer subskrypcji."
            print e
            abort(404)
        except KeyError, e:
            print "Prawdopodobnie nastąpiła próba odwołania się do sensora, który nie jest zarejestrowany: %s."%e
            abort(404)
        except Exception, e:
            print e
        else:
            return response

    def start(self, debug = False):
        """
        Uruchamia monitor oraz serwer HTTP.\n
        
        debug - ustala czy serwer HTTP ma być uruchomiony w trybie debugowania\n
        """

        MonitorHTTP.monitor.set_catalog(self.catalog)
        MonitorHTTP.monitor.db_register(self.port)

        MonitorHTTP.monitor.start()
        MonitorHTTP.app.debug = debug
        MonitorHTTP.app.run(host = "0.0.0.0", port = self.port)


if __name__ == "__main__":
    pass
