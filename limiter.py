from ratelimit import limits
import cache as c

FIFTEEN_MINUTES = 900
HOUR = 3600
DAY = 86400
DAILY_LIMIT = int(c.cache['daily_limit'])
purgelist = []

def canUnfollow():
    try:
        if canUnfollowCheck3():
            try:
                if canUnfollowCheck2():
                    try:
                        return canUnfollowCheck1()
                    except:
                        return 'Cannot Unfollow- Reached 15 Minute Limit'
            except:
                return 'Cannot Unfollow- Reached Hourly Limit'
    except:
        return 'Cannot Unfollow- Reached Daily Limit'


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
                        return 'Cannot Follow- Reached 15 Minute Limit'
            except:
                return 'Cannot Follow- Reached Hourly Limit'
    except:
        return 'Cannot Follow- Reached Daily Limit'


@limits(calls=30, period=FIFTEEN_MINUTES)
def canFollowCheck1():
    return True


@limits(calls=60, period=HOUR)
def canFollowCheck2():
    return True


@limits(calls=DAILY_LIMIT, period=DAY)
def canFollowCheck3():
    return True

def canAutoPurge(param):
    global go
    if param == 'can':
        go = True
    elif param == 'cannot':
        go = False
    elif param == 'check':
        return go
    else:
        return 'error'

def canAutoCrawl(param):
    global go
    if param == 'can':
        go = True
    elif param == 'cannot':
        go = False
    elif param == 'check':
        return go
    else:
        return 'error'

def autoPurge(action, *v):
    global purgelist
    for val in v:
        value = val
    if action == 'add':
        purgelist.append(value)
    elif action == 'len':
        return len(purgelist)
    elif action == 'remove':
        try:
            x = purgelist[0]
            purgelist.pop(0)
            return x
        except:
            return 'error'
    elif action == 'removeManual':
        purgelist.remove(value)
