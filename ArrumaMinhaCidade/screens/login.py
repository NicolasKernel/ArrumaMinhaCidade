from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        layout.add_widget(Label(text='Login/Cadastro', font_size=24))
        login_button = Button(text='Ir para Perfil', size_hint=(1, 0.5))
        login_button.bind(on_press=self.go_to_perfil)
        layout.add_widget(login_button)
        self.add_widget(layout)

    def go_to_perfil(self, instance):
        self.manager.current = 'perfil'