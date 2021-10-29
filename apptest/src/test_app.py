#
# HTTP Status Code
#
# 200: OK
#  - GET, POST, PUT, DELETE
#
# 400: Bad request. 
#  - POST, PUT: Key and/or Value are not OK.
#
# 404: Resource not found.
#  - GET, DELETE: Key doesn't exist
#
# 405: Method not allowed.
#  - /api/v1/keys/ : Getting if method is not GET
#  - /api/v1/keys/key : Method is not in [GET,POST,PUT,DELETE]
#
# 409: Resource conflict. 
#  - POST: Key already exists
#
# 500: Server internal error.
#  - Unexpected trouble happens on app server due to Bug.
#

import os
from requests import get, post, put, delete

APP_HOST = os.environ['APP_HOST']
APP_PORT = int(os.environ['APP_PORT'])
BASEURL = f'http://{APP_HOST}:{APP_PORT}/api/v1'

##########
## KEYS ##
##########

def test_keys_get():
  r = get(f'{BASEURL}/keys/')
  assert r.status_code == 200

def test_keys_get_wrongurl():
  r = get(f'{BASEURL}/key/')
  assert r.status_code == 404

def test_keys_post():
  r = post(f'{BASEURL}/keys/')
  assert r.status_code == 405

def test_keys_put():
  r = put(f'{BASEURL}/keys/')
  assert r.status_code == 405

def test_keys_delete():
  r = delete(f'{BASEURL}/keys/')
  assert r.status_code == 405


#############
## KEY GET ##
#############

def test_key_get_exist():
  clean_and_add_keys()
  r = get(f'{BASEURL}/keys/apple')
  assert r.status_code == 200
  assert r.json() == {'apple':'red'}

def test_key_get_notexist():
  clean_and_add_keys()
  r = get(f'{BASEURL}/keys/lemon')
  assert r.status_code == 404

def test_key_get_notalnum1():
  clean_and_add_keys()
  r = get(f'{BASEURL}/keys/ap_le')
  assert r.status_code == 400

def test_key_get_notalnum2():
  clean_and_add_keys()
  r = get(f'{BASEURL}/keys/あいうえお')
  assert r.status_code == 400

##############
## KEY POST ##
##############

def test_key_post_notexist():
  clean_and_add_keys()
  r = post(f'{BASEURL}/keys/grape', data='purple')
  assert r.status_code == 200
  assert r.json() == {'grape':'purple'}

def test_key_post_exist():
  clean_and_add_keys()
  r = post(f'{BASEURL}/keys/apple', data='green')
  assert r.status_code == 409

def test_key_post_notalnum1():
  clean_and_add_keys()
  r = post(f'{BASEURL}/keys/gr_pe', data='purple')
  assert r.status_code == 400

def test_key_post_notalnum2():
  clean_and_add_keys()
  r = post(f'{BASEURL}/keys/grape', data='pu_ple')
  assert r.status_code == 400

def test_key_post_notalnum3():
  clean_and_add_keys()
  r = post(f'{BASEURL}/keys/あいうえお', data='purple')
  assert r.status_code == 400

def test_key_post_notalnum4():
  clean_and_add_keys()
  r = post(f'{BASEURL}/keys/grape', data='あいうえお'.encode())
  assert r.status_code == 400

#############
## KEY PUT ##
#############

def test_key_put_notexist():
  clean_and_add_keys()
  r = put(f'{BASEURL}/keys/grape', data='purple')
  assert r.status_code == 200
  assert r.json() == {'grape':'purple'}

def test_key_put_exist():
  clean_and_add_keys()
  r = put(f'{BASEURL}/keys/apple', data='green')
  assert r.status_code == 200
  assert r.json() == {'apple':'green'}

def test_key_put_notalnum1():
  clean_and_add_keys()
  r = put(f'{BASEURL}/keys/gr_pe', data='purple')
  assert r.status_code == 400

def test_key_put_notalnum2():
  clean_and_add_keys()
  r = put(f'{BASEURL}/keys/grape', data='pu_ple')
  assert r.status_code == 400

def test_key_put_notalnum3():
  clean_and_add_keys()
  r = put(f'{BASEURL}/keys/あいうえお', data='purple')
  assert r.status_code == 400

def test_key_put_notalnum4():
  clean_and_add_keys()
  r = put(f'{BASEURL}/keys/grape', data='あいうえお'.encode())
  assert r.status_code == 400

################
## KEY DELETE ##
################

def test_key_delete_exist():
  clean_and_add_keys()
  r = delete(f'{BASEURL}/keys/apple')
  assert r.status_code == 200
  assert r.json() == {}

def test_key_delete_notexist():
  clean_and_add_keys()
  r = delete(f'{BASEURL}/keys/grape')
  assert r.status_code == 404

def test_key_delete_notalnum1():
  clean_and_add_keys()
  r = delete(f'{BASEURL}/keys/ap_le')
  assert r.status_code == 400

def test_key_delete_notalnum1():
  clean_and_add_keys()
  r = delete(f'{BASEURL}/keys/あいうえお')
  assert r.status_code == 400


###############
## TEST END ###
###############

def test_clean():
  clean()
  assert True


########################
## Utility. Not tests ##
########################

def clean():
  r = get(f'{BASEURL}/keys/')
  for key in r.json():
    delete(f'{BASEURL}/keys/{key}')
  num_keys = len(get(f'{BASEURL}/keys/').json())
  assert 0 == num_keys

def clean_and_add_keys():
  clean()
  r = put(f'{BASEURL}/keys/apple', data='red')
  assert r.status_code == 200
  r = put(f'{BASEURL}/keys/banana', data='yellow')
  assert r.status_code == 200
