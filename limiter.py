from ratelimit import limits
import cache as c

FIFTEEN_MINUTES = 900
HOUR = 3600
DAY = 86400
DAILY_LIMIT = int(c.cache['daily_limit'])

def canUnfollow():
    try:
        print("checking day")
        if canUnfollowCheck3():
            try:
                print("checking hour")
                if canUnfollowCheck2():
                    try:
                        print("checking 15")
                        return canUnfollowCheck1()
                    except:
                        return '15min'
            except:
                return 'hour'
    except:
        return 'day'


@limits(calls=30, period=FIFTEEN_MINUTES)
def canUnfollowCheck1():
    return True

@limits(calls=60, period=HOUR)
def canUnfollowCheck2():
    return True

@limits(calls=DAILY_LIMIT, period=DAY)
def canUnfollowCheck3():
    return True


def canFollow():
    try:
        if canFollowCheck3():
            try:
                if canFollowCheck2():
                    try:
                        return canFollowCheck1()
                    except:
                        return '15min'
            except:
                return 'hour'
    except:
        return 'day'


@limits(calls=30, period=FIFTEEN_MINUTES)
def canFollowCheck1():
    return True


@limits(calls=60, period=HOUR)
def canFollowCheck2():
    return True


@limits(calls=DAILY_LIMIT, period=DAY)
def canFollowCheck3():
    return True

def canAuto(param):
    global go
    if param == 'can':
        go = True
    elif param == 'cannot':
        go = False
    elif param == 'check':
        return go
    else:
        return 'error'