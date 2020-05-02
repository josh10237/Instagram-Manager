import helpers as h
import cache as c
import limiter as l
from time import sleep

from instagram_private_api import (
    Client, ClientError, ClientLoginError,
    ClientCookieExpiredError, ClientLoginRequiredError,
    __version__ as client_version)

username = "testaccforapi"
api = Client("testaccforapi", "steelhead21", auto_patch=True)
# rank_token = api.generate_uuid(return_hex=False, seed=None)
# rank_token = '2abc9200-76e4-11ea-ab20-001a7dda7113'
# user_id1 = "32341377860"  # testaccforapi
# user_id2 = "5565476890"  # ella
# user_id3 = "243946204"  # josh
# user_id4 = "32649564590"  # pratik
# arr = [user_id1, user_id2, user_id3]

def get_last_post_id(username):
    return api.username_feed(username)['items'][0]['id']

def get_likers_post(media_id):
    print(len(api.media_likers(media_id)['users']))
    return api.media_likers(media_id)['users']


if __name__ == '__main__':
    id = get_last_post_id(username)
    api.media_likers(id)['users']
    # tot = len(api.media_likers(id)['users'])
    # count = 0
    # while count < tot:
    #     arr = api.media_likers(id)['users'][count]
    #     user_name = arr['username']
    #     profile = arr['profile_pic_url']
    #     user_id = arr['pk']
    #     count += 1
    #     print(str(user_name) + " " + str(user_id) + " " + profile)