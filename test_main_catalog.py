#-*- coding: utf-8 -*-

import catalog
import unittest

class CatalogTest(unittest.TestCase):

    def setUp(self):
        self.catalog = catalog.CatalogHTTP('5010')
        self.app = self.catalog.app.test_client()
        self.app.testing = True

    def tearDown(self):
        pass
				
    def test_sensor_get(self):
        rv = self.app.get('/sensors/', follow_redirects=True)
        print '~/sensors/ - GET\n', rv.data
        assert 'sensors' in rv.data
        print				

    def test_sensor_post(self):
        rv = self.app.post('/sensors/', data=dict(host='127.0.0.1', port=1111, uuid=1234, hostname='example'), follow_redirects=True)
        print '~/sensors/ - POST\n', rv.data
        print
			
    def test_monitors_get(self):
        rv = self.app.get('/monitors/', follow_redirects=True)
        print '~/monitors/ - GET\n', rv.data
        assert 'monitors' in rv.data
        print				

    def test_monitors_post(self):
        rv = self.app.post('/monitors/', data=dict(host='127.0.0.1', port=1111, uuid=1234), follow_redirects=True)
        print '~/monitors/ - POST\n', rv.data
        print
			
    def test_sensors_m_get(self):
        rv = self.app.get('/sensors/123/', follow_redirects=True)
        print '~/sensors/123/\n', rv.data
        assert 'sensors' in rv.data
        print				

    def test_eraser_post(self):
        rv = self.app.post('/monitors/eraser/', data=dict(host='127.0.0.1', port=1111, uuid=1234), follow_redirects=True)
        print '~/monitors/eraser/\n', rv.data
        print
			
if __name__ == '__main__':
    unittest.main()