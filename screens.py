from kivy.app import App
import helpers as h
import cache as c
import accountgrade as ag
from kivy.core.window import Window, Animation
from kivy.graphics.context_instructions import Color
from kivy.properties import NumericProperty, ColorProperty
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
        # if h.remember_api() == 400:
        #     SCREEN_MANAGER.current = 'newUser'

    def continue_remember(self):
        h.new_API(c.retrieve_log_in('username'), c.retrieve_log_in('password'))
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
            c.cache_log_in(username, password)
            SCREEN_MANAGER.current = 'dashboard'


class ImageButton(ButtonBehavior, AsyncImage):
    pass


class DashboardScreen(Screen):
    def settings(self):
        SCREEN_MANAGER.current = 'settings'

    def refresh(self):
        self.ids.refresh.y = Window.height
        try:
            profile_pic = c.retrieve_profile_pic()
            print(profile_pic)
            print('1')
            if len(profile_pic) < 5:
                profile_pic = h.get_profile_pic()
                c.cache_profile_pic(profile_pic)
                print(profile_pic)
                print('2')
        except:
            profile_pic = h.get_profile_pic()
            c.cache_profile_pic(profile_pic)
            print(profile_pic)
            print('3')
        self.ids.profile_photo.source = profile_pic
        self.ids.user_label.text = "@" + c.retrieve_log_in('username')
        followers = h.getFollowers(c.retrieve_log_in('username'))
        following = h.getFollowing(c.retrieve_log_in('username'))
        ratio = followers / following
        dfmb = h.getDFMB(c.retrieve_log_in('username'), 0)
        avglikes = h.getAverageLikes(c.retrieve_log_in('username'))
        engagemnet = avglikes / followers
        self.ids.letter_grade.text = ag.letter_grade(followers, ratio, engagemnet, avglikes)
        self.ids.followers.text = str(followers)
        self.ids.following.text = str(following)
        self.ids.ratio.text = "%.2f" % round(ratio, 2)
        self.ids.avg_likes.text = "%.2f" % round(ratio, 2)
        self.ids.dfmb.text = str(dfmb)
        self.ids.avg_likes.text = str(avglikes)
        self.ids.engagement.text = "%.2f" % round(engagemnet, 2)
        self.ids.refresh.y = Window.height * 0.9 - 15


class SettingsScreen(Screen):

    def pull_settings(self):
        mutual_friends = ''
        crawl_control = ''
        purge_control = ''
        ratio_vl = ''
        ratio_l = ''
        ratio_h = ''
        ratio_vh = ''
        whitelist_legnth = ''
        speed = ''
        daily_limit = ''
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
SCREEN_MANAGER.add_widget(SettingsScreen(name='settings'))
SCREEN_MANAGER.add_widget(RememberScreen(name='remember'))
SCREEN_MANAGER.add_widget(NewUserScreen(name='newUser'))
SCREEN_MANAGER.add_widget(DashboardScreen(name='dashboard'))
