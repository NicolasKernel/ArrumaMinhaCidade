from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.uix.spinner import Spinner
from kivy.graphics import Color, Rectangle
from kivy.uix.popup import Popup
from kivy.app import App
import os
import sys
import json
from datetime import datetime
import random
import string
import shutil
from tkinter import filedialog, Tk

def resource_path(relative_path):
    """Retorna o caminho absoluto para uso com PyInstaller."""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

class ServicesScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.json_file = "services_updates.json"  # Same JSON file used by BlogScreen and ServiceUpdateScreen
        self.service_types = [
            'Infraestrutura e Mobilidade',
            'Saneamento Básico',
            'Limpeza e Manutenção Urbana',
            'Planejamento Urbano'
        ]

        # Layout principal horizontal
        main_layout = BoxLayout(orientation='horizontal', spacing=10)

        # Barra lateral esquerda para navegação
        left_layout = BoxLayout(orientation='vertical', size_hint_x=0.1, padding=10, spacing=10)
        # Área da direita: GridLayout com 2 linhas (área de usuário + formulário)
        right_layout = GridLayout(cols=1, rows=2, size_hint_x=0.9, padding=10, spacing=10)

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
            text='Novo Serviço',
            font_size=22,
            size_hint=(1, None),
            height=60,
            color=(0, 0, 0, 1),
            font_name='Roboto'
        )
        left_layout.add_widget(title)

        logo = Image(
            source=resource_path(os.path.join('resources', 'logo.png')),
            size_hint=(1, None),
            height=120,
            fit_mode='contain'
        )
        left_layout.add_widget(logo)

        left_layout.add_widget(Widget())

        buttons = [
            ('Ir para lista de Serviços', self.go_to_landing),
            ('Ir para lista de Serviços', self.go_to_blog),
            ('Ir para Notificações', self.go_to_notifs),
            ('Solicitar Serviço', self.go_to_services),
            ('Sair', self.go_to_login)
        ]
        for text, callback in buttons:
            btn = Button(
                text=text,
                size_hint=(1, 0.5),
                background_color=(0.1, 0.7, 0.3, 1),
                color=(1, 1, 1, 1)
            )
            btn.bind(on_press=callback)
            left_layout.add_widget(btn)

        # ==================== Área de Usuário Direita (topo) ====================
        top_bar = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=80,
            padding=10,
            spacing=10
        )
        top_bar.add_widget(Widget(size_hint_x=1))

        self.user_label = Label(
            text='Olá, Usuário!',
            font_size=20,
            color=(0, 0, 0, 1),
            size_hint=(None, None),
            size=(150, 60),
            halign='right',
            valign='middle'
        )
        self.user_label.bind(size=self.user_label.setter('text_size'))
        top_bar.add_widget(self.user_label)

        profile_pic = Image(
            source=resource_path(os.path.join('resources', 'logo.png')),
            size_hint=(None, None),
            size=(60, 60),
            fit_mode='contain'
        )
        profile_pic.bind(on_touch_down=self._on_profile_pic_touch)
        top_bar.add_widget(profile_pic)
        self.profile_pic = profile_pic

        right_layout.add_widget(top_bar)

        # ==================== Formulário de Criação de Serviço ====================
        right_content = BoxLayout(orientation='vertical', spacing=10, padding=[10, 5, 10, 10])

        # Título da tela
        title = Label(
            text='Criar Novo Serviço',
            font_size=24,
            size_hint_y=None,
            height=50,
            color=(0, 0, 0, 1),
            font_name='Roboto',
            halign='center',
            text_size=(None, None)
        )
        right_content.add_widget(title)

        # Formulário
        form_layout = BoxLayout(orientation='vertical', spacing=10, padding=20)

        # Campo Nome do Serviço
        form_layout.add_widget(Label(
            text='Nome do Serviço:',
            font_size=14,
            color=(0, 0, 0, 1),
            size_hint_y=None,
            height=30
        ))
        self.service_name_input = TextInput(
            hint_text='Digite o nome do serviço',
            multiline=False,
            size_hint_y=None,
            height=40
        )
        form_layout.add_widget(self.service_name_input)

        # Campo Descrição
        form_layout.add_widget(Label(
            text='Descrição do Serviço:',
            font_size=14,
            color=(0, 0, 0, 1),
            size_hint_y=None,
            height=30
        ))
        self.description_input = TextInput(
            hint_text='Digite a descrição do serviço',
            multiline=True,
            size_hint_y=None,
            height=80
        )
        form_layout.add_widget(self.description_input)

        # Campo Endereço
        form_layout.add_widget(Label(
            text='Endereço:',
            font_size=14,
            color=(0, 0, 0, 1),
            size_hint_y=None,
            height=30
        ))
        self.address_input = TextInput(
            hint_text='Digite o endereço (ex: Rua Exemplo)',
            multiline=False,
            size_hint_y=None,
            height=40
        )
        form_layout.add_widget(self.address_input)

        # Campo Número do Endereço
        form_layout.add_widget(Label(
            text='Número do Endereço:',
            font_size=14,
            color=(0, 0, 0, 1),
            size_hint_y=None,
            height=30
        ))
        self.number_input = TextInput(
            hint_text='Digite o número',
            multiline=False,
            size_hint_y=None,
            height=40
        )
        form_layout.add_widget(self.number_input)

        # Campo Bairro
        form_layout.add_widget(Label(
            text='Bairro:',
            font_size=14,
            color=(0, 0, 0, 1),
            size_hint_y=None,
            height=30
        ))
        self.bairro_input = TextInput(
            hint_text='Digite o bairro',
            multiline=False,
            size_hint_y=None,
            height=40
        )
        form_layout.add_widget(self.bairro_input)

        # Campo Tipo de Serviço
        form_layout.add_widget(Label(
            text='Tipo de Serviço:',
            font_size=14,
            color=(0, 0, 0, 1),
            size_hint_y=None,
            height=30
        ))
        self.service_type_spinner = Spinner(
            text='Selecione o tipo de serviço',
            values=self.service_types,
            size_hint_y=None,
            height=40
        )
        form_layout.add_widget(self.service_type_spinner)

        # Botão para carregar imagem
        form_layout.add_widget(Label(
            text='Imagem do Serviço:',
            font_size=14,
            color=(0, 0, 0, 1),
            size_hint_y=None,
            height=30
        ))
        self.image_button = Button(
            text='Selecionar Imagem',
            size_hint_y=None,
            height=40,
            background_color=(0.2, 0.6, 1, 1),
            color=(1, 1, 1, 1)
        )
        self.image_button.bind(on_press=self.show_file_chooser)
        form_layout.add_widget(self.image_button)

        # Campo para digitar o caminho da imagem
        self.image_input = TextInput(
            hint_text='Digite o caminho da imagem (ex: images/servico.png)',
            multiline=False,
            size_hint_y=None,
            height=40
        )
        form_layout.add_widget(self.image_input)

        # Botão para criar serviço
        create_button = Button(
            text='Criar Serviço',
            size_hint=(1, None),
            height=50,
            background_color=(0.1, 0.7, 0.3, 1),
            color=(1, 1, 1, 1)
        )
        create_button.bind(on_press=self.create_service)
        form_layout.add_widget(create_button)

        right_content.add_widget(form_layout)
        right_layout.add_widget(right_content)

    def _update_left_rect(self, instance, value):
        self.left_rect.pos = instance.pos
        self.left_rect.size = instance.size

    def _update_right_rect(self, instance, value):
        self.right_rect.pos = instance.pos
        self.right_rect.size = instance.size

    def generate_unique_id(self):
        """Gera um ID único com 3 números e 3 letras."""
        try:
            with open(self.json_file, 'r') as f:
                all_updates = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            all_updates = {}

        existing_ids = []
        for service_data in all_updates.values():
            if isinstance(service_data, dict) and 'id' in service_data:
                existing_ids.append(service_data['id'])

        while True:
            numbers = ''.join(random.choices(string.digits, k=3))
            letters = ''.join(random.choices(string.ascii_uppercase, k=3))
            new_id = numbers + letters
            if new_id not in existing_ids:
                return new_id

    def show_file_chooser(self, instance):
        """Abre um seletor de arquivos usando tkinter."""
        try:
            # Inicializa o Tkinter e esconde a janela principal
            root = Tk()
            root.withdraw()
            
            # Abre o seletor de arquivos
            file_path = filedialog.askopenfilename(
                filetypes=[("Imagens", "*.png *.jpg *.jpeg")]
            )
            
            # Destrói a janela do Tkinter
            root.destroy()
            
            if file_path:
                self.image_input.text = file_path
            else:
                popup = Popup(
                    title='Aviso',
                    content=Label(text='Nenhuma imagem selecionada!'),
                    size_hint=(None, None),
                    size=(400, 200)
                )
                popup.open()
        except Exception as e:
            popup = Popup(
                title='Erro',
                content=Label(text=f'Erro ao selecionar imagem: {str(e)}'),
                size_hint=(None, None),
                size=(400, 200)
            )
            popup.open()

    def create_service(self, instance):
        """Cria um novo serviço e salva no JSON."""
        service_id = self.generate_unique_id()  # Gera ID automaticamente
        service_name = self.service_name_input.text.strip()
        description = self.description_input.text.strip()
        address = self.address_input.text.strip()
        number = self.number_input.text.strip()
        bairro = self.bairro_input.text.strip()
        image_path = self.image_input.text.strip()
        service_type = self.service_type_spinner.text.strip()

        if not all([service_name, description, address, bairro, service_type != 'Selecione o tipo de serviço']):
            popup = Popup(
                title='Erro',
                content=Label(text='Por favor, preencha todos os campos obrigatórios, incluindo o tipo de serviço!'),
                size_hint=(None, None),
                size=(400, 200)
            )
            popup.open()
            return

        # Formata o endereço completo
        full_address = f"{address}, {number}, {bairro}"

        # Obtém a data atual
        current_date = datetime.now().strftime('%d/%m/%Y')

        if image_path and os.path.isfile(image_path):
            images_dir = os.path.join(os.path.abspath("."), 'images')
            if not os.path.exists(images_dir):
                os.makedirs(images_dir)
            img_name = f"{service_id}_{os.path.basename(image_path)}"
            dest_path = os.path.join(images_dir, img_name)
            try:
                shutil.copy(image_path, dest_path)
                image_path = os.path.join('images', img_name)
            except Exception as e:
                popup = Popup(
                    title='Erro',
                    content=Label(text=f'Erro ao copiar imagem: {e}'),
                    size_hint=(None, None),
                    size=(400, 200)
                )
                popup.open()
                return
        else:
            image_path = os.path.join('images', 'default.png')

        # Cria o novo serviço
        new_service = {
            'id': service_id,
            'title': service_name,
            'description': description,
            'date': current_date,
            'address': full_address,
            'image': image_path,
            'status': 'Em análise',
            'type': service_type,
            'last_update': f"{current_date} 00:00"
        }

        # Salva no JSON com todas as informações
        try:
            with open(self.json_file, 'r') as f:
                all_updates = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            all_updates = {}

        all_updates[service_name] = new_service  # Salva o serviço completo

        with open(self.json_file, 'w') as f:
            json.dump(all_updates, f, indent=4)

        # Adiciona o serviço à lista de atualizações na BlogScreen
        if 'blog' in self.manager.screen_names:
            blog_screen = self.manager.get_screen('blog')
            blog_screen.add_service(new_service)  # Usa add_service para garantir que o serviço apareça no topo

        # Mostra popup de sucesso
        popup = Popup(
            title='Sucesso',
            content=Label(text='Serviço criado com sucesso!'),
            size_hint=(None, None),
            size=(400, 200)
        )
        popup.open()

        # Limpa os campos
        self.service_name_input.text = ''
        self.description_input.text = ''
        self.address_input.text = ''
        self.number_input.text = ''
        self.bairro_input.text = ''
        self.image_input.text = ''
        self.service_type_spinner.text = 'Selecione o tipo de serviço'

    def on_pre_enter(self, *args):
        app = App.get_running_app()
        usuario_nome = "Usuário"
        if hasattr(app, "usuario_logado") and app.usuario_logado:
            usuario_nome = app.usuario_logado.get("username", "Usuário")
        self.user_label.text = f'Olá, {usuario_nome}!'
        
    # ==================== Métodos de Navegação ====================
    def go_to_landing(self, instance):
        if 'landing' in self.manager.screen_names:
            self.manager.current = 'landing'
        else:
            print("Erro: tela 'landing' não encontrada")
    
    def go_to_perfil(self, instance):
        if 'perfil' in self.manager.screen_names:
            self.manager.current = 'perfil'
        else:
            print("Erro: tela 'perfil' não encontrada")

    def go_to_blog(self, instance):
        if 'blog' in self.manager.screen_names:
            self.manager.current = 'blog'
        else:
            print("Erro: tela 'blog' não encontrada")

    def go_to_services(self, instance):
            popup = Popup(
                title='Aviso',
                content=Label(text='Você já está na solicitação de serviços.'),
                size_hint=(None, None),
                size=(350, 180)
            )
            popup.open()

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

    def _on_profile_pic_touch(self, instance, touch):
        if instance.collide_point(*touch.pos):
            if 'perfil' in self.manager.screen_names:
                self.manager.current = 'perfil'
            else:
                print("Erro: tela 'perfil' não encontrada")
