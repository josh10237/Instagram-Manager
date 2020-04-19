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

SCREEN_MANAGER = ScreenManager()


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
        return SCREEN_MANAGER


Window.clearcolor = (1, 1, 1, 1)
Window.size = (800, 550)


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
        h.startThread('dash', self)

    def continue_remember(self):
        SCREEN_MANAGER.current = 'dashboard'

    def switch_account(self, str):
        if str == 'press':
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
            print('auto')
        except:
            h.dashThread()
            arr = c.retrieve_dash()
            followers = arr[0]
            following = arr[1]
            dfmb = arr[2]
            avglikes = arr[3]
            print('error- manual')
        if arg1 == 'manual':
            h.dashThread()
            arr = c.retrieve_dash()
            followers = arr[0]
            following = arr[1]
            dfmb = arr[2]
            avglikes = arr[3]
            print('manual refresh')
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

class CrawlScreen(Screen):
    def backButton(self):
        SCREEN_MANAGER.current = 'dashboard'


class PurgeScreen(Screen):
    def backButton(self):
        SCREEN_MANAGER.current = 'dashboard'

    def add_row(self, user_name, user_id, profile, percent):
        layout = GridLayout(rows=1, row_force_default=True, row_default_height=60)
        layout.add_widget(ImageButton(source=profile))
        layout.add_widget(Label(text="@" + user_name, color=(0, 0, 0, 1), font_size=25))
        layout.add_widget(Label(text=str(user_id), color=(0, 0, 0, 0), font_size=25))
        bsplit = GridLayout(rows=1)
        bsplit.add_widget(Button(background_normal='images/buttonbackgrounds/unfollow.png',
                                 background_down='images/buttonbackgrounds/unfollow_select.png', size_hint_x=None, width=100))
        bsplit.add_widget(Button(background_normal='images/buttonbackgrounds/waitlist.png',
                                 background_down='images/buttonbackgrounds/waitlist_select.png', size_hint_x=.5, border=(3,3,3,3)))
        layout.add_widget(bsplit)
        self.ids.widget_list.add_widget(layout)

    def toggle_purge(self):
        if self.ids.toggle_purge_button.text == "Start Purge":
            h.startThread('purge', self)
        else:
            pass

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
            print("recursive call")
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
# Builder.load_file('screens/crawl.kv')
SCREEN_MANAGER.add_widget(SettingsScreen(name='settings'))
SCREEN_MANAGER.add_widget(RememberScreen(name='remember'))
# SCREEN_MANAGER.add_widget(CrawlScreen(name='crawl'))
SCREEN_MANAGER.add_widget(PurgeScreen(name='purge'))
SCREEN_MANAGER.add_widget(NewUserScreen(name='newUser'))
SCREEN_MANAGER.add_widget(DashboardScreen(name='dashboard'))
