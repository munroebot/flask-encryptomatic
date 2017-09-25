from flask import Flask, Response, request
import CryptoUtils
import json
from functools import wraps

app = Flask(__name__)

app.config['LOCKED'] = True
app.config['DB_PASSWORD'] = None

def _decrypt_file(encryption_key):

    with open('config.py.asc') as f:
        data_file = f.read()
    f.close()

    return json.loads(CryptoUtils.decrypt(data_file,encryption_key))

def unlock_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if app.config['LOCKED']:
            return Response("app is locked", status=503)
        return f(*args, **kwargs)
    return decorated_function

@app.route("/")
@unlock_required
def index():
    return str(app.config['DB_USERNAME']+ "/" + app.config['DB_PASSWORD'])

@app.route("/unlock", methods=['POST'])
def do_unlock():

    try:
        encryption_key = request.form.get('key')
        config = _decrypt_file(encryption_key)
        app.config['LOCKED'] = False

        for key, value in config.iteritems():
            app.config[key] = value

        return Response("app is unlocked", status=200)
    except:
        app.config['LOCKED'] = True
        return Response("app is still locked, bro", status=503)

app.run(host='0.0.0.0',debug=False)
