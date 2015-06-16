
from nose.tools import with_setup, assert_equal
import json

from org.tecstack.cstone.apprest import app

class TestAppRest():
    '''
    Nose will recreate the Class Instance for each test method.

    Use nose to test around:
        nosetests -v    --with-coverage
                        --cover-package=org.tecstack.cstone
                        --cover-erase
    '''

    def setup(self):
        self.tester = app.test_client(self)
        app.reload_data()

    def teardown(self):
        pass

    def get_order_num(self):
        resp = self.tester.get('/biz/api/v1.0/orders')
        data = json.loads(resp.data)
        return len(data['orders'])

    @with_setup(setup, teardown)
    def test_order_list(self):
        resp = self.tester.get('/biz/api/v1.0/orders')
        assert_equal(200, resp.status_code)
        data = json.loads(resp.data)
        orders = data['orders']
        assert_equal(2, len(orders))

    @with_setup(setup, teardown)
    def test_order_new(self):
        data = json.dumps(dict(title='test order',
                    desc ='test desc'))
        resp = self.tester.post('/biz/api/v1.0/orders',
                                data=data,
                                content_type='application/json')
        assert_equal(201, resp.status_code)
        data = json.loads(resp.data)
        order = data['order']
        assert_equal('test order', order['title'])
        # There'll be 3 items in the list.
        assert_equal(3, self.get_order_num())

    @with_setup(setup,teardown)
    def test_order_get(self):
        resp = self.tester.get('/biz/api/v1.0/orders/1')
        assert_equal(200, resp.status_code)
        data = json.loads(resp.data)
        order = data['order']
        assert_equal('order 1', order['title'])

    @with_setup(setup,teardown)
    def test_order_update(self):
        data = json.dumps(dict(title='test order',
                    desc ='test desc'))
        resp = self.tester.put('/biz/api/v1.0/orders/1',
                            data = data,
                            content_type='application/json')
        assert_equal(200, resp.status_code)
        data = json.loads(resp.data)
        order = data['order']
        assert_equal('test order', order['title'])

    @with_setup(setup,teardown)
    def test_order_delete(self):
        resp = self.tester.delete('/biz/api/v1.0/orders/1')
        assert_equal(200, resp.status_code)
        data = json.loads(resp.data)
        assert_equal('success', data['result'])
        assert_equal(1, self.get_order_num())
