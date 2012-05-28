import sensor
import unittest

class SensorTest(unittest.TestCase):

    def setUp(self):
            self.sensor = sensor.Sensor('5010', '127.0.0.1:5001')
            self.sensor.shttp.add_monitor_id(1)
            self.app = self.sensor.shttp.app.test_client()
            self.app.testing = True

    def tearDown(self):
            pass

    def test_keepalive(self):
            rv = self.app.get('/keepalive/')
            print '~/keepalive/'
            print rv.data
            assert 'OK' in rv.data
            print

    def test_cpu(self):
            rv = self.app.get('/cpu/', headers=dict(id=1), follow_redirects=True)
            print '~/cpu/'
            print rv.data
            assert 'CPU' in rv.data
            print

    def test_ram(self):
            rv = self.app.get('/ram/', headers=dict(id=1), follow_redirects=True)
            print '~/ram/'
            print rv.data
            assert 'RAM' in rv.data
            print
	 			
    def test_hdd(self):
            rv = self.app.get('/hdd/', headers=dict(id=1), follow_redirects=True)
            print '~/hdd/'
            print rv.data
            assert 'Hard drives' in rv.data
            print

if __name__ == '__main__':
        unittest.main()