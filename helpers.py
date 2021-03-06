from time import sleep
import cache as c
import whitelist as w
from instagram_private_api import Client, ClientCompatPatch


global api

def new_API(username, password):
    global api
    try:
        api = Client(username, password, auto_patch=True)
    except ClientError:
        return "error"


def getFollowing(username):  
    return api.username_info(username)['user']['following_count']


def getFollowers(username):
    return api.username_info(username)['user']['follower_count']


def getDFMB(*username):
    try:
        x = c.retrieve_dash()[2]
        if x is not None:
            return (x)
    except:
        return ("Run Purge")
    if x == None:
        return ("Run Purge")


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


def get_last_post_id(username):
    return api.username_feed(username)['items'][0]['id']

def get_likers_post(media_id):
    return api.media_likers(media_id)['users']


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
    arr = []
    user_id = get_user_id(username)
    rank_token = '2abc9200-76e4-11ea-ab20-001a7dda7113'
    a = api.user_following(user_id, rank_token)
    for val in a['users']:
        arr.append((val['username'], val['pk'], val['profile_picture']))
    return arr



def dynamic_DFMB(arr, step):
    user = arr[step]
    user_id = user[1]
    percent = (step + 1) / len(arr)
    if is_following_back(user_id):
        print("Following you back :)")
        return ['nil', percent]
    else:
        user_name = user[0]
        profile = user[2]
        print("DFMB :(   " + str(user_name))
        return [profile, user_id, user_name, percent]

def unfollow(user_id):
    api.friendships_destroy(user_id)

def follow(user_id):
    user_name = get_usernme(user_id)
    profile = get_profile_user(user_name)
    w.whitelist_timer([profile, user_id, user_name])
    api.friendships_create(user_id)

def get_usernme(user_id):
    return api.user_info(user_id)['user']['username']

def get_mutual(user_id):
    return api.user_info(user_id)['user']['mutual_followers_count']

def get_ratio(user_id):
    followers = (api.user_info(user_id)['user']['counts']['followed_by'])
    following = (api.user_info(user_id)['user']['counts']['follows'])
    return followers/following

def get_profile_user(username):
    return api.username_info(username)['user']['profile_pic_url']

def get_crawl_check_data(user_id):
    rtarr = []
    arr = api.friendships_show(user_id)
    rtarr.append(arr['incoming_request'])
    rtarr.append(arr['outgoing_request'])
    rtarr.append(arr['blocking'])
    rtarr.append(arr['following'])
    rtarr.append(arr['followed_by'])
    rtarr.append(arr['is_private'])
    return rtarr