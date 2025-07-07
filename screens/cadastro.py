from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.graphics import Color, Rectangle
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
import os
import sys
import json
from models.user import User
from utils.validation import validate_cep, validate_email, validate_cpf

def resource_path(relative_path):
    """Retorna o caminho absoluto para uso com PyInstaller."""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

class CadastroScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.users_json = "usuarios.json"

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
            source=resource_path(os.path.join('resources', 'logo.png')),
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
            text='Cadastro',
            font_size=30,
            color=(0.094, 0.208, 0.349, 0.839)
        ))

        # Campo Nome
        main_layout.add_widget(Label(text='Nome:', font_size=13, color=(0.094, 0.208, 0.349, 0.839)))
        self.nome_input = TextInput(multiline=False, size_hint=(1, None), height=40)
        main_layout.add_widget(self.nome_input)

        # Espaço extra antes do bloco Telefone/CPF
        main_layout.add_widget(Widget(size_hint_y=None, height=20))

        # Layout horizontal para Telefone e CPF
        telefone_cpf_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint=(1, None), height=40)

        # Campo Telefone
        telefone_layout = BoxLayout(orientation='vertical', size_hint=(1, 3))
        telefone_layout.add_widget(Label(text='Telefone:', font_size=13, color=(0.094, 0.208, 0.349, 0.839)))
        self.telefone_input = TextInput(multiline=False, size_hint=(1, None), height=40)
        telefone_layout.add_widget(self.telefone_input)
        telefone_cpf_layout.add_widget(telefone_layout)

        # Campo CPF
        cpf_layout = BoxLayout(orientation='vertical', size_hint=(1, 3))
        cpf_layout.add_widget(Label(text='CPF:', font_size=13, color=(0.094, 0.208, 0.349, 0.839)))
        self.cpf_input = TextInput(multiline=False, size_hint=(1, None), height=40)
        cpf_layout.add_widget(self.cpf_input)
        telefone_cpf_layout.add_widget(cpf_layout)

        main_layout.add_widget(telefone_cpf_layout)

        # Campo Senha
        main_layout.add_widget(Label(text='Senha:', font_size=13, color=(0.094, 0.208, 0.349, 0.839)))
        self.senha_input = TextInput(multiline=False, password=True, size_hint=(1, None), height=40)
        main_layout.add_widget(self.senha_input)

        # Campo CEP
        main_layout.add_widget(Label(text='CEP:', font_size=13, color=(0.094, 0.208, 0.349, 0.839)))
        self.cep_input = TextInput(multiline=False, size_hint=(1, None), height=40)
        main_layout.add_widget(self.cep_input)

        # Campo Bairro
        main_layout.add_widget(Label(text='Bairro:', font_size=13, color=(0.094, 0.208, 0.349, 0.839)))
        self.bairro_input = TextInput(multiline=False, size_hint=(1, None), height=40)
        main_layout.add_widget(self.bairro_input)

        # Botão de Enviar
        submit_button = Button(
            text='Enviar',
            size_hint_x=1,
            height=45,
            background_color=(0.855, 0.855, 0.878, 0.831)
        )
        submit_button.bind(on_press=self.submit_action)
        main_layout.add_widget(submit_button)

        # Botão de Voltar
        back_button = Button(
            text='Voltar',
            size_hint_x=1,
            height=45,
            background_color=(0.855, 0.855, 0.878, 0.831)
        )
        back_button.bind(on_press=self.goto_login)
        main_layout.add_widget(back_button)

        self.info_label = Label(text='', font_size=13, color=(0, 0.5, 0, 1))
        main_layout.add_widget(self.info_label)

    def _update_bg_rect(self, instance, value):
        self.bg_rect.pos = instance.pos
        self.bg_rect.size = instance.size

    def submit_action(self, instance):
        # Validação de CPF antes de cadastrar
        if not validate_cpf(self.cpf_input.text):
            popup = Popup(
                title='CPF inválido',
                content=Label(text='O CPF informado é inválido.'),
                size_hint=(None, None),
                size=(350, 180)
            )
            popup.open()
            return

        # Validação de CEP antes de cadastrar
        if not validate_cep(self.cep_input.text):
            popup = Popup(
                title='CEP inválido',
                content=Label(text='O CEP informado é inválido ou não existe.'),
                size_hint=(None, None),
                size=(350, 180)
            )
            popup.open()
            return

        # Cria o usuário
        user = User(
            username=self.nome_input.text,
            email="",  # Não há campo de email
            telefone=self.telefone_input.text,
            cpf=self.cpf_input.text,
            cep=self.cep_input.text,
            bairro=self.bairro_input.text,
            senha=self.senha_input.text,
            is_admin=False
        )

        # Carrega usuários existentes
        try:
            with open(self.users_json, "r", encoding="utf-8") as f:
                users_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            users_data = []

        # Adiciona novo usuário
        users_data.append({
            "username": user.username,
            "email": user.email,
            "telefone": user.telefone,
            "cpf": user.cpf,
            "cep": user.cep,
            "bairro": user.bairro,
            "senha": user.senha,
            "is_admin": user.is_admin
        })

        # Salva no JSON
        with open(self.users_json, "w", encoding="utf-8") as f:
            json.dump(users_data, f, ensure_ascii=False, indent=4)

        # Mostra popup de confirmação de cadastro
        popup = Popup(
            title='Cadastro enviado',
            content=Label(
                text=(
                    f"Nome: {self.nome_input.text}\n"
                    f"Telefone: {self.telefone_input.text}\n"
                    f"CPF: {self.cpf_input.text}\n"
                    f"CEP: {self.cep_input.text}\n"
                    f"Bairro: {self.bairro_input.text}\n"
                    "Cadastro enviado!"
                )
            ),
            size_hint=(None, None),
            size=(400, 250)
        )
        popup.open()

    def goto_login(self, instance):
        if self.manager and 'login' in self.manager.screen_names:
            self.manager.current = 'login'