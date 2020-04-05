import helpers as h

from instagram_private_api import (
    Client, ClientError, ClientLoginError,
    ClientCookieExpiredError, ClientLoginRequiredError,
    __version__ as client_version)

username = "testaccforapi"
api = Client("testaccforapi", "steelhead21", auto_patch=True)
#rank_token = api.generate_uuid(return_hex=False, seed=None)
rank_token = '2abc9200-76e4-11ea-ab20-001a7dda7113'
user_id1 = "32341377860" #testaccforapi
user_id2 = "5565476890" #ella
user_id3 = "243946204" #josh
arr = [user_id1, user_id2, user_id3]
#print(len(api.user_following(user_id2, rank_token, max_id=0)['users']))
#print(api.user_following(user_id2, rank_token, max_id=100))
print(api.user_following(user_id2, rank_token, max_id=100))

# maxid = 0
# arr = []
# run = True
# while run:
#     for x in range (99):
#         try:
#             id = api.user_following(user_id2, rank_token, max_id=maxid)['users'][x]['username']
#             arr.append(id)
#         except:
#             print(arr)
#             run = False
#
#     maxid += 100