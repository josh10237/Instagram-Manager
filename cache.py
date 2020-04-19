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

def cache_profile_pic(url):
    cache['profile_pic'] = url

def retrieve_profile_pic():
    return cache['profile_pic']

def cache_dash(arr):
    # [followers, following, dfmb, avglikes]
    cache['dash'] = arr

def retrieve_dash():
    # arr[0] = followers, arr[1] = following, arr[2] = dfmb, arr[3] = avglikes
    return cache['dash']

def clear_cache():
    cache['username'] = None
    cache['password'] = None
    cache['profile_pic'] = None
    cache['dash'] = None
    #settings cache- usage of below found in screens.py
    cache['mutual_friends'] = '30+'
    cache['crawl_control'] = 'manual'
    cache['purge_control'] = 'manual'
    cache['ratio_vl'] = True
    cache['ratio_l'] = True
    cache['ratio_h'] = True
    cache['ratio_vh'] = False
    cache['whitelist_legnth'] = '10'
    cache['speed'] = 'slow'
    cache['daily_limit'] = '100'





# def cache_api(api):
#     cache['api'] = api
#
# def retrieve_api():
#     return cache['api']