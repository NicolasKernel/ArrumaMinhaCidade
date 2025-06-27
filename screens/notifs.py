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
from kivy.app import App
import os
import json
import datetime

class NotifsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

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

        # ==================== Barra Lateral Esquerda ====================
        title = Label(
            text='Notificações',
            font_size=22,
            size_hint=(1, None),
            height=60,
            color=(0, 0, 0, 1),
            font_name='Roboto'
        )
        left_layout.add_widget(title)

        logo = Image(
            source=os.path.join('resources', 'logo.png'),
            size_hint=(1, None),
            height=120,
            fit_mode='contain'
        )
        left_layout.add_widget(logo)
        
        left_layout.add_widget(Widget())

        buttons = [
            ('Blog', self.go_to_blog),
            ('Lista de Serviços', self.go_to_blog),
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

        # ==================== Filtros no topo da área direita ====================

        top_bar = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=80,
            padding=10,
            spacing=10
        )

        top_bar.add_widget(Widget(size_hint_x=1))
        
        self.user_label = Label(
            text=f'',
            font_size=20,
            color=(0, 0, 0, 1),
            size_hint=(None, None),
            size=(200, 60),
            halign='right',
            valign='middle'
        )
        self.user_label.bind(size=self.user_label.setter('text_size'))
        top_bar.add_widget(self.user_label)

        profile_pic = Image(
            source=os.path.join('resources', 'logo.png'),
            size_hint=(None, None),
            size=(60, 60),
            fit_mode='contain'
        )
        profile_pic.bind(on_touch_down=self._on_profile_pic_touch)
        top_bar.add_widget(profile_pic)
        self.profile_pic = profile_pic

        right_layout.add_widget(top_bar)

        # ==================== Conteúdo Principal Direita ====================
        right_content = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # Título da tela
        title = Label(
            text='Notificações dos Serviços que você segue',
            font_size=24,
            size_hint_y=None,
            height=50,
            color=(0, 0, 0, 1),
            font_name='Roboto',
            halign='center',
            text_size=(None, None)
        )
        right_content.add_widget(title)

        # ScrollView para a lista de notificações
        self.scroll = ScrollView(size_hint=(1, 1))
        self.notif_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            spacing=15,
            padding=[10, 10, 10, 10]
        )
        self.notif_layout.bind(minimum_height=self.notif_layout.setter('height'))

        with self.notif_layout.canvas.before:
            Color(0.95, 0.95, 0.95, 1)
            self.notif_rect = Rectangle(size=self.notif_layout.size, pos=self.notif_layout.pos)
        self.notif_layout.bind(size=self._update_notif_rect, pos=self._update_notif_rect)

        self.scroll.add_widget(self.notif_layout)
        right_content.add_widget(self.scroll)

        # Botão para voltar à tela inicial
        back_button = Button(
            text='Voltar para Landing',
            size_hint=(1, None),
            height=50,
            background_color=(0.1, 0.7, 0.3, 1),
            color=(1, 1, 1, 1)
        )
        back_button.bind(on_press=self.go_to_landing)
        right_content.add_widget(back_button)

        right_layout.add_widget(right_content)

    def on_pre_enter(self, *args):
        app = App.get_running_app()
        usuario_nome = "Usuário"
        if hasattr(app, "usuario_logado") and app.usuario_logado:
            usuario_nome = app.usuario_logado.get("username", "Usuário")
        self.user_label.text = f'{usuario_nome}!'
        self.notif_posts = []
        if app.usuario_logado and "seguindo" in app.usuario_logado:
            try:
                with open("services_updates.json", "r", encoding="utf-8") as f:
                    all_services = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                all_services = {}

            for service in all_services.values():
                service_id = service.get("id")
                if service_id and service_id in app.usuario_logado["seguindo"]:
                    updates = service.get("updates", [])
                    for update in updates:
                        self.notif_posts.append({
                            "id": service_id,
                            "title": service.get("title", ""),
                            "text": update.get("text", ""),
                            "date": update.get("date", "")
                        })
        # Ordena por data decrescente (mais recente primeiro)
        def parse_date(d):
            try:
                return datetime.datetime.strptime(d, "%d/%m/%Y %H:%M")
            except Exception:
                return datetime.datetime.min
        self.notif_posts.sort(key=lambda x: parse_date(x.get("date", "")), reverse=True)
        self.update_notifs(self.notif_posts)

    def update_notifs(self, notif_posts):
        
        self.notif_layout.add_widget(Label(
                text="As notificações aparecerão aqui quando você seguir serviços.",
                font_size=16,
                color=(0.5, 0.5, 0.5, 1),
                size_hint_y=None,
                height=40
        ))

        for notif in notif_posts:
            post = BoxLayout(
                orientation='horizontal',
                size_hint_y=None,
                height=80,
                padding=[10, 5, 10, 5],
                spacing=10
            )
            with post.canvas.before:
                Color(1, 1, 1, 1)
                post.post_rect = Rectangle(size=post.size, pos=post.pos)
            post.bind(size=self._update_post_rect, pos=self._update_post_rect)

            # Apenas os campos pedidos: ID, Título, Atualização do admin, Data
            id_label = Label(
                text=f'ID: {notif.get("id", "")}',
                font_size=12,
                color=(0, 0, 0, 1),
                size_hint_x=0.2,
                halign='left',
                valign='middle'
            )
            title_label = Label(
                text=f'Título: {notif.get("title", "")}',
                font_size=14,
                color=(0, 0, 0, 1),
                size_hint_x=0.3,
                halign='left',
                valign='middle'
            )
            update_label = Label(
                text=f'Atualização: {notif.get("text", "")}',
                font_size=12,
                color=(0, 0, 0, 1),
                size_hint_x=0.3,
                halign='left',
                valign='middle'
            )
            date_label = Label(
                text=f'Data: {notif.get("date", "")}',
                font_size=12,
                color=(0.5, 0.5, 0.5, 1),
                size_hint_x=0.2,
                halign='left',
                valign='middle'
            )
            for lbl in [id_label, title_label, update_label, date_label]:
                lbl.bind(size=lbl.setter('text_size'))
                post.add_widget(lbl)

            self.notif_layout.add_widget(post)

    def _update_left_rect(self, instance, value):
        self.left_rect.pos = instance.pos
        self.left_rect.size = instance.size

    def _update_right_rect(self, instance, value):
        self.right_rect.pos = instance.pos
        self.right_rect.size = instance.size

    def _update_notif_rect(self, instance, value):
        self.notif_rect.pos = instance.pos
        self.notif_rect.size = instance.size

    def _update_post_rect(self, instance, value):
        instance.post_rect.pos = instance.pos
        instance.post_rect.size = instance.size

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

    def _on_profile_pic_touch(self, instance, touch):
        if instance.collide_point(*touch.pos):
            if 'perfil' in self.manager.screen_names:
                self.manager.current = 'perfil'
            else:
                print("Erro: tela 'perfil' não encontrada")

    def go_to_landing(self, instance):
        if 'landing' in self.manager.screen_names:
            self.manager.current = "landing"
            
            
    def go_to_login(self, instance):
        if 'login' in self.manager.screen_names:
            self.manager.current = 'login'
        else:
            print("Erro: tela 'login' não encontrada")