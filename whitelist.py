import cache as c
from datetime import timedelta, date


def retrieve_whitelist():
    return c.cache['whitelist']


def whitelist(arr):
    w = c.cache['whitelist']
    # profile, user_id, user_name
    try:
        w.insert(0, (arr[0], arr[1], arr[2], None))
    except AttributeError:
        w = [(arr[0], arr[1], arr[2], None)]
    c.cache['whitelist'] = w


def whitelist_timer(arr):
    w = c.cache['whitelist']
    if w == None:
        return
    timeAdd = int(c.cache['whitelist_legnth'])
    expiration = date.today() + timedelta(days=timeAdd)
    # profile, user_id, user_name
    w.append((arr[0], arr[1], arr[2], expiration))
    c.cache['whitelist'] = w


def update_whitelist():
    w = c.cache['whitelist']
    if w == None:
        return
    for item in w:
        if item[3] is not None and item[3] > date.today():
            w.remove(item)
    c.cache['whitelist'] = w


def diff_dates(expDate):
    if expDate is None:
        return None
    return expDate - date.today()


def remove_from_whitelist(user_id):
    w = c.cache['whitelist']
    if w == None:
        return
    for item in w:
        if item[1] == user_id:
            w.remove(item)
            c.cache['whitelist'] = w
            return
    return "error not found"


def offWaitlist(user_id):
    w = c.cache['whitelist']
    if w == None:
        return True
    for item in w:
        if item[1] == user_id:
            print(item[2])
            return False
    return True


def clear_whitelist():
    c.cache['whitelist'] = None

