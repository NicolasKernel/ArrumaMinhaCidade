from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
import os

class LandingScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Layout principal horizontal
        main_layout = BoxLayout(orientation='horizontal', spacing=10)

        # Layouts verticais para a esquerda e direita
        left_layout = BoxLayout(orientation='vertical', size_hint_x=0.25, padding=10, spacing=10)
        # Área da direita: GridLayout com 2 linhas (área de usuário + conteúdo)
        right_layout = GridLayout(cols=1, rows=2, size_hint_x=0.75, padding=10, spacing=10)

        # Adiciona os layouts ao layout principal
        main_layout.add_widget(left_layout)
        main_layout.add_widget(right_layout)

        # Adiciona o layout principal à tela
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

        # ==================== Layout da Esquerda ====================
        
        title = Label(
            text='Arruma Minha Cidade',
            font_size=24,
            size_hint=(1, 0.2),
            color=(0, 0, 0, 1),
            font_name='Roboto'
        )
        left_layout.add_widget(title)

        logo = Image(
            source=os.path.join('resources', 'logo.png'),
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

        # ==================== Layout da Direita: Barra Superior ====================

        top_bar = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=80,
            padding=10,
            spacing=10
        )

        # Espaçador para empurrar o conteúdo para a direita
        top_bar.add_widget(Widget(size_hint_x=1))

        # Label do perfil
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

        # Foto de perfil
        profile_pic = Image(
            source=os.path.join('resources', 'logo.png'),
            size_hint=(None, None),
            size=(60, 60),
            fit_mode='contain'  
        )
        top_bar.add_widget(profile_pic)

        # Adiciona a top_bar na primeira linha do right_layout
        right_layout.add_widget(top_bar)

        # Adiciona um BoxLayout vazio (ou coloque aqui o conteúdo principal do lado direito)
        right_content = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # ======= Exemplo de barra de pesquisa =======
        search_bar = TextInput(
            hint_text='Pesquisar...',
            size_hint_y=None,
            height=40,
            multiline=False
        )
        right_content.add_widget(search_bar)

        # ======= POSTS =======

        scroll = ScrollView(size_hint=(1, 1))
        posts_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10)
        posts_layout.bind(minimum_height=posts_layout.setter('height'))

        # Adiciona alguns posts de exemplo
        for i in range(1, 6):
            post = BoxLayout(orientation='vertical', size_hint_y=None, height=100, padding=10)
            post.add_widget(Label(text=f'Post #{i}', font_size=18, color=(0,0,0,1), size_hint_y=None, height=30))
            post.add_widget(Label(text='Conteúdo do post aqui...', font_size=14, color=(0,0,0,1)))
            posts_layout.add_widget(post)

        scroll.add_widget(posts_layout)
        right_content.add_widget(scroll)

        # Adiciona o right_content ao right_layout
        right_layout.add_widget(right_content)

    # ==================== Métodos de Atualização ====================

    def _update_left_rect(self, instance, value):
        self.left_rect.pos = instance.pos
        self.left_rect.size = instance.size

    def _update_right_rect(self, instance, value):
        self.right_rect.pos = instance.pos
        self.right_rect.size = instance.size

    def _update_top_bar_rect(self, instance, value):
        self.top_bar_rect.pos = instance.pos
        self.top_bar_rect.size = instance.size

    # ==================== Métodos de Navegação ====================
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