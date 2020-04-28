global unfollows
global follows
from ratelimit import limits
import cache as c

FIFTEEN_MINUTES = 900
HOUR = 3600
DAY = 86400
DAILY_LIMIT = int(c.cache['daily_limit'])

@limits(calls=30, period=FIFTEEN_MINUTES)
@limits(calls=60, period=HOUR)
@limits(calls=DAILY_LIMIT, period=DAY)
def canUnfollow():
    return True
