from random import randint
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
    except:
        return "error"


def getFollowing(username):
    return api.username_info(username)['user']['following_count']


def getFollowers(username):
    return api.username_info(username)['user']['follower_count']


def getDFMB(username):
    return randint(0, 800)


def getAverageLikes(username):
    count = 0
    media_arr = []
    sum = 0
    for x in api.username_feed(username)['items']:
        media_arr.append(x['id'])
        count += 1
        if count == 6:
            break
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
