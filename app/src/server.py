import os, re, redis
from flask import Flask, jsonify, request

REDIS_HOST = os.environ['REDIS_HOST']
REDIS_PORT = int(os.environ['REDIS_PORT'])
REDIS_DB = int(os.environ['REDIS_DB'])
REDIS = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
APP_PORT = int(os.environ['PORT'])
DEBUG = os.environ['DEBUG'].lower() == 'true'
app = Flask('app server')

@app.route('/api/v1/keys/', methods=['GET'])
def api_keys():
  data = {}
  cursor = '0'
  while cursor != 0:
    cursor, keys = REDIS.scan(cursor=cursor, count=1000000)
    if len(keys) == 0:
      break
    keys = [key.decode() for key in keys]
    values = [value.decode() for value in REDIS.mget(*keys)]
    data.update(dict(zip(keys, values)))
  return success(data)

@app.route('/api/v1/keys/<key>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def api_key(key):
  if not isalnum(key):
    return error(400.1)
  body = request.get_data().decode().strip()
  if request.method in ['POST', 'PUT']:
    if body == '':
      return error(400.2)
    if not isalnum(body):
      return error(400.3)
  def get():
    value = REDIS.get(key)
    if value is not None:
      return success({key:value.decode()})
    return error(404)
  def post():
    if REDIS.get(key) is not None:
      return error(409)
    REDIS.set(key, body)
    return success({key:body})
  def put():
    REDIS.set(key, body)
    return success({key:body})
  def delete():
    if REDIS.delete(key) == 0:
      return error(404)
    return success({})
  fdict = {'GET':get, 'POST':post, 'PUT':put, 'DELETE':delete}
  return fdict[request.method]()

def isalnum(text):
  return re.match(r'^[a-zA-Z0-9]+$', text) is not None

def success(d):
  return (jsonify(d), 200)

def error(code):
  message = {
    400.1: "bad request. key must be alnum",
    400.2: "bad request. post/put needs value on body",
    400.3: "bad request. value must be Alnum",
    404: "resource not found",
    409: "resource conflict. resource already exist",
  }
  return (jsonify({'error':message[code], 'code':int(code)}), int(code))

@app.errorhandler(404)
def api_not_found_error(error):
  return (jsonify({'error':"api not found", 'code':404}), 404)

@app.errorhandler(405)
def method_not_allowed_error(error):
  return (jsonify({'error':'method not allowed', 'code':405}), 405)

@app.errorhandler(500)
def internal_server_error(error):
  return (jsonify({'error':'server internal error', 'code':500}), 500)

app.run(debug=DEBUG, host='0.0.0.0', port=APP_PORT)
