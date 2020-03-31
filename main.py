from kivy.app import App
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

SCREEN_MANAGER = ScreenManager()
#test

class instagramManager(App):
    def build(self):
        SCREEN_MANAGER.current = 'main'
        return SCREEN_MANAGER


Window.clearcolor = (1, 1, 1, 1)


class MainScreen(Screen):
    global counter
    counter = 0

    def method(self, num):
        global counter
        counter += num
        self.ids.info_button.text = "Count: " + str(counter)


Builder.load_file('screens/main.kv')
SCREEN_MANAGER.add_widget(MainScreen(name='main'))

if __name__ == "__main__":
    instagramManager().run()