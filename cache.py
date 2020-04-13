from fcache.cache import FileCache
cache = FileCache('instagramManager', flag='cs')

def cache_log_in(username, password):
    cache['username'] = username
    cache['password'] = password

def retrieve_log_in(type):
    if type == 'username':
        return cache['username']
    else:
        return cache['password']

def cache_following(arr):
    cache['following_arr'] = arr

def retrieve_following():
    return cache['following_arr']

def cache_DFMB(arr):
    cache['DFMB_arr'] = arr

def retrieve_DFMB():
    return cache['DFMB_arr']

# def cache_api(api):
#     cache['api'] = api
#
# def retrieve_api():
#     return cache['api']