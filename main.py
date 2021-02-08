import helpers as h
import cache as c
import limiter as l
from datetime import timedelta, date
from time import sleep

from instagram_private_api import (
    Client, ClientError, ClientLoginError,
    ClientCookieExpiredError, ClientLoginRequiredError,
    __version__ as client_version)

username = "testaccforapi"
api = Client(username, password, auto_patch=True)


if __name__ == '__main__':
    # EndDate = date.today() + timedelta(days=10)
    # print(EndDate)
    pass
