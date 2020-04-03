from kivy.app import App
import helpers as h
import cache as c
from kivy.core.window import Window, Animation
from kivy.graphics.context_instructions import Color
from kivy.properties import NumericProperty, ColorProperty
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.textinput import TextInput
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

SCREEN_MANAGER = ScreenManager()


class instagramManagerApp(App):
    def build(self):
        username = ''
        password = ''
        try:
            username = c.cache['username']
            password = c.cache['password']
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

    def continue_remember(self):
        SCREEN_MANAGER.current = 'dashboard'

    def switch_account(self, str):
        if str == 'press':
            self.ids.switch_acc.color = (0, 0, 0, .7)
        else:
            SCREEN_MANAGER.current = 'newUser'


class NewUserScreen(Screen):
    def logIn(self):
        username = self.ids.username.text
        password = self.ids.password.text
        if len(username) < 2 or len(password) < 2:
            self.ids.error_info.text = 'Please enter a valid log in'
        elif h.new_API(username, password) == 'error':
            self.ids.error_info.text = 'Invalid Log In'
        else:
            c.cache_log_in(username, password)
            SCREEN_MANAGER.current = 'dashboard'


class DashboardScreen(Screen):

    def settings(self):
        SCREEN_MANAGER.current = 'settings'

    def refresh(self):
        self.ids.refresh.y = Window.height
#        self.ids.profile_photo.source =
        self.ids.user_label.text = "@" + c.retrieve_log_in('username')
        self.ids.followers.text = "-"
        self.ids.following.text = "-"
        self.ids.ratio.text = "-"
        self.ids.dfmb.text = "-"
        self.ids.avg_likes.text = "-"
        self.ids.engagement.text = "-"
        followers = h.getFollowers()
        following = h.getFollowing()
        ratio = followers / following
        dfmb = h.getDFMB()
        avglikes = h.getAverageLikes()
        engagemnet = avglikes / followers
        self.ids.followers.text = str(followers)
        self.ids.following.text = str(following)
        self.ids.ratio.text = "%.2f" % round(ratio, 2)
        self.ids.dfmb.text = str(dfmb)
        self.ids.avg_likes.text = str(avglikes)
        self.ids.engagement.text = "%.2f" % round(engagemnet, 2)
        self.ids.refresh.y = Window.height * 0.9 - 15


class SettingsScreen(Screen):
    def tenplus(self):
        self.ids.tenplus.background_normal = 'images/settingbackgrounds/10+_select.png'
        self.ids.thirtyplus.background_normal = 'images/settingbackgrounds/30+.png'
        self.ids.fiftyplus.background_normal = 'images/settingbackgrounds/50+.png'
        self.ids.hundredplus.background_normal = 'images/settingbackgrounds/100+.png'

    def thirtyplus(self):
        self.ids.tenplus.background_normal = 'images/settingbackgrounds/10+.png'
        self.ids.thirtyplus.background_normal = 'images/settingbackgrounds/30+_select.png'
        self.ids.fiftyplus.background_normal = 'images/settingbackgrounds/50+.png'
        self.ids.hundredplus.background_normal = 'images/settingbackgrounds/100+.png'

    def fiftyplus(self):
        self.ids.tenplus.background_normal = 'images/settingbackgrounds/10+.png'
        self.ids.thirtyplus.background_normal = 'images/settingbackgrounds/30+.png'
        self.ids.fiftyplus.background_normal = 'images/settingbackgrounds/50+_select.png'
        self.ids.hundredplus.background_normal = 'images/settingbackgrounds/100+.png'

    def hundredplus(self):
        self.ids.tenplus.background_normal = 'images/settingbackgrounds/10+.png'
        self.ids.thirtyplus.background_normal = 'images/settingbackgrounds/30+.png'
        self.ids.fiftyplus.background_normal = 'images/settingbackgrounds/50+.png'
        self.ids.hundredplus.background_normal = 'images/settingbackgrounds/100+_select.png'

    def manual(self, type):
        if type == 'crawl':
            self.ids.crawlmanual.background_normal = 'images/settingbackgrounds/manual_select.png'
            self.ids.crawlautomatic.background_normal = 'images/settingbackgrounds/automatic.png'
        else:
            self.ids.purgemanual.background_normal = 'images/settingbackgrounds/manual_select.png'
            self.ids.purgeautomatic.background_normal = 'images/settingbackgrounds/automatic.png'

    def automatic(self, type):
        if type == 'crawl':
            self.ids.crawlmanual.background_normal = 'images/settingbackgrounds/manual.png'
            self.ids.crawlautomatic.background_normal = 'images/settingbackgrounds/automatic_select.png'
        else:
            self.ids.purgemanual.background_normal = 'images/settingbackgrounds/manual.png'
            self.ids.purgeautomatic.background_normal = 'images/settingbackgrounds/automatic_select.png'

    def verylow(self):
        if self.ids.verylow.background_normal == 'images/settingbackgrounds/verylow.png':
            self.ids.verylow.background_normal = 'images/settingbackgrounds/verylow_select.png'
        else:
            self.ids.verylow.background_normal = 'images/settingbackgrounds/verylow.png'

    def low(self):
        if self.ids.low.background_normal == 'images/settingbackgrounds/low.png':
            self.ids.low.background_normal = 'images/settingbackgrounds/low_select.png'
        else:
            self.ids.low.background_normal = 'images/settingbackgrounds/low.png'

    def high(self):
        if self.ids.high.background_normal == 'images/settingbackgrounds/high.png':
            self.ids.high.background_normal = 'images/settingbackgrounds/high_select.png'
        else:
            self.ids.high.background_normal = 'images/settingbackgrounds/high.png'

    def veryhigh(self):
        if self.ids.veryhigh.background_normal == 'images/settingbackgrounds/veryhigh.png':
            self.ids.veryhigh.background_normal = 'images/settingbackgrounds/veryhigh_select.png'
        else:
            self.ids.veryhigh.background_normal = 'images/settingbackgrounds/veryhigh.png'

    def fivedays(self):
        self.ids.fivedays.background_normal = 'images/settingbackgrounds/5days_select.png'
        self.ids.tendays.background_normal = 'images/settingbackgrounds/10days.png'
        self.ids.fifteendays.background_normal = 'images/settingbackgrounds/15days.png'

    def tendays(self):
        self.ids.fivedays.background_normal = 'images/settingbackgrounds/5days.png'
        self.ids.tendays.background_normal = 'images/settingbackgrounds/10days_select.png'
        self.ids.fifteendays.background_normal = 'images/settingbackgrounds/15days.png'

    def fifteendays(self):
        self.ids.fivedays.background_normal = 'images/settingbackgrounds/5days.png'
        self.ids.tendays.background_normal = 'images/settingbackgrounds/10days.png'
        self.ids.fifteendays.background_normal = 'images/settingbackgrounds/15days_select.png'

    def slow(self):
        self.ids.slow.background_normal = 'images/settingbackgrounds/slow_select.png'
        self.ids.med.background_normal = 'images/settingbackgrounds/med.png'
        self.ids.fast.background_normal = 'images/settingbackgrounds/fast.png'

    def med(self):
        self.ids.slow.background_normal = 'images/settingbackgrounds/slow.png'
        self.ids.med.background_normal = 'images/settingbackgrounds/med_select.png'
        self.ids.fast.background_normal = 'images/settingbackgrounds/fast.png'

    def fast(self):
        self.ids.slow.background_normal = 'images/settingbackgrounds/slow.png'
        self.ids.med.background_normal = 'images/settingbackgrounds/med.png'
        self.ids.fast.background_normal = 'images/settingbackgrounds/fast_select.png'

    def hundred(self):
        self.ids.hundred.background_normal = 'images/settingbackgrounds/100_select.png'
        self.ids.hundredfifty.background_normal = 'images/settingbackgrounds/150.png'
        self.ids.twohundred.background_normal = 'images/settingbackgrounds/200.png'

    def hundredfifty(self):
        self.ids.hundred.background_normal = 'images/settingbackgrounds/100.png'
        self.ids.hundredfifty.background_normal = 'images/settingbackgrounds/150_select.png'
        self.ids.twohundred.background_normal = 'images/settingbackgrounds/200.png'

    def twohundred(self):
        self.ids.hundred.background_normal = 'images/settingbackgrounds/100.png'
        self.ids.hundredfifty.background_normal = 'images/settingbackgrounds/150.png'
        self.ids.twohundred.background_normal = 'images/settingbackgrounds/200_select.png'


Builder.load_file('screens/login.kv')
Builder.load_file('screens/dashboard.kv')
Builder.load_file('screens/settings.kv')
SCREEN_MANAGER.add_widget(SettingsScreen(name='settings'))
SCREEN_MANAGER.add_widget(RememberScreen(name='remember'))
SCREEN_MANAGER.add_widget(NewUserScreen(name='newUser'))
SCREEN_MANAGER.add_widget(DashboardScreen(name='dashboard'))
