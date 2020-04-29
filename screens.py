import threading
from kivy.uix.popup import Popup
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from threading import Thread
import helpers as h
import cache as c
import limiter as l
from time import sleep
import accountgrade as ag
from kivy.core.window import Window, Animation
from kivy.graphics.context_instructions import Color
from kivy.properties import NumericProperty, ColorProperty, ObjectProperty
from kivy.uix.image import Image, AsyncImage
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.textinput import TextInput
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.anchorlayout import AnchorLayout
from concurrent.futures import ThreadPoolExecutor
import threading
from random import randint
import time

SCREEN_MANAGER = ScreenManager()
runningPurgeAuto = False
runningCrawlAuto = False


class instagramManagerApp(App):
    def build(self):
        username = ''
        password = ''
        try:
            username = c.retrieve_log_in('username')
            password = c.retrieve_log_in('password')
        except:
            pass
        if len(username) > 1 and len(password) > 1:
            SCREEN_MANAGER.current = 'remember'
        else:
            SCREEN_MANAGER.current = 'newUser'
        l.canAutoPurge('cannot')
        return SCREEN_MANAGER


Window.clearcolor = (1, 1, 1, 1)
Window.size = (800, 550)
Window.minimum_width, Window.minimum_height = Window.size


class RememberScreen(Screen):
    def check_cache(self):
        self.ids.enter_button.text = "Continue as @" + c.retrieve_log_in('username')
        try:
            profile_pic = c.retrieve_profile_pic()
            if len(profile_pic) < 5:
                profile_pic = h.get_profile_pic()
        except:
            SCREEN_MANAGER.current = 'newUser'
        self.ids.profile.source = profile_pic
        c.dash_set_up()

    def continue_remember(self):
        SCREEN_MANAGER.current = 'dashboard'

    def switch_account(self, str1):
        if str1 == 'press':
            self.ids.switch_acc.color = (0, 0, 0, .7)
        else:
            SCREEN_MANAGER.current = 'newUser'


class NewUserScreen(Screen):
    def logIn(self):
        self.ids.error_info.text = ' '
        username = self.ids.username.text
        password = self.ids.password.text
        if len(username) < 2 or len(password) < 2:
            self.ids.error_info.text = 'Please enter a valid log in'
        elif h.new_API(username, password) == 'error':

            self.ids.error_info.text = 'Invalid Log In'
        else:
            c.clear_cache()
            c.cache_log_in(username, password)
            SCREEN_MANAGER.current = 'dashboard'


class ImageButton(ButtonBehavior, AsyncImage):
    pass


class DashboardScreen(Screen):
    def settings(self):
        SCREEN_MANAGER.current = 'settings'

    def purgeScreen(self):
        SCREEN_MANAGER.current = 'purge'

    def crawlScreen(self):
        SCREEN_MANAGER.current = 'crawl'

    def AGbreakdown(self):
        if self.ids.followers_grade.text != "-":
            self.ids.followers_grade.color = (0, 0, 0, 0)
            self.ids.avglikes_grade.color = (0, 0, 0, 0)
            self.ids.engagement_grade.color = (0, 0, 0, 0)
            self.ids.ratio_grade.color = (0, 0, 0, 0)
            self.ids.followers_grade.text = "-"
        else:
            arr = c.retrieve_grade_tips()
            self.ids.followers_grade.text = "%" + str("%.2f" % round(arr[0], 2))
            self.ids.followers_grade.color = (0, 0, 0, 1)
            self.ids.avglikes_grade.text = "%" + str("%.2f" % round(arr[1], 2))
            self.ids.avglikes_grade.color = (0, 0, 0, 1)
            self.ids.engagement_grade.text = "%" + str("%.2f" % round(arr[2], 2))
            self.ids.engagement_grade.color = (0, 0, 0, 1)
            self.ids.ratio_grade.text = "%" + str("%.2f" % round(arr[3], 2))
            self.ids.ratio_grade.color = (0, 0, 0, 1)

    def refresh(self, *args):
        arg1 = ''
        for arg in args:
            arg1 = arg
        self.ids.refresh.y = Window.height + 500
        try:
            profile_pic = c.retrieve_profile_pic()
            if len(profile_pic) < 5:
                profile_pic = h.get_profile_pic()
                c.cache_profile_pic(profile_pic)
        except:
            profile_pic = h.get_profile_pic()
            c.cache_profile_pic(profile_pic)
        self.ids.profile_photo.source = profile_pic
        self.ids.user_label.text = "@" + c.retrieve_log_in('username')
        arr = c.retrieve_dash()
        try:
            followers = arr[0]
            following = arr[1]
            dfmb = arr[2]
            avglikes = arr[3]
        except:
            c.dash_set_up()
            arr = c.retrieve_dash()
            followers = arr[0]
            following = arr[1]
            dfmb = arr[2]
            avglikes = arr[3]
        if arg1 == 'manual':
            c.dash_set_up()
            arr = c.retrieve_dash()
            followers = arr[0]
            following = arr[1]
            dfmb = arr[2]
            avglikes = arr[3]
        ratio = followers / following
        engagemnet = avglikes / followers
        self.ids.letter_grade.text = ag.letter_grade(followers, ratio, engagemnet, avglikes)
        self.ids.followers.text = str(followers)
        self.ids.following.text = str(following)
        self.ids.ratio.text = "%.2f" % round(ratio, 2)
        self.ids.avg_likes.text = "%.2f" % round(avglikes, 2)
        self.ids.dfmb.text = str(dfmb)
        self.ids.engagement.text = "%.2f" % round(engagemnet, 2)
        self.ids.refresh.y = Window.height * 0.95 - 40


class UnfollowButton(Button):
    def __init__(self, calling_obj, userRowObj, **kwargs):
        super(UnfollowButton, self).__init__(**kwargs)
        self.bind(on_release=self.unfollow)
        self.calling_obj = calling_obj
        self.userRowObj = userRowObj

    def unfollow(self, instance):
        m = l.canUnfollow()
        rt = self.calling_obj
        # LEAVE AS "== True"   DO NOT SIMPLIFY THE EXPRESSION
        if m == True:
            lt = self.userRowObj.layout
            id = self.userRowObj.user_id
            l.autoPurge('removeManual', (lt,id))
            rt.remove_row(lt)
            h.unfollow(id)
        else:
            rt.unfollow_error(m)


class CrawlScreen(Screen):
    def backButton(self):
        SCREEN_MANAGER.current = 'dashboard'

    def base(self):
        SCREEN_MANAGER.current = 'base'

    # def toggle_crawl(self):
    #     if self.ids.toggle_crawl_button.text == "Start Crawl":
    #         self.ids.widget_list.clear_widgets()
    #         self.ids.toggle_crawl_button.text = "Running..."
    #         x = threading.Thread(target=self.crawlThread, daemon=True)
    #         x.start()
    #
    # def crawlThread(self):
    #     tot = 0
    #     dfmb = 0
    #     self.ids.pc.bold = False
    #     self.ids.pc.color = (0, 0, 0, 1)
    #     similar_arr = c.retrieve_similar()
    #     while tot < len(following_arr):
    #         arr = h.dynamic_DFMB(following_arr, tot)
    #         if arr[0] == 'nil':
    #             self.update_percent(arr[1])
    #         else:
    #             # profile, user_id, username, percent
    #             self.add_row(arr[0], arr[1], arr[2], arr[3])
    #             self.update_percent(arr[3])
    #             dfmb += 1
    #         tot += 1
    #     dash = c.retrieve_dash()
    #     dash[2] = dfmb
    #     c.cache_dash(dash)
    #     l.canAutoPurge('can')
    #     if self.ids.set_auto_button.text == "Turn Off Automatic":
    #         self.ids.set_auto_button.text = "Turn On Automatic"
    #         self.toggle_auto()
    #     self.ids.toggle_purge_button.text = "Start Purge"
    #
    def pullSettings(self):
        if c.cache['crawl_control'] == 'auto':
            self.ids.set_auto_button.text = "Turn Off Automatic"
            # self.toggle_auto()
        else:
            self.ids.set_auto_button.text = "Turn On Automatic"
    #
    # def toggle_auto(self):
    #     if self.ids.set_auto_button.text == "Turn On Automatic":
    #         self.ids.set_auto_button.text = "Turn Off Automatic"
    #         c.cache['crawl_control'] = 'auto'
    #         # x = threading.Thread(target=self.followThread, daemon=True)
    #         # x.start()
    #     else:
    #         self.ids.set_auto_button.text = "Turn On Automatic"
    #         c.cache['crawl_control'] = 'manual'
    #
    # def followThread(self):
    #     global runningCrawlAuto
    #     if runningCrawlAuto:
    #         return
    #     while self.ids.set_auto_button.text == "Turn Off Automatic" and l.canAutoPurge('check') == True:
    #         runningCrawlAuto = True
    #         if c.cache['speed'] == 'slow':
    #             t = randint(60, 70)
    #         elif c.cache['speed'] == 'med':
    #             t = randint(30, 35)
    #         elif c.cache['speed'] == 'fast':
    #             t = randint(5, 10)
    #         while t > 0 and self.ids.set_auto_button.text == "Turn Off Automatic":
    #             mins, secs = divmod(t, 60)
    #             self.ids.auto_timer.text = '{:01d}:{:02d}'.format(mins, secs)
    #             time.sleep(1)
    #             t -= 1
    #         print("done")
    #         tmp = l.autoPurge('remove')
    #         if tmp == 'error':
    #             return
    #         else:
    #             tup = tmp
    #             lay = tup[0]
    #             id = tup[1]
    #         checker = l.canAutoPurge('check')
    #         if checker == True:
    #             self.remove_row(lay)
    #             h.unfollow(id)
    #         else:
    #             self.unfollow_error(checker)
    #             return
    #     self.ids.auto_timer.text = ""
    #     runningCrawlAuto = False


class BaseScreen(Screen):
    def backButton(self):
        SCREEN_MANAGER.current = 'crawl'

    def pullCache(self):
        print('pulled')
        arr = c.retrieve_similar()
        for user in arr:
            # profile, user_idm, user_name
            self.add_row(user[0], user[1], user[2])
        self.add_row('empty', None, None)

    def add_row(self, profile, user_id, user_name):
        u = UserRow(self, profile, user_id, user_name)
        g = u.create_layout_base()
        self.ids.widget_list.add_widget(g)


class UserRow(GridLayout):
    def __init__(self, obj, profile, user_id, user_name):
        self.calling_obj = obj
        self.profile = profile
        self.user_id = user_id
        self.user_name = user_name
        self.layout = None

    def create_layout_purge(self):
        layout = GridLayout(rows=1, row_force_default=True, row_default_height=60)
        layout.add_widget(ImageButton(source=self.profile))
        layout.add_widget(Label(text="@" + self.user_name, color=(0, 0, 0, .8), halign="left",
                                valign="middle", text_size=(300, None)))
        bsplit = GridLayout(rows=1)
        unfollowButton = UnfollowButton(self.calling_obj, self,
                                        background_normal='images/buttonbackgrounds/unfollow.png',
                                        background_down='images/buttonbackgrounds/unfollow_select.png',
                                        size_hint_x=None, width=100)
        bsplit.add_widget(unfollowButton)
        bsplit.add_widget(Button(background_normal='images/buttonbackgrounds/waitlist.png',
                                 background_down='images/buttonbackgrounds/waitlist_select.png',
                                 width=50, height=50, size_hint_x=None, size_hint_y=None,
                                 valign="middle", border=(3, 3, 3, 3)))
        layout.add_widget(bsplit)
        self.layout = layout
        return layout

    def create_layout_base(self):
        layout = GridLayout(rows=1, row_force_default=True, row_default_height=60)
        layout.add_widget(ImageButton(source=self.profile))
        layout.add_widget(Label(text="@" + self.user_name, color=(0, 0, 0, .8), halign="left",
                                valign="middle", text_size=(300, None)))
        bsplit = GridLayout(rows=1)
        removeButton = UnfollowButton(self.calling_obj, self,
                                        background_normal='images/buttonbackgrounds/unfollow.png',
                                        background_down='images/buttonbackgrounds/unfollow_select.png',
                                        size_hint_x=None, width=100)
        bsplit.add_widget(removeButton)
        layout.add_widget(bsplit)
        self.layout = layout
        return layout


class PurgeScreen(Screen):
    def backButton(self):
        SCREEN_MANAGER.current = 'dashboard'

    def add_row(self, profile, user_id, user_name, percent):
        u = UserRow(self, profile, user_id, user_name)
        g = u.create_layout_purge()
        l.autoPurge('add', (g, user_id))
        self.ids.widget_list.add_widget(g)
        self.update_percent(percent)

    def update_percent(self, percent):
        pc = percent * 100
        p = "%.2f" % round(pc, 2)
        self.ids.pc.text = "%" + p

    def remove_row(self, lay):
        self.ids.widget_list.remove_widget(lay)
        print("Did it: ")
        print(lay)

    def unfollow_error(self, m):
        self.ids.pc.color = (1, .2, .2, 1)
        self.ids.pc.bold = True
        self.ids.pc.text = m

    def toggle_purge(self):
        if self.ids.toggle_purge_button.text == "Start Purge":
            self.ids.widget_list.clear_widgets()
            self.ids.toggle_purge_button.text = "Running..."
            x = threading.Thread(target=self.purgeThread, daemon=True)
            x.start()

    def purgeThread(self):
        tot = 0
        dfmb = 0
        self.ids.pc.bold = False
        self.ids.pc.color = (0, 0, 0, 1)
        following_arr = h.get_following_array(c.retrieve_log_in('username'))
        while tot < len(following_arr):
            arr = h.dynamic_DFMB(following_arr, tot)
            if arr[0] == 'nil':
                self.update_percent(arr[1])
            else:
                # profile, user_id, username, percent
                self.add_row(arr[0], arr[1], arr[2], arr[3])
                self.update_percent(arr[3])
                dfmb += 1
            tot += 1
        dash = c.retrieve_dash()
        dash[2] = dfmb
        c.cache_dash(dash)
        l.canAutoPurge('can')
        if self.ids.set_auto_button.text == "Turn Off Automatic":
            self.ids.set_auto_button.text = "Turn On Automatic"
            self.toggle_auto()
        self.ids.toggle_purge_button.text = "Start Purge"

    def pullSettings(self):
        if c.cache['purge_control'] == 'auto':
            self.ids.set_auto_button.text = "Turn On Automatic"
            self.toggle_auto()
        else:
            self.ids.set_auto_button.text = "Turn On Automatic"

    def toggle_auto(self):
        if self.ids.set_auto_button.text == "Turn On Automatic":
            self.ids.set_auto_button.text = "Turn Off Automatic"
            c.cache['purge_control'] = 'auto'
            x = threading.Thread(target=self.unfollowThread, daemon=True)
            x.start()
        else:
            self.ids.set_auto_button.text = "Turn On Automatic"
            c.cache['purge_control'] = 'manual'

    def unfollowThread(self):
        global runningPurgeAuto
        if runningPurgeAuto:
            return
        while self.ids.set_auto_button.text == "Turn Off Automatic" and l.canAutoPurge('check') == True:
            runningPurgeAuto = True
            if c.cache['speed'] == 'slow':
                t = randint(60, 70)
            elif c.cache['speed'] == 'med':
                t = randint(30, 35)
            elif c.cache['speed'] == 'fast':
                t = randint(5, 10)
            while t > 0 and self.ids.set_auto_button.text == "Turn Off Automatic":
                mins, secs = divmod(t, 60)
                self.ids.auto_timer.text = '{:01d}:{:02d}'.format(mins, secs)
                time.sleep(1)
                t -= 1
            print("done")
            tmp = l.autoPurge('remove')
            if tmp == 'error':
                return
            else:
                tup = tmp
                lay = tup[0]
                id = tup[1]
            checker = l.canAutoPurge('check')
            if checker == True:
                self.remove_row(lay)
                h.unfollow(id)
            else:
                self.unfollow_error(checker)
                return
        self.ids.auto_timer.text = ""
        runningPurgeAuto = False


class SettingsScreen(Screen):

    def pull_settings(self):
        try:  # pull from cache
            mutual_friends = c.cache['mutual_friends']
            crawl_control = c.cache['crawl_control']
            purge_control = c.cache['purge_control']
            ratio_vl = c.cache['ratio_vl']
            ratio_l = c.cache['ratio_l']
            ratio_h = c.cache['ratio_h']
            ratio_vh = c.cache['ratio_vh']
            whitelist_legnth = c.cache['whitelist_legnth']
            speed = c.cache['speed']
            daily_limit = c.cache['daily_limit']
        except:  # cache defualts and re-run
            c.cache['mutual_friends'] = '30+'
            c.cache['crawl_control'] = 'manual'
            c.cache['purge_control'] = 'manual'
            c.cache['ratio_vl'] = True
            c.cache['ratio_l'] = True
            c.cache['ratio_h'] = True
            c.cache['ratio_vh'] = False
            c.cache['whitelist_legnth'] = '10'
            c.cache['speed'] = 'slow'
            c.cache['daily_limit'] = '100'
            self.pull_settings()
        if mutual_friends == '10+':
            self.tenplus()
        elif mutual_friends == '30+':
            self.thirtyplus()
        elif mutual_friends == '50+':
            self.fiftyplus()
        elif mutual_friends == '100+':
            self.thirtyplus()
        if crawl_control == 'manual':
            self.manual('crawl')
        elif crawl_control == 'auto':
            self.automatic('crawl')
        if purge_control == 'manual':
            self.manual('purge')
        elif purge_control == 'auto':
            self.automatic('purge')
        if ratio_vl:
            self.ids.verylow.background_normal = 'images/settingbackgrounds/verylow_select.png'
        else:
            self.ids.verylow.background_normal = 'images/settingbackgrounds/verylow.png'
        if ratio_l:
            self.ids.low.background_normal = 'images/settingbackgrounds/low_select.png'
        else:
            self.ids.low.background_normal = 'images/settingbackgrounds/low.png'
        if ratio_h:
            self.ids.high.background_normal = 'images/settingbackgrounds/high_select.png'
        else:
            self.ids.high.background_normal = 'images/settingbackgrounds/high.png'
        if ratio_vh:
            self.ids.veryhigh.background_normal = 'images/settingbackgrounds/veryhigh_select.png'
        else:
            self.ids.veryhigh.background_normal = 'images/settingbackgrounds/veryhigh.png'
        if whitelist_legnth == '5':
            self.fivedays()
        elif whitelist_legnth == '10':
            self.tendays()
        elif whitelist_legnth == '15':
            self.fifteendays()
        if speed == 'slow':
            self.slow()
        elif speed == 'med':
            self.med()
        elif speed == 'fast':
            self.fast()
        if daily_limit == '100':
            self.hundred()
        elif daily_limit == '150':
            self.hundredfifty()
        elif daily_limit == '200':
            self.twohundred()

    def backButton(self):
        SCREEN_MANAGER.current = 'dashboard'

    def tenplus(self):
        self.ids.tenplus.background_normal = 'images/settingbackgrounds/10+_select.png'
        self.ids.thirtyplus.background_normal = 'images/settingbackgrounds/30+.png'
        self.ids.fiftyplus.background_normal = 'images/settingbackgrounds/50+.png'
        self.ids.hundredplus.background_normal = 'images/settingbackgrounds/100+.png'
        c.cache['mutual_friends'] = '10+'

    def thirtyplus(self):
        self.ids.tenplus.background_normal = 'images/settingbackgrounds/10+.png'
        self.ids.thirtyplus.background_normal = 'images/settingbackgrounds/30+_select.png'
        self.ids.fiftyplus.background_normal = 'images/settingbackgrounds/50+.png'
        self.ids.hundredplus.background_normal = 'images/settingbackgrounds/100+.png'
        c.cache['mutual_friends'] = '30+'

    def fiftyplus(self):
        self.ids.tenplus.background_normal = 'images/settingbackgrounds/10+.png'
        self.ids.thirtyplus.background_normal = 'images/settingbackgrounds/30+.png'
        self.ids.fiftyplus.background_normal = 'images/settingbackgrounds/50+_select.png'
        self.ids.hundredplus.background_normal = 'images/settingbackgrounds/100+.png'
        c.cache['mutual_friends'] = '50+'

    def hundredplus(self):
        self.ids.tenplus.background_normal = 'images/settingbackgrounds/10+.png'
        self.ids.thirtyplus.background_normal = 'images/settingbackgrounds/30+.png'
        self.ids.fiftyplus.background_normal = 'images/settingbackgrounds/50+.png'
        self.ids.hundredplus.background_normal = 'images/settingbackgrounds/100+_select.png'
        c.cache['mutual_friends'] = '100+'

    def manual(self, type):
        if type == 'crawl':
            self.ids.crawlmanual.background_normal = 'images/settingbackgrounds/manual_select.png'
            self.ids.crawlautomatic.background_normal = 'images/settingbackgrounds/automatic.png'
            c.cache['crawl_control'] = 'manual'
        else:
            self.ids.purgemanual.background_normal = 'images/settingbackgrounds/manual_select.png'
            self.ids.purgeautomatic.background_normal = 'images/settingbackgrounds/automatic.png'
            c.cache['purge_control'] = 'manual'

    def automatic(self, type):
        if type == 'crawl':
            self.ids.crawlmanual.background_normal = 'images/settingbackgrounds/manual.png'
            self.ids.crawlautomatic.background_normal = 'images/settingbackgrounds/automatic_select.png'
            c.cache['crawl_control'] = 'auto'
        else:
            self.ids.purgemanual.background_normal = 'images/settingbackgrounds/manual.png'
            self.ids.purgeautomatic.background_normal = 'images/settingbackgrounds/automatic_select.png'
            c.cache['purge_control'] = 'auto'

    def verylow(self):
        if self.ids.verylow.background_normal == 'images/settingbackgrounds/verylow.png':
            self.ids.verylow.background_normal = 'images/settingbackgrounds/verylow_select.png'
            c.cache['ratio_vl'] = True
        else:
            self.ids.verylow.background_normal = 'images/settingbackgrounds/verylow.png'
            c.cache['ratio_vl'] = False

    def low(self):
        if self.ids.low.background_normal == 'images/settingbackgrounds/low.png':
            self.ids.low.background_normal = 'images/settingbackgrounds/low_select.png'
            c.cache['ratio_l'] = True
        else:
            self.ids.low.background_normal = 'images/settingbackgrounds/low.png'
            c.cache['ratio_l'] = False

    def high(self):
        if self.ids.high.background_normal == 'images/settingbackgrounds/high.png':
            self.ids.high.background_normal = 'images/settingbackgrounds/high_select.png'
            c.cache['ratio_h'] = True
        else:
            self.ids.high.background_normal = 'images/settingbackgrounds/high.png'
            c.cache['ratio_h'] = False

    def veryhigh(self):
        if self.ids.veryhigh.background_normal == 'images/settingbackgrounds/veryhigh.png':
            self.ids.veryhigh.background_normal = 'images/settingbackgrounds/veryhigh_select.png'
            c.cache['ratio_vh'] = True
        else:
            self.ids.veryhigh.background_normal = 'images/settingbackgrounds/veryhigh.png'
            c.cache['ratio_vh'] = False

    def fivedays(self):
        self.ids.fivedays.background_normal = 'images/settingbackgrounds/5days_select.png'
        self.ids.tendays.background_normal = 'images/settingbackgrounds/10days.png'
        self.ids.fifteendays.background_normal = 'images/settingbackgrounds/15days.png'
        c.cache['whitelist_legnth'] = '5'

    def tendays(self):
        self.ids.fivedays.background_normal = 'images/settingbackgrounds/5days.png'
        self.ids.tendays.background_normal = 'images/settingbackgrounds/10days_select.png'
        self.ids.fifteendays.background_normal = 'images/settingbackgrounds/15days.png'
        c.cache['whitelist_legnth'] = '10'

    def fifteendays(self):
        self.ids.fivedays.background_normal = 'images/settingbackgrounds/5days.png'
        self.ids.tendays.background_normal = 'images/settingbackgrounds/10days.png'
        self.ids.fifteendays.background_normal = 'images/settingbackgrounds/15days_select.png'
        c.cache['whitelist_legnth'] = '15'

    def slow(self):
        self.ids.slow.background_normal = 'images/settingbackgrounds/slow_select.png'
        self.ids.med.background_normal = 'images/settingbackgrounds/med.png'
        self.ids.fast.background_normal = 'images/settingbackgrounds/fast.png'
        c.cache['speed'] = 'slow'

    def med(self):
        self.ids.slow.background_normal = 'images/settingbackgrounds/slow.png'
        self.ids.med.background_normal = 'images/settingbackgrounds/med_select.png'
        self.ids.fast.background_normal = 'images/settingbackgrounds/fast.png'
        c.cache['speed'] = 'med'

    def fast(self):
        self.ids.slow.background_normal = 'images/settingbackgrounds/slow.png'
        self.ids.med.background_normal = 'images/settingbackgrounds/med.png'
        self.ids.fast.background_normal = 'images/settingbackgrounds/fast_select.png'
        c.cache['speed'] = 'fast'

    def hundred(self):
        self.ids.hundred.background_normal = 'images/settingbackgrounds/100_select.png'
        self.ids.hundredfifty.background_normal = 'images/settingbackgrounds/150.png'
        self.ids.twohundred.background_normal = 'images/settingbackgrounds/200.png'
        c.cache['daily_limit'] = '100'

    def hundredfifty(self):
        self.ids.hundred.background_normal = 'images/settingbackgrounds/100.png'
        self.ids.hundredfifty.background_normal = 'images/settingbackgrounds/150_select.png'
        self.ids.twohundred.background_normal = 'images/settingbackgrounds/200.png'
        c.cache['daily_limit'] = '150'

    def twohundred(self):
        self.ids.hundred.background_normal = 'images/settingbackgrounds/100.png'
        self.ids.hundredfifty.background_normal = 'images/settingbackgrounds/150.png'
        self.ids.twohundred.background_normal = 'images/settingbackgrounds/200_select.png'
        c.cache['daily_limit'] = '200'


Builder.load_file('screens/login.kv')
Builder.load_file('screens/dashboard.kv')
Builder.load_file('screens/settings.kv')
Builder.load_file('screens/purge.kv')
Builder.load_file('screens/crawl.kv')
Builder.load_file('screens/base.kv')
SCREEN_MANAGER.add_widget(SettingsScreen(name='settings'))
SCREEN_MANAGER.add_widget(RememberScreen(name='remember'))
SCREEN_MANAGER.add_widget(CrawlScreen(name='crawl'))
SCREEN_MANAGER.add_widget(PurgeScreen(name='purge'))
SCREEN_MANAGER.add_widget(BaseScreen(name='base'))
SCREEN_MANAGER.add_widget(NewUserScreen(name='newUser'))
SCREEN_MANAGER.add_widget(DashboardScreen(name='dashboard'))
