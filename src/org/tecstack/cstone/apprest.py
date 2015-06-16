from flask import Flask
from flask import Flask, jsonify, abort, make_response
from flask.ext.restful import Api, Resource
from flask.ext.restful import reqparse
from flask.ext.restful import fields, marshal
from flask.ext.httpauth import HTTPBasicAuth

app = Flask(__name__)
api = Api(app)
auth = HTTPBasicAuth()

@auth.get_password
def get_password(username):
    if username == 'promise':
        return 'pass'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error':'unauthorized access'}), 403)


def reload_data():
    global orders
    orders = [
        {
            'id':1,
            'title':'order 1',
            'desc':'first order',
        },
        {
            'id':2,
            'title':'order 2',
            'desc':'second order',
        }
    ]

app.reload_data = reload_data

orders = [
    {
        'id':1,
        'title':'order 1',
        'desc':'first order',
    },
    {
        'id':2,
        'title':'order 2',
        'desc':'second order',
    }
]

order_fields = {
    'title': fields.String,
    'desc': fields.String,
    'uri': fields.Url('order')
}


class OrderListApi(Resource):
    # decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title',
                                type=str,
                                required=True,
                                help='No order title provided',
                                location='json')
        self.reqparse.add_argument('desc',
                                type=str,
                                default='',
                                location='json')
        super(OrderListApi, self).__init__()

    def get(self):
        return {'orders': [marshal(o, order_fields) for o in orders]}

    def post(self):
        args = self.reqparse.parse_args()
        order = {
            'id': orders[-1]['id'] + 1,
            'title': args['title'],
            'desc': args['desc'],
        }
        orders.append(order)
        return {'order': marshal(order, order_fields)}, 201


class OrderApi(Resource):
    # decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title',
                                type = str,
                                location = 'json')
        self.reqparse.add_argument('desc',
                                type = str,
                                location = 'json')
        super(OrderApi, self).__init__()

    def get(self, id):
        forders = [o for o in orders if o['id']==id]
        if len(forders) == 0:
            abort(404)
        return {'order': marshal(forders[0],order_fields)}

    def put(self, id):
        forders = [o for o in orders if o['id']==id]
        if len(forders) == 0:
            abort(404)
        order = forders[0]
        args = self.reqparse.parse_args()
        for k,v in args.items():
            if v is not None:
                order[k] = v;

        return {'order': marshal(order, order_fields)}

    def delete(self, id):
        forders = [o for o in orders if o['id']==id]
        if len(forders) == 0:
            abort(404)
        orders.remove(forders[0])
        return {'result':'success'}

api.add_resource(OrderListApi,'/biz/api/v1.0/orders', endpoint='orders')
api.add_resource(OrderApi, '/biz/api/v1.0/orders/<int:id>', endpoint='order')

if __name__ == '__main__':
    app.run(debug=True, port=8000)
