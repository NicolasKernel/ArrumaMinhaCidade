from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle
from kivy.uix.widget import Widget
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
import os
import json
from datetime import datetime

class NotifsScreen(Screen):
    def __init__(self, blog_posts=None, **kwargs):
        super().__init__(**kwargs)
        self.json_file = "services_updates.json"
        self.notif_posts = blog_posts if blog_posts is not None else self.load_json_data()

        # Layout principal horizontal
        main_layout = BoxLayout(orientation='horizontal', spacing=10)

        # Barra lateral esquerda para navegação
        left_layout = BoxLayout(orientation='vertical', size_hint_x=0.1, padding=10, spacing=10)
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

        # ==================== Left Layout: Barra de Navegação ====================
        left_layout.add_widget(Widget(size_hint_y=None, height=20))  # Espaçamento

        logo_image = Image(
            source=os.path.join('resources', 'logo.png'),
            size_hint_y=None,
            height=50
        )
        left_layout.add_widget(logo_image)

        left_layout.add_widget(Widget(size_hint_y=None, height=20))  # Espaçamento

        # Botões de navegação
        nav_buttons_data = [
            ("perfil", "perfil_icon.png", self.go_to_perfil),
            ("notifications", "notifs_icon.png", None),  # Já estamos em notificações
            ("landing", "home_icon.png", self.go_to_landing),
            ("services", "services_icon.png", self.go_to_services),
            ("blog", "blog_icon.png", self.go_to_blog),
            ("logout", "logout_icon.png", self.go_to_login),
        ]

        for name, icon, on_press_callback in nav_buttons_data:
            button_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, spacing=10)
            
            icon_image = Image(source=os.path.join('resources', icon), size_hint_x=None, width=30)
            button_layout.add_widget(icon_image)

            button = Button(
                text=name.capitalize(),
                background_color=(0, 0, 0, 0),  # Transparente
                color=(0, 0, 0, 1),
                size_hint_x=1,
                halign='left',
                valign='middle',
                text_size=(left_layout.width - 60, None)
            )
            if on_press_callback:
                button.bind(on_press=on_press_callback)
            
            button_layout.add_widget(button)
            left_layout.add_widget(button_layout)
            
            left_layout.add_widget(Widget(size_hint_y=None, height=10)) # Espaçamento entre botões

        left_layout.add_widget(Widget())  # Espaçador para empurrar o conteúdo para cima

        # ==================== Right Layout: Top Bar e Conteúdo ====================
        # Top bar (Área de usuário)
        top_bar = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, padding=10, spacing=10)
        with top_bar.canvas.before:
            Color(0.9, 0.9, 0.9, 1)
            self.top_bar_rect = Rectangle(size=top_bar.size, pos=top_bar.pos)
        top_bar.bind(size=self._update_top_bar_rect, pos=self._update_top_bar_rect)

        user_label = Label(text="Olá, Usuário!", color=(0, 0, 0, 1), font_size=18, size_hint_x=0.8)
        top_bar.add_widget(user_label)

        settings_button = Button(
            text="⚙️",
            font_size=24,
            size_hint_x=0.1,
            background_color=(0,0,0,0),
            color=(0,0,0,1)
        )
        top_bar.add_widget(settings_button)

        logout_button_top = Button(
            text="Sair",
            size_hint_x=0.1,
            background_color=(1, 0.2, 0.2, 1),
            on_press=self.go_to_login
        )
        top_bar.add_widget(logout_button_top)
        right_layout.add_widget(top_bar)

        # Área de Conteúdo das Notificações
        self.notifs_content = ScrollView(do_scroll_y=True, size_hint_y=1)
        right_layout.add_widget(self.notifs_content)

        self.notifs_layout = BoxLayout(orientation='vertical', spacing=20, size_hint_y=None, padding=10)
        self.notifs_layout.bind(minimum_height=self.notifs_layout.setter('height'))
        self.notifs_content.add_widget(self.notifs_layout)

        # Atualizar e exibir as notificações
        self.update_notifs()

    def load_json_data(self):
        """Carrega os dados do JSON."""
        try:
            with open(self.json_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def on_pre_enter(self, *args):
        """Recarga os dados do JSON antes de entrar na tela."""
        self.notif_posts = self.load_json_data()
        self.update_notifs()

    def update_notifs(self):
        self.notifs_layout.clear_widgets()

        # Coletar todas as atualizações de todos os serviços
        all_updates = []
        for service_title, service_data in self.notif_posts.items():
            if 'updates' in service_data and service_data['updates']:
                for update in service_data['updates']:
                    # Adiciona o título do serviço a cada atualização para exibição
                    update_with_service_context = {
                        'service_title': service_title,
                        'status': service_data.get('status', 'N/A'),
                        'image_path': service_data.get('image', ''),
                        **update
                    }
                    all_updates.append(update_with_service_context)
        
        # Ordenar todas as atualizações pela data (mais recentes primeiro)
        try:
            all_updates.sort(
                key=lambda x: datetime.strptime(x['date'], '%d/%m/%Y %H:%M'),
                reverse=True
            )
        except (KeyError, ValueError) as e:
            print(f"Erro ao ordenar atualizações: {e}")

        if not all_updates:
            self.notifs_layout.add_widget(Label(text="Nenhuma notificação disponível.", color=(0,0,0,1)))
            return

        for notif in all_updates:
            notif_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=200, padding=10, spacing=5)
            with notif_layout.canvas.before:
                Color(0.95, 0.95, 0.95, 1)
                notif_layout.notif_rect = Rectangle(size=notif_layout.size, pos=notif_layout.pos)
            notif_layout.bind(size=self._update_notif_rect, pos=self._update_notif_rect)

            # Cabeçalho da Notificação (Título do Serviço, Data e Status)
            header_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=30)
            
            service_title_label = Label(
                text=f"Serviço: {notif.get('service_title', 'N/A')}",
                font_size=16,
                bold=True,
                color=(0, 0, 0, 1),
                size_hint_x=0.7,
                halign='left',
                valign='middle',
                text_size=(self.notifs_content.width * 0.7 - 20, None)
            )
            header_layout.add_widget(service_title_label)

            status_color = (0, 0.7, 0, 1) if notif.get('status', 'Ativo') == 'Ativo' else (0.7, 0.7, 0, 1)
            status_label = Label(
                text=f"Status: {notif.get('status', 'N/A')}",
                font_size=12,
                color=status_color,
                size_hint_x=0.3,
                halign='right',
                valign='middle'
            )
            header_layout.add_widget(status_label)
            notif_layout.add_widget(header_layout)

            # Imagem do Serviço
            image_path = notif.get('image_path', '')
            if image_path and os.path.exists(image_path):
                service_image = Image(
                    source=image_path,
                    size_hint_y=None,
                    height=80,
                    fit_mode='contain'
                )
                notif_layout.add_widget(service_image)
            else:
                placeholder_label = Label(text="[Sem Imagem]", color=(0.5,0.5,0.5,1), size_hint_y=None, height=80)
                notif_layout.add_widget(placeholder_label)

            # Detalhes da Atualização
            update_text = notif.get('text', '')
            update_user = notif.get('user', 'Desconhecido')
            update_date = notif.get('date', 'N/A')

            update_label = Label(
                text=f"Por {update_user} em {update_date}:\n[color=000000]{update_text}[/color]",
                markup=True,
                font_size=13,
                color=(0.3, 0.3, 0.3, 1),
                halign='left',
                valign='top',
                text_size=(self.notifs_content.width - 40, None)
            )
            notif_layout.add_widget(update_label)

            self.notifs_layout.add_widget(notif_layout)

    def _update_left_rect(self, instance, value):
        self.left_rect.pos = instance.pos
        self.left_rect.size = instance.size

    def _update_right_rect(self, instance, value):
        self.right_rect.pos = instance.pos
        self.right_rect.size = instance.size

    def _update_top_bar_rect(self, instance, value):
        self.top_bar_rect.pos = instance.pos
        self.top_bar_rect.size = instance.size

    def _update_notif_rect(self, instance, value):
        instance.notif_rect.pos = instance.pos
        instance.notif_rect.size = instance.size

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
        if 'services' in self.manager.screen_names:
            self.manager.current = 'services'
        else:
            print("Erro: tela 'services' não encontrada")

    def go_to_login(self, instance):
        if 'login' in self.manager.screen_names:
            self.manager.current = 'login'
        else:
            print("Erro: tela 'login' não encontrada")

    def go_to_landing(self, instance):
        if 'landing' in self.manager.screen_names:
            self.manager.current = 'landing'
        else:
            print("Erro: tela 'landing' não encontrada")
