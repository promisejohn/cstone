
from flask import Flask, request, abort, url_for, jsonify, g
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.httpauth import HTTPBasicAuth
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import TimedJSONWebSignatureSerializer \
                as Serializer, BadSignature, SignatureExpired


app = Flask(__name__, instance_relative_config=True)
app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy dog'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s/../.data/sqlite3.db' \
                                        % app.instance_path
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

# extensions
db = SQLAlchemy(app)
auth = HTTPBasicAuth()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True)
    password_hash = db.Column(db.String(128))

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=600):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id':self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired as e:
            return None
        except BadSignature as e:
            return None
        user = User.query.get(data['id'])
        return user

@auth.verify_password
def verify_password(username_or_token, password):
    # first try auth with token
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try auth with username/password
        user = User.query.filter_by(username = username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True

@app.route('/auth/api/v1.0/token')
@auth.login_required
def get_auth_token():
    '''
    Play around:
        curl -u promise:pass -i http://127.0.0.1:8000/auth/api/v1.0/token
        curl -u ${token}:unused -i http://127.0.0.1:8000/auth/api/v1.0/token
    '''
    token = g.user.generate_auth_token()
    return jsonify({'token':token.decode('ascii')})

@app.route('/auth/api/v1.0/resource')
@auth.login_required
def get_resource():
    '''
    Play around:
        curl -u promise:pass -i http://127.0.0.1:8000/auth/api/v1.0/resource
    '''
    return jsonify({'data':'Hello %s!' % g.user.username})

@app.route('/auth/api/v1.0/users', methods=['POST'])
def new_user():
    '''
    Play around:
        curl -i -X POST -H "Content-Type: application/json" \
                -d '{"username":"promise","password":"pass"}' \
                http://127.0.0.1:8000/auth/api/v1.0/users
    '''
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        abort(400) # missing arguments
    if User.query.filter_by(username=username).first() is not None:
        abort(400) # existing user

    user = User(username=username)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'username':user.username, 'password':user.password_hash}),\
            201,{'Location':url_for('get_user', id=user.id, _external=True)}

@app.route('/auth/api/v1.0/users/<int:id>',methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    if not user:
        abort(400)
    return jsonify({'username':user.username})

if __name__ == '__main__':
    db.drop_all()
    db.create_all()
    app.run(port=8000, debug=True)
