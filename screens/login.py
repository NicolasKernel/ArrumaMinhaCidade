from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.uix.popup import Popup
from kivy.app import App
import os
import json 

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Layout principal vertical centralizado
        main_layout = BoxLayout(orientation='vertical', padding=60, spacing=20)
        self.add_widget(main_layout)

        # Fundo para o layout principal
        with main_layout.canvas.before:
            Color(0.922, 0.933, 0.941, 0.831)
            self.bg_rect = Rectangle(size=main_layout.size, pos=main_layout.pos)
        main_layout.bind(size=self._update_bg_rect, pos=self._update_bg_rect)

        # Logo
        logo = Image(
            source=os.path.join('resources', 'logo.png'),
            size_hint=(1, None),
            height=120,
            fit_mode='contain'
        )
        main_layout.add_widget(logo)

        # Título
        main_layout.add_widget(Label(
            text='Arruma Minha Cidade',
            font_size=28,
            size_hint=(1, None),
            height=60,
            color=(0.094, 0.208, 0.349, 0.839),
            font_name='Roboto'
        ))

        main_layout.add_widget(Label(
            text='Login',
            font_size=30,
            color=(0.094, 0.208, 0.349, 0.839)
        ))

        # Campo CPF
        cpf_layout = BoxLayout(orientation='vertical', spacing=5)
        cpf_layout.add_widget(Label(
            text='CPF:', font_size=13, color=(0.094, 0.208, 0.349, 0.839)
        ))
        self.cpf_input = TextInput(
            multiline=False,
            size_hint=(0.20, None),
            height=30,
            pos_hint={'center_x': 0.5}
        )
        cpf_layout.add_widget(self.cpf_input)
        main_layout.add_widget(cpf_layout)

        # Campo Senha
        senha_layout = BoxLayout(orientation='vertical', spacing=5)
        senha_layout.add_widget(Label(
            text='Senha:', font_size=13, color=(0.094, 0.208, 0.349, 0.839)
        ))
        self.senha_input = TextInput(
            multiline=False,
            password=True,
            size_hint=(0.20, None),
            height=30,
            pos_hint={'center_x': 0.5}
        )
        senha_layout.add_widget(self.senha_input)
        main_layout.add_widget(senha_layout)

        # Espaçador para aumentar a distância entre o campo de senha e os botões
        main_layout.add_widget(Widget(size_hint_y=None, height=30))

        # Botão Entrar
        login_button = Button(
            text='Entrar',
            size_hint=(0.2, None),
            height=50,
            background_color=(0.855, 0.855, 0.878, 0.831),
            pos_hint={'center_x': 0.5}
        )
        login_button.bind(on_press=self.login_action)
        main_layout.add_widget(login_button)

        # Botão Cadastro
        signup_button = Button(
            text='Cadastro',
            size_hint=(0.2, None),
            height=50,
            background_color=(0.855, 0.855, 0.878, 0.831),
            pos_hint={'center_x': 0.5}
        )
        signup_button.bind(on_press=self.signup_action)
        main_layout.add_widget(signup_button)

        self.error_label = Label(text='', font_size=13, color=(1, 0, 0, 1))
        main_layout.add_widget(self.error_label)

        self.users_json = "usuarios.json"

    def _update_bg_rect(self, instance, value):
        self.bg_rect.pos = instance.pos
        self.bg_rect.size = instance.size

    def login_action(self, instance):
        cpf = self.cpf_input.text
        senha = self.senha_input.text

        try:
            with open(self.users_json, "r", encoding="utf-8") as f:
                users_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            users_data = []

        usuario_encontrado = None
        for user in users_data:
            if user.get("cpf") == cpf and user.get("senha") == senha:
                usuario_encontrado = user
                break

        if usuario_encontrado:
            # Garante que os campos existem
            if "seguindo" not in usuario_encontrado:
                usuario_encontrado["seguindo"] = []
            print(f"Usuário {cpf} logado com sucesso!")
            App.get_running_app().usuario_logado = usuario_encontrado
            # Redireciona para tela de admin se for admin, senão para landing
            if usuario_encontrado.get("is_admin", False):
                if self.manager and 'admin' in self.manager.screen_names:
                    self.manager.current = 'admin'
            elif self.manager and 'landing' in self.manager.screen_names:
                self.manager.current = 'landing'
        else:
            popup = Popup(
                title='Erro de Login',
                content=Label(text='CPF ou senha incorretos!'),
                size_hint=(None, None),
                size=(350, 180)
            )
            popup.open()

    def signup_action(self, instance):
        if self.manager and 'cadastro' in self.manager.screen_names:
            self.manager.current = 'cadastro'