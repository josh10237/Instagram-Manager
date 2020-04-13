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

def cache_profile_pic(url):
    cache['profile_pic'] = url

def retrieve_profile_pic():
    return cache['profile_pic']

def clear_cache():
    cache['username'] = None
    cache['password'] = None
    cache['following_arr'] = None
    cache['DFMB_arr'] = None
    cache['profile_pic'] = None
    cache['mutual_friends'] = None
    cache['crawl_control'] = None
    cache['purge_control'] = None
    cache['ratio_vl'] = None
    cache['ratio_l'] = None
    cache['ratio_h'] = None
    cache['ratio_vh'] = None
    cache['whitelist_legnth'] = None
    cache['speed'] = None
    cache['daily_limit'] = None





# def cache_api(api):
#     cache['api'] = api
#
# def retrieve_api():
#     return cache['api']