from instagram_private_api import (
        Client, ClientError, ClientLoginError,
        ClientCookieExpiredError, ClientLoginRequiredError,
        __version__ as client_version)

username = "testaccforapi"
user_id = 5565476890
api = Client("testaccforapi", "steelhead21", auto_patch=True)
rank_token = api.generate_uuid(return_hex=False, seed=None)
count = 0
running = True
page_size = api.user_followers(user_id, rank_token)['page_size']
page_size = int(100)
print(page_size)
while running:
    if count < 180:
        for x in range(page_size):
            print(api.user_followers(user_id, rank_token)['users'][x]['username'])
            count += 1
        next_max_id = api.user_followers(user_id, rank_token)['next_max_id']
        for x in range(page_size):
            print(api.user_followers(user_id, rank_token, max_id=next_max_id)['users'][x]['username'])
            count += 1
print(count)
# following_arr = []
# for following in api.username_info(username)['user']['following_count']:
#     following_arr.append()
# for user in following_arr[]
#     top_result = api.user_followers(api.username_info(username)['user']['pk'], rank_token)['users'][0]
#     if top_result == username:
#         print(True)
#     else:
#         print(False)








# count = 0
# rank_token = api.generate_uuid(return_hex=False, seed=None)
# for users in (api.user_followers(api.username_info('joshbenson_')['user']['pk'], rank_token)['users']):
#     count+=1
# print(count)

