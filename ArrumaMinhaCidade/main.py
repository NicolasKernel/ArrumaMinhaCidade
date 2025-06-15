from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from screens.login import LoginScreen
from screens.perfil import PerfilScreen
from screens.landing import LandingScreen
from screens.blog import BlogScreen
from controllers.navigation import NavigationController
from kivy.core.window import Window

Window.clearcolor = (1, 1, 1, 1)
Window.maximize()

class ScreenManagement(ScreenManager):
    pass

class MainApp(App):
    def build(self):
        sm = ScreenManagement()
        nav = NavigationController(sm)
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(PerfilScreen(name='perfil'))
        sm.add_widget(LandingScreen(name='landing'))
        sm.add_widget(BlogScreen(name='blog'))
        return sm

if __name__ == '__main__':
    MainApp().run()
