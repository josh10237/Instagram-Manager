from instagram_private_api import Client, ClientCompatPatch
from time import sleep

user_name = 'testaccforapi'
password = 'MADdog23'
api = Client(user_name, password, auto_patch=True)


def is_following_back(username):
    rank_token = api.generate_uuid(return_hex=False, seed=None)
    top_result = api.user_followers(api.username_info(username)['user']['pk'], rank_token)['users'][0]
    if top_result == user_name:
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
        if count == 5:
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
