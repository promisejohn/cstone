from flask import Flask, request, jsonify
from flask import abort, make_response, url_for
from flask.ext.httpauth import HTTPBasicAuth

app = Flask(__name__)
auth = HTTPBasicAuth()

@auth.get_password
def get_password(username):
    if username == 'promise':
        return 'pass'
    return None

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

@app.errorhandler(404)
def not_found(error):
    '''
    Make JSON Error response.
    '''
    return make_response(jsonify({'error':'Not Found.'}), 404)


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error':'Bad Request.'}), 400)

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error':'unauthorized access'}), 403)


@app.route('/')
def index():
    return "Hello World!"


def make_public_order(order):
    '''
    Return the order public URI
    '''
    public_order = {}
    for field in order:
        if field == 'id':
            public_order['uri'] = url_for('get_order',
                                        order_id=order['id'],
                                        _external=True)
        else:
            public_order[field] = order[field]

    return public_order

@app.route('/biz/api/v1.0/orders',methods=['GET'])
@auth.login_required
def get_orders():
    '''
    Get order list.

        Play ground with http auth:
            curl -u promise:pass -i http://localhost:8000/biz/api/v1.0/orders
    '''
    return jsonify({'orders':map(make_public_order, orders)})

@app.route('/biz/api/v1.0/orders/<int:order_id>',methods=['GET'])
def get_order(order_id):
    '''
    Get an order with id.
    '''
    forders = filter(lambda o: o['id'] == order_id, orders)
    if len(forders) == 0:
        abort(404)
    return jsonify({'order':forders[0]})

@app.route('/biz/api/v1.0/orders',methods=['POST'])
def create_order():
    '''
    Create new order.

        Play ground:
            curl -i -H 'Content-Type: application/json' -X POST \
                -d '{"title":"another order"}' \
                http://localhost:8000/biz/api/v1.0/orders
    '''
    if not request.json or not 'title' in request.json:
        abort(400)
    order = {
        'id':orders[-1]['id'] + 1,
        'title':request.json['title'],
        'desc':request.json.get('desc',''),
    }
    orders.append(order)
    return jsonify({'order':order}), 201

@app.route('/biz/api/v1.0/orders/<int:order_id>',methods=['PUT'])
def update_order(order_id):
    '''
    Update an existing order.

        Play ground:
            curl -i -H 'Content-Type: application/json' -X PUT
                -d '{"title":"another order modified", "desc":"desc modified"}'
                http://localhost:8000/biz/api/v1.0/orders/3
    '''
    forders = filter(lambda o: o['id'] == order_id, orders)
    if len(forders) == 0:
        abort(404)
    order = forders[0]
    if not request.json:
        abort(400)
    if 'title' not in request.json:
        abort(400)
    order['title'] = request.json.get('title',order['title'])
    order['desc'] = request.json.get('desc',order['desc'])
    return jsonify({'result':'success'})

@app.route('/biz/api/v1.0/orders/<int:order_id>',methods=['DELETE'])
def delete_order(order_id):
    '''
    Delete an order.

        Play ground:
            curl -i -X DELETE http://localhost:8000/biz/api/v1.0/orders/3
    '''
    forders = filter(lambda o: o['id'] == order_id, orders)
    if len(forders) == 0:
        abort(404)
    orders.remove(forders[0])
    return jsonify({'result':'success'})


if __name__ == '__main__':
    app.run(port=8000,debug=True);
