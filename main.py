from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
from kivy.config import Config
from screens.login import LoginScreen
from screens.cadastro import CadastroScreen
from screens.notifs import NotifsScreen
from screens.perfil import PerfilScreen
from screens.landing import LandingScreen
from screens.blog import BlogScreen
from screens.admin import AdminScreen
from screens.service_update import ServiceUpdateScreen
from screens.services import ServicesScreen

Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
Window.clearcolor = (1, 1, 1, 1)
Window.maximize()

class ScreenManagement(ScreenManager):
    pass

class MainApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.usuario_logado = None  # Inicializa o atributo

    def build(self):
        sm = ScreenManagement()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(CadastroScreen(name='cadastro'))
        sm.add_widget(NotifsScreen(name='notifications'))
        sm.add_widget(PerfilScreen(name='perfil'))
        sm.add_widget(LandingScreen(name='landing'))
        sm.add_widget(ServiceUpdateScreen(name='service_update'))
        sm.add_widget(BlogScreen(name='blog'))
        sm.add_widget(ServicesScreen(name='services'))
        sm.add_widget(AdminScreen(name='admin'))
        return sm

if __name__ == '__main__':
    MainApp().run()