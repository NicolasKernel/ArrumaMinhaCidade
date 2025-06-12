from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

class LandingScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        layout.add_widget(Label(text='Landing Page', font_size=24))
        landing_button = Button(text='Voltar para Login', size_hint=(1, 0.5))
        landing_button.bind(on_press=self.go_to_login)
        layout.add_widget(landing_button)
        self.add_widget(layout)

    def go_to_login(self, instance):
        self.manager.current = 'login'