
from nose.tools import with_setup, assert_equal
import json

from org.tecstack.cstone.auth import app, db

class TestAuth():

    def setup(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = \
                    'sqlite:///%s/../../.data/test.db' % app.instance_path
        db.create_all()
        self.tester = app.test_client(self)

    def teardown(self):
        db.drop_all()

    @with_setup(setup,teardown)
    def test_new_user(self):
        data = json.dumps(dict(username='test username',
                    password ='pass'))
        resp = self.tester.post('/auth/api/v1.0/users',
                                data=data,
                                content_type='application/json')
        assert_equal(201, resp.status_code)
        data = json.loads(resp.data)
        username = data['username']
        assert_equal('test username', username)
        assert_equal('http://localhost/auth/api/v1.0/users/1',
                    resp.headers['Location'])
