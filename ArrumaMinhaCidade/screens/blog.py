from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

class BlogScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        layout.add_widget(Label(text='Blog', font_size=24))
        blog_button = Button(text='Ir para Post', size_hint=(1, 0.5))
        blog_button.bind(on_press=self.go_to_post)
        layout.add_widget(blog_button)
        self.add_widget(layout)

    def go_to_post(self, instance):
        self.manager.current = 'post'