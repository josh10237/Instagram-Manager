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

def cache_auth_cookies():
    pass