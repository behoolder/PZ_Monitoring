#-*- coding: utf-8 -*-

import monitor
import unittest

class MonitorTest(unittest.TestCase):

    def setUp(self):
        #Przyk³adowe dane uruchomienia monitor, catalog istnieje = 127.0.0.1:5000
        self.monitor = monitor.MonitorHTTP('5010', '127.0.0.1:5000')
        self.app = self.monitor.app.test_client()
        self.app.testing = True

    def tearDown(self):
        pass

    #Metody testujace monitor
    def test_keepalive(self):
        rv = self.app.get('/keepalive/', follow_redirects=True)
        print '~/keepalive/\n', rv.data
        assert 'OK' in rv.data
        print
			
    def test_login_get(self):
        rv = self.app.get('/login/', follow_redirects=True)
        print '~/login/ - GET\n\t\t ', rv.data
        assert '''<form action="" method="post">
                  <p><input type=text name=username>
                  <p><input type=submit value=Login>
                  </form>''' in rv.data
        print
        
    def test_login_post(self):
        rv = self.app.post('/login/', headers=dict(Origin='*'), data=dict(username='login'), follow_redirects=True)
        print '~/login/ - POST\n', rv.data
        assert 'msg' in rv.data
        print
		
    def test_sensors(self):
        rv = self.app.get('/sensors/', headers=dict(Origin='*'), follow_redirects=True)
        print '~/sensors/\n', rv.data
        assert '{' in rv.data
        print
		
    def test_register(self):
        rv = self.app.post('/register/', headers=dict(Origin='*'), data=dict(port=5011, hostname='tester', cpu=1, ram=1, hdd=1), follow_redirects=True)
        print '~/register/\n', rv.data
        assert '-' in rv.data
        print
		
    def test_subscribe(self):
        rv = self.app.post('/subscribe/', headers=dict(Origin='*'), data=dict(port=5011, hostname='tester', cpu=1, ram=1, hdd=1), follow_redirects=True)
        print '~/subscribe/\n', rv.data
        assert 'error' in rv.data
        print
			
if __name__ == '__main__':
    unittest.main()