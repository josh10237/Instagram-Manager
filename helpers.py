from time import sleep

from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label

import screens
import cache as c
import os.path
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


def getDFMB(*username):
    try:
        x = c.retrieve_DFMB_count()
        if x is not None:
            return (x)
    except:
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
    arr = []
    user_id = get_user_id(username)
    rank_token = '2abc9200-76e4-11ea-ab20-001a7dda7113'
    a = api.user_following(user_id, rank_token)
    print(len(a['users']))
    for val in a['users']:
        arr.append((val['username'], val['pk'], val['profile_picture']))
    return arr


def get_DFMB_array(username):
    ret_arr = []
    arr = get_following_array(username)
    x = 0
    for user in arr:
        profile = user[2]
        user_id = user[1]
        user_name = user[0]
        x += 1
        if not is_following_back(user_id):
            ret_arr.append(user_name)
            percent = x / len(arr)
            DFMB_column(user_name, user_id, profile, percent)
            print("added: " + str(user_name))
    return ret_arr


def DFMB_column(user_name, user_id, profile, percent):
    layout = GridLayout(rows=1, cols=3)
    layout.add_widget(screens.ImageButton(source=c.retrieve_profile_pic()))
    layout.add_widget(Label(text="@" + user_name, color=(0, 0, 0, 1), font_size=25))
    layout.add_widget(Button(background_normal='images/buttonbackgrounds/unfollow.png',
                             background_down='images/buttonbackgrounds/unfollow_select.png'))
    self.ids.widget_list.add_widget(layout)

# def DFMB_column(username):
#     ret_arr = []
#     x = 0
#     arr = get_following_array(username)
#     total = len(arr)
#     for user in arr:
#         profile = user[2]
#         user_id = user[1]
#         user_name = user[0]
#         x += 1
#         percent = x/total
#         if not is_following_back(user_id):
#             ret_arr.append(user_name)
#             p = screens.ListRow(user_name, user_id, profile)
#             p.add_row()
#             print("added: " + str(user_name))
#     return ret_arr
