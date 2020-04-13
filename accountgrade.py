import math as m

def letter_grade(followers, ratio, engagement, avglikes):
    pc = calculate_grade(followers, ratio, engagement, avglikes)
    if pc > 1.25:
        return 'gold'
    elif pc > 1:
        return 'A+'
    elif pc > .85:
        return 'A'
    elif pc > .8:
        return 'A-'
    elif pc > .75:
        return 'B+'
    elif pc > .65:
        return 'B'
    elif pc > .6:
        return 'B-'
    elif pc > .55:
        return 'C+'
    elif pc > .45:
        return 'C'
    elif pc > .4:
        return 'C-'
    elif pc > .35:
        return 'D+'
    elif pc > .25:
        return 'D'
    elif pc > .2:
        return 'D-'
    else:
        return 'F'


def calculate_grade(followers, ratio, engagement, avglikes):
    g1 = calc_followers(followers)
    g2 = calc_avglikes(avglikes)
    g3 = calc_engagment(engagement, g1)
    g4 = calc_ratio(ratio)
    return (g1 * g1 + g2 * g2 + g3 + g4) / 3.5


def calc_followers(followers):
    x = (m.log(followers, 10)) / 5
    x = correction(x)
    return x


def calc_avglikes(avglikes):
    x = (m.log(avglikes, 10)) / 4
    x = correction(x)
    return x


def calc_engagment(engagement, g1):
    x = engagement * 3 * m.sqrt(g1)
    x = correction(x)
    return x


def calc_ratio(ratio):
    x = ratio / 2
    x = correction(x)
    return x


def correction(x):
    if x > 2:
        return 1.5
    elif x > 1:
        return (1 + x) / 2
    else:
        return x
