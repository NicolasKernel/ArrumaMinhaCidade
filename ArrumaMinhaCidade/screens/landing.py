from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
import os

class LandingScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Main horizontal layout
        main_layout = BoxLayout(orientation='horizontal', padding=10, spacing=10)

        # Vertical layouts for left and right
        left_layout = BoxLayout(orientation='vertical', size_hint_x=0.3, padding=10, spacing=10)
        right_layout = BoxLayout(orientation='vertical', size_hint_x=0.7, padding=10, spacing=10)

        # Add layouts to main layout
        main_layout.add_widget(left_layout)
        main_layout.add_widget(right_layout)

        # Add main layout to screen
        self.add_widget(main_layout)

        # Background for left_layout
        with left_layout.canvas.before:
            Color(0.9, 0.9, 0.9, 1) 
            self.left_rect = Rectangle(size=left_layout.size, pos=left_layout.pos)
        left_layout.bind(size=self._update_left_rect, pos=self._update_left_rect)

        # Background for right_layout
        with right_layout.canvas.before:
            Color(1, 1, 1, 1) 
            self.right_rect = Rectangle(size=right_layout.size, pos=right_layout.pos)
        right_layout.bind(size=self._update_right_rect, pos=self._update_right_rect)

        # ==================== Left Layout ====================
        
        title = Label(
            text='Arruma Minha Cidade',
            font_size=24,
            size_hint=(1, 0.2),
            color=(0, 0, 0, 1),
            font_name='Roboto'
        )
        left_layout.add_widget(title)

        logo = Image(
            source=os.path.join('images', 'logo.png'),
            size_hint=(1, None),
            height=300,
            fit_mode='contain'
        )
        left_layout.add_widget(logo)

        buttons = [
            ('Ir para Perfil', self.go_to_perfil),
            ('Ir para Blog', self.go_to_blog),
            ('Ir para Lista de Serviços', self.go_to_services),
            ('Ir para Notificações', self.go_to_notifs)
        ]
        for text, callback in buttons:
            btn = Button(
                text=text,
                size_hint=(1, 0.2),
                background_color=(0.1, 0.7, 0.3, 1),
                color=(1, 1, 1, 1)
            )
            btn.bind(on_press=callback)
            left_layout.add_widget(btn)

        # ==================== Right Layout: Top Bar ====================

        top_bar = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=80,
            padding=10,
            spacing=10
        )
        # Add background to top_bar for debugging
        with top_bar.canvas.before:
            Color(0.8, 0.8, 0.8, 1) 
            self.top_bar_rect = Rectangle(size=top_bar.size, pos=top_bar.pos)
        top_bar.bind(size=self._update_top_bar_rect, pos=self._update_top_bar_rect)

        # Spacer to push content to the right
        top_bar.add_widget(Widget(size_hint_x=1))

        # Profile label
        user_label = Label(
            text='Olá, Usuário!',
            font_size=20,
            color=(0, 0, 0, 1),
            size_hint=(None, None),
            size=(150, 60),
            halign='right',
            valign='middle'
        )
        user_label.bind(size=user_label.setter('text_size'))
        top_bar.add_widget(user_label)

        # Profile picture
        try:
            profile_pic = Image(
                source=os.path.join('images', 'logo.png'),
                size_hint=(None, None),
                size=(60, 60),
                fit_mode='contain'  
            )
        except Exception as e:
            print(f"Error loading profile picture: {e}")
            profile_pic = Label(text='[Image Missing]', size_hint=(None, None), size=(60, 60))
        top_bar.add_widget(profile_pic)

        # Add top_bar to right_layout
        right_layout.add_widget(top_bar)

    # ==================== Update Methods ====================

    def _update_left_rect(self, instance, value):
        self.left_rect.pos = instance.pos
        self.left_rect.size = instance.size

    def _update_right_rect(self, instance, value):
        self.right_rect.pos = instance.pos
        self.right_rect.size = instance.size

    def _update_top_bar_rect(self, instance, value):
        self.top_bar_rect.pos = instance.pos
        self.top_bar_rect.size = instance.size

    # ==================== Navigation Methods ====================
    def go_to_perfil(self, instance):
        if 'perfil' in self.manager.screen_names:
            self.manager.current = 'perfil'
        else:
            print("Error: 'perfil' screen not found")

    def go_to_blog(self, instance):
        if 'blog' in self.manager.screen_names:
            self.manager.current = 'blog'
        else:
            print("Error: 'blog' screen not found")

    def go_to_services(self, instance):
        if 'services' in self.manager.screen_names:
            self.manager.current = 'services'
        else:
            print("Error: 'services' screen not found")

    def go_to_notifs(self, instance):
        if 'notifications' in self.manager.screen_names:
            self.manager.current = 'notifications'
        else:
            print("Error: 'notifications' screen not found")

    def go_to_login(self, instance):
        if 'login' in self.manager.screen_names:
            self.manager.current = 'login'
        else:
            print("Error: 'login' screen not found")
