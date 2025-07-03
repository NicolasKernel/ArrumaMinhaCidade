from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, NoTransition, SlideTransition
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.switch import Switch
import os
from kivy.app import App

class PerfilScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Layout principal horizontal
        main_layout = BoxLayout(orientation='horizontal', spacing=10)

        # Barra lateral esquerda para navegação
        left_layout = BoxLayout(orientation='vertical', size_hint_x=0.1, padding=10, spacing=10)
        # Lado direito: apenas uma coluna para exibir informações
        right_layout = BoxLayout(orientation='vertical', padding=30, spacing=15, size_hint_x=0.9)

        main_layout.add_widget(left_layout)
        main_layout.add_widget(right_layout)
        self.add_widget(main_layout)

        # Fundo para o left_layout
        with left_layout.canvas.before:
            Color(0.9, 0.9, 0.9, 1)
            self.left_rect = Rectangle(size=left_layout.size, pos=left_layout.pos)
        left_layout.bind(size=self._update_left_rect, pos=self._update_left_rect)

        # Fundo para o right_layout
        with right_layout.canvas.before:
            Color(1, 1, 1, 1)
            self.right_rect = Rectangle(size=right_layout.size, pos=right_layout.pos)
        right_layout.bind(size=self._update_right_rect, pos=self._update_right_rect)

        # ==================== Barra Lateral Esquerda ====================
        title = Label(
            text='Perfil',
            font_size=24,
            size_hint=(1, 0.2),
            color=(0, 0, 0, 1),
            font_name='Roboto'
        )
        left_layout.add_widget(title)

        logo = Image(
            source=os.path.join('resources', 'logo.png'),
            size_hint=(1, None),
            height=150,
            fit_mode='contain'
        )
        left_layout.add_widget(logo)
        
        left_layout.add_widget(Widget())
        
        # Botões para outras configurações
        buttons = [
            ('Ir para Landing', self.go_to_landing),
            ('Ir para lista de Serviços', self.go_to_blog),
            ('Ir para Notificações', self.go_to_notifs),
            ('Solicitar Serviço', self.go_to_services),
            ('Sair', self.go_to_login)
        ]
        for text, callback in buttons:
            btn = Button(
                text=text,
                size_hint=(1, 0.5),
                background_color=(0.812, 0.812, 0.812, 1),
                color=(1, 1, 1, 1)
            )
            btn.bind(on_press=callback)
            left_layout.add_widget(btn)

        # ==================== Conteúdo da Direita: Informações do Usuário ====================
        self.info_layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        right_layout.add_widget(self.info_layout)

    def on_pre_enter(self, *args):
        self.info_layout.clear_widgets()
        app = App.get_running_app()
        usuario = getattr(app, "usuario_logado", None)
        if usuario:
            self.info_layout.add_widget(Label(
                text="[b]Informações do Usuário:[/b]",
                font_size=20,
                color=(0, 0, 0, 1),
                markup=True,
                size_hint_y=None,
                height=40
            ))
            for key, value in usuario.items():
                self.info_layout.add_widget(Label(
                    text=f"[b]{key}:[/b] {value}",
                    font_size=16,
                    color=(0.1, 0.1, 0.1, 1),
                    markup=True,
                    size_hint_y=None,
                    height=30
                ))
        else:
            self.info_layout.add_widget(Label(
                text="Nenhum usuário logado.",
                font_size=18,
                color=(1, 0, 0, 1),
                size_hint_y=None,
                height=40
            ))

    # ==================== Métodos de Atualização ====================
    def _update_left_rect(self, instance, value):
        self.left_rect.pos = instance.pos
        self.left_rect.size = instance.size

    def _update_right_rect(self, instance, value):
        self.right_rect.pos = instance.pos
        self.right_rect.size = instance.size

    # ==================== Métodos de Navegação ====================
    def go_to_landing(self, instance):
        if 'landing' in self.manager.screen_names:
            self.manager.current = 'landing'
        else:
            print("Erro: tela 'landing' não encontrada")
    
    def go_to_perfil(self, instance):
        popup = Popup(
            title='Aviso',
            content=Label(text='Você já está no seu perfil.'),
            size_hint=(None, None),
            size=(350, 180)
        )
        popup.open()

    def go_to_blog(self, instance):
        if 'blog' in self.manager.screen_names:
            self.manager.current = 'blog'
        else:
            print("Erro: tela 'blog' não encontrada")

    def go_to_services(self, instance):
        if 'services' in self.manager.screen_names:
            self.manager.current = 'services'
        else:
            print("Erro: tela 'services' não encontrada")

    def go_to_notifs(self, instance):
        if 'notifications' in self.manager.screen_names:
            self.manager.current = 'notifications'
        else:
            print("Erro: tela 'notifications' não encontrada")

    def go_to_login(self, instance):
        if 'login' in self.manager.screen_names:
            self.manager.current = 'login'
        else:
            print("Erro: tela 'login' não encontrada")
