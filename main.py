import helpers as h
import cache as c
import limiter as l
from time import sleep

from instagram_private_api import (
    Client, ClientError, ClientLoginError,
    ClientCookieExpiredError, ClientLoginRequiredError,
    __version__ as client_version)

# username = "ellabenson04"
# api = Client("ellabenson04", "Jesse2dog", auto_patch=True)
# rank_token = api.generate_uuid(return_hex=False, seed=None)
# rank_token = '2abc9200-76e4-11ea-ab20-001a7dda7113'
# user_id1 = "32341377860"  # testaccforapi
# user_id2 = "5565476890"  # ella
# user_id3 = "243946204"  # josh
# user_id4 = "32649564590"  # pratik
# arr = [user_id1, user_id2, user_id3]


if __name__ == '__main__':
    # print(l.canUnfollow())
    # print("1 done")
    # print(l.canUnfollow())
    # print("2 done")
    # print(l.canUnfollow())
    # print("3 done")
    # print(l.canUnfollow())
    for x in range (0,10):
        m = l.canUnfollow()
        if m == True:
            print("did it")
        else:
            print(m)

