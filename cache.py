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

def cache_settings(mutual_friends, crawl_control, ratio_arr, purge_control, whitelist_legnth, speed, daily_limit):
    cache['mutual_friends'] = mutual_friends
    cache['crawl_control'] = crawl_control
    cache['ratio_arr'] = ratio_arr
    cache['purge_control'] = purge_control
    cache['whitelist_legnth'] = whitelist_legnth
    cache['speed'] = speed
    cache['daily_limit'] = daily_limit

def cache_following(arr):
    cache['following_arr'] = arr

def retrieve_following():
    return cache['following_arr']

def cache_auth_cookies():
    pass