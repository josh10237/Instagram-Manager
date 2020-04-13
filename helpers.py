import cache as c
from time import sleep
import os.path

try:
    from instagram_private_api import (
        Client, ClientError, ClientLoginError,
        ClientCookieExpiredError, ClientLoginRequiredError,
        __version__ as client_version)
except ImportError:
    import sys

    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from instagram_private_api import (
        Client, ClientError, ClientLoginError,
        ClientCookieExpiredError, ClientLoginRequiredError,
        __version__ as client_version)

global api
def new_API(username, password):
    global api
    try:
        api = Client(username, password, auto_patch=True)
        #c.cache_api(api)
    except:
        return "error"

# def remember_api():
#     global api
#     try:
#         api = c.retrieve_api()
#         return(200)
#     except:
#         return (400)


def getFollowing(username):
    return api.username_info(username)['user']['following_count']


def getFollowers(username):
    return api.username_info(username)['user']['follower_count']


def getDFMB(username, over_ride):
    if over_ride == 0:  #get cached value
        DFMB_cache = ''
        try:
            DFMB_cache = c.retrieve_DFMB()
            if DFMB_cache != '':
                return len(DFMB_cache)
        except:
            print("Automatic Ovverride Activated DFMB")
            over_ride = 1
    elif over_ride == 1:  #get real DFMB check on cached following_array
        return len(get_DFMB_array(username))
    else:  #get real DFMB on real following_array
        return len(get_DFMB_array(username, True))

def get_profile_pic():
    return api.current_user()['user']['profile_pic_url']

def getAverageLikes(username):
    count = 0
    media_arr = []
    sum = 0
    for x in api.username_feed(username)['items']:
        media_arr.append(x['id'])
        count += 1
        if count == 6:
            break
    if media_arr == []:
        return 0
    for media_id in media_arr:
        sum += int(len(api.media_likers(str(media_id))['users']))
    return (sum / count)


def is_following_back(user_id):
    if api.friendships_show(user_id)['followed_by']:
        return True
    else:
        return False


def get_user_id(username):
    return api.username_info(username)['user']['pk']


def get_media_user(username):
    count = 0
    media_arr = []
    for x in api.username_feed(username)['items']:
        media_arr.append(x['id'])
        count += 1
        if count == 6:
            break
    return media_arr


def get_likers_post(media_id):
    likers_arr = []
    for x in api.media_likers(media_id)['users']:
        likers_arr.append(x['pk'])


def follow_arr(speed, follow_arr):
    while follow_arr.len() > 5:
        api.friendships_create(follow_arr[0])
        follow_arr.pop(0)
        sleep(speed)


def following_ids(user_id):
    maxid = 0
    arr = []
    rank_token = api.generate_uuid(return_hex=False, seed=None)
    while True:
        for x in range(99):
            try:
                id = api.user_following(user_id, rank_token, max_id=maxid)['users'][x]['username']
                arr.append(id)
            except:
                return (arr)

        maxid += 100


def get_following_array(username):
    # from getDFMB : 2
    arr = []
    x = 0
    max_id = 0
    user_id = get_user_id(username)
    rank_token = '2abc9200-76e4-11ea-ab20-001a7dda7113'
    numFollowing = getFollowing(username)
    if numFollowing == 0:
        return ('request limit')
    a = api.user_following(user_id, rank_token)
    while x < numFollowing:
        try:
            val = x % 100
            tup = (a['users'][val]['username'], a['users'][val]['pk'], a['users'][val]['profile_picture'])
            arr.append(tup)
            sleep(.1)
        except IndexError:
            # shouldn't be triggered unless something went wrong
            return ("index error")
        except:
            # only triggered with bad password or rate limiting error
            return ("rate/throttle error")
        if ((x % 100) == 0) and (x != 0):
            max_id += 100
            a = api.user_following(user_id, rank_token, max_id=str(max_id))
        x += 1
    c.cache_following(arr)
    print("got following arr")
    return (arr)

def get_DFMB_array(username, *override):
    #from getDFMB : 1
    ret_arr = []
    ovr = str(override)
    tmp = ''
    for character in ovr:
        if character.isalnum():
            tmp += character
    ovr = tmp
    if ovr == 'True':
        arr = get_following_array(username)
    else:
        following_cache = ''
        try:
            following_cache = c.retrieve_following()
            if following_cache != '':
                arr = following_cache
        except:
            print("Automatic Ovverride Activated Following")
            arr = get_following_array(username)
    for user in arr:
        user_id = user[1]
        user_name = user[0]
        if not is_following_back(user_id):
            ret_arr.append(user_name)
            sleep(.1)
            print("added: " + str(user_name))
    c.cache_DFMB(ret_arr)
    return ret_arr
