import helpers as h
from time import sleep

from instagram_private_api import (
    Client, ClientError, ClientLoginError,
    ClientCookieExpiredError, ClientLoginRequiredError,
    __version__ as client_version)

username = "joshbenson_"
api = Client("_protikg", "iCRcoiCRco", auto_patch=True)
# rank_token = api.generate_uuid(return_hex=False, seed=None)
rank_token = '2abc9200-76e4-11ea-ab20-001a7dda7113'
user_id1 = "32341377860"  # testaccforapi
user_id2 = "5565476890"  # ella
user_id3 = "243946204"  # josh
user_id4 = "32649564590"  # pratik
arr = [user_id1, user_id2, user_id3]
# print(len(api.user_following(user_id2, rank_token, max_id=0)['users']))
# print(api.user_following(user_id2, rank_token, max_id=100))
# print(api.user_followers(user_id2, rank_token, max_id=100))
# user_id = api.user_followers(user_id1, rank_token)['users'][0]['username']
# print(user_id)
# user_id = api.user_followers(user_id3, rank_token, max_id=2900)
# print(user_id)
# maxid = 0
# arr = []
# run = True
# while run:
#     for x in range(99):
#         try:
#             user_id = api.user_followers(user_id4, rank_token, max_id='100')['users'][x]['username']
#             arr.append(user_id)
#             sleep(1)
#             print(arr)
#         except:
#             print("Done")
#             run = False
#             break
#
#     maxid += 100

# def get following array
# for x in range(99):
#      try:
#         user_id = api.user_followers(user_id4, rank_token, max_id='100')['users'][x]['username']
#         arr.append(user_id)
#         sleep(1)
#      except:
#          if
#         print(arr)
# max_id = 100
# x = 0
# a = api.user_following(user_id3, rank_token, max_id=str(max_id))['users'][90]['username']
# print(a)


arr = []
x = 0
max_id = 0
numFollowing = api.username_info(username)['user']['following_count']
a = api.user_following(user_id3, rank_token)
while x < numFollowing:
    try:
        val = x % 100
        arr.append(a['users'][val]['username'])
        print(arr)
        sleep(.2)
    except IndexError:
        print("Done " + str(max_id))
        break
    except:
        print("rate/throttle error")
        break
    if ((x % 100) == 0) and (x != 0):
        max_id += 100
        a = api.user_following(user_id3, rank_token, max_id=str(max_id))
    x += 1
print("Done End " + str(max_id))