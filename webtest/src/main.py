import test_selenium as ts

def tprint(fun):
  print(fun.__name__)
  fun()

# get
tprint(ts.test_get_success_nokey)
tprint(ts.test_get_success_keyexist)
tprint(ts.test_get_fail_keynotexist)

# post
tprint(ts.test_post_success)
tprint(ts.test_post_fail_nokey)
tprint(ts.test_post_fail_novalue)
tprint(ts.test_post_fail_keyexist)

# put
tprint(ts.test_put_success_create)
tprint(ts.test_put_success_update)
tprint(ts.test_put_fail_nokey)
tprint(ts.test_put_fail_novalue)

# delete
tprint(ts.test_delete_success)
tprint(ts.test_delete_fail_nokey)
tprint(ts.test_delete_fail_keynotexist)