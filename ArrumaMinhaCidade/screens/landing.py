from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle

class LandingScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Cria o layout da direitoa
        rightLayout = BoxLayout(orientation='vertical')
        leftLayout = BoxLayout(orientation='vertical')
        
        
        # Adiciona fundo cinza claro
        with rightLayout.canvas.before:
            Color(0.95, 0.95, 0.95, 1)  # RGBA para cinza claro
            self.rect = Rectangle(size=rightLayout.size, pos=rightLayout.pos)
        rightLayout.bind(size=self._update_rect, pos=self._update_rect)

        # Título
        title = Label(
            text='Bem-vindo à Landing Page',
            font_size=32,
            color=(0, 0.5, 0.8, 1),  # Azul escuro
            size_hint_y=None,
            height=50,
            halign='center'
        )
        rightLayout.add_widget(title)

        # Botão para Perfil
        perfil_button = Button(
            text='Ir para Perfil',
            size_hint=(1, 0.6),
            background_color=(0.1, 0.7, 0.3, 1),  # Verde
            color=(1, 1, 1, 1)  # Texto branco
        )
        perfil_button.bind(on_press=self.go_to_perfil)
        rightLayout.add_widget(perfil_button)

        # Botão para Blog
        blog_button = Button(
            text='Ir para Blog',
            size_hint=(1, 0.6),
            background_color=(0.1, 0.7, 0.3, 1),  # Verde
            color=(1, 1, 1, 1)  # Texto branco
        )
        blog_button.bind(on_press=self.go_to_blog)
        rightLayout.add_widget(blog_button)

        # Botão para Lista de Serviços
        services_button = Button(
            text='Ir para Lista de Serviços',
            size_hint=(1, 0.6),
            background_color=(0.1, 0.7, 0.3, 1),  # Verde
            color=(1, 1, 1, 1)  # Texto branco
        )
        services_button.bind(on_press=self.go_to_services)
        rightLayout.add_widget(services_button)

        # Botão para Post
        notifs_button = Button(
            text='Ir para notificações',
            size_hint=(1, 0.6),
            background_color=(0.1, 0.7, 0.3, 1),  # Verde
            color=(1, 1, 1, 1)  # Texto branco
        )
        notifs_button.bind(on_press=self.go_to_notifs)
        rightLayout.add_widget(notifs_button)

        # Botão para Voltar ao Login
        back_button = Button(
            text='Voltar para Login',
            size_hint=(1, 0.6),
            background_color=(0.7, 0.2, 0.2, 1),  # Vermelho
            color=(1, 1, 1, 1)  # Texto branco
        )
        back_button.bind(on_press=self.go_to_login)
        rightLayout.add_widget(back_button)

        self.add_widget(rightLayout)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def go_to_perfil(self, instance):
        self.manager.current = 'perfil'

    def go_to_blog(self, instance):
        self.manager.current = 'blog'

    def go_to_services(self, instance):
        self.manager.current = 'services'

    def go_to_notifs(self, instance):
        self.manager.current = 'notifications'

    def go_to_login(self, instance):
        self.manager.current = 'login'
