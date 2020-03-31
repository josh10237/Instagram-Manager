from kivy.app import App
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

SCREEN_MANAGER = ScreenManager()

class instagramManager(App):
    def build(self):

        SCREEN_MANAGER.current = 'remember'
        return SCREEN_MANAGER


Window.clearcolor = (1, 1, 1, 1)


class RememberScreen(Screen):
    global counter
    counter = 0

    def method(self, num):
        global counter
        counter += num
        self.ids.info_button.text = "Count: " + str(counter)


Builder.load_file('screens/login.kv')
SCREEN_MANAGER.add_widget(RememberScreen(name='remember'))