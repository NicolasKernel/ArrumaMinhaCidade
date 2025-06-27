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
from kivy.uix.switch import Switch
import os

class PerfilScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Layout principal horizontal
        main_layout = BoxLayout(orientation='horizontal', spacing=10)

        # Barra lateral esquerda para navegação
        left_layout = BoxLayout(orientation='vertical', size_hint_x=0.1, padding=10, spacing=10)
        # Lado direito: GridLayout com 2 colunas
        right_layout = GridLayout(cols=2, padding=10, spacing=10, size_hint_x=0.9)

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
            text='Configurações',
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
            ('Perfil', self.go_to_perfil),
            ('Notificações', self.go_to_notifs),
            ('Privacidade', self.go_to_privacy),
            ('< Voltar', self.go_to_landing),
            ('< Logout', self.go_to_login)
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

        # ==================== Conteúdo da Primeira Coluna ====================
        right_content = BoxLayout(orientation='vertical', spacing=20, padding=30)
        self.name_input = TextInput(
            hint_text='Nome',
            text='Usuário Exemplo',
            size_hint_y=None,
            height=30
        )
        self.email_input = TextInput(
            hint_text='Email',
            text='usuario@email.com',
            size_hint_y=None,
            height=30
        )
        self.cep_input = TextInput(
            hint_text='CEP',
            text='00000-000',
            size_hint_y=None,
            height=30
        )
        self.phone_input = TextInput(
            hint_text='Telefone',
            text='(00) 00000-0000',
            size_hint_y=None,
            height=30
        )
        
        self.switch = Switch(
            active=True,
            size_hint_y=None,
            height=50
        )
        
        def callback(instance, value):
            if value:
                ScreenManager(transition=NoTransition())
            else:
                ScreenManager(transition=SlideTransition())
    
        
        right_content.add_widget(Label(text='Nome:', color=(0,0,0,1), size_hint_y=None, height=25))
        right_content.add_widget(self.name_input)
        right_content.add_widget(Label(text='Email:', color=(0,0,0,1), size_hint_y=None, height=25))
        right_content.add_widget(self.email_input)
        right_content.add_widget(Label(text='CEP:', color=(0,0,0,1), size_hint_y=None, height=25))
        right_content.add_widget(self.cep_input)
        right_content.add_widget(Label(text='Telefone:', color=(0,0,0,1), size_hint_y=None, height=25))
        right_content.add_widget(self.phone_input)
        right_content.add_widget(Widget())
        right_content.add_widget(Label(text='Configurações da Aplicação', font_size=20, color=(0, 0, 0, 1), size_hint_y=None, height=30))
        right_content.add_widget(Label(text='Animação de slide ao passar as telas:', color=(0,0,0,1), size_hint_y=None, height=25))
        right_content.add_widget(self.switch)
        self.switch.bind(active=callback)
        

        # ==================== Conteúdo da Segunda Coluna ====================
        right_side_content = BoxLayout(orientation='vertical', spacing=20, padding=30)
        right_side_content.size_hint_x = 0.5

        # Imagem clicável no topo
        profile_img = Image(
            source=os.path.join('resources', 'logo.png'),
            size_hint=(1, None),
            height=120
        )
        def on_profile_img_touch(instance, touch):
            if profile_img.collide_point(*touch.pos):
                print("Imagem de perfil clicada!")
        profile_img.bind(on_touch_down=on_profile_img_touch)
        right_side_content.add_widget(profile_img)

        # Espaço entre imagem e botão
        right_side_content.add_widget(Widget())

        # Botão de salvar alterações (movido para a segunda coluna)
        save_btn = Button(
            text='Salvar Alterações',
            size_hint_y=None,
            height=50,
            background_color=(0.2, 0.6, 1, 1),
            color=(1, 1, 1, 1)
        )
        save_btn.bind(on_press=self.save_profile)
        right_side_content.add_widget(save_btn)

        # Adiciona ambos ao GridLayout
        right_layout.add_widget(right_content)
        right_layout.add_widget(right_side_content)
        
    # ==================== Métodos de Atualização ====================
    def _update_left_rect(self, instance, value):
        self.left_rect.pos = instance.pos
        self.left_rect.size = instance.size

    def _update_right_rect(self, instance, value):
        self.right_rect.pos = instance.pos
        self.right_rect.size = instance.size

    # ==================== Métodos de Navegação ====================
    def go_to_perfil(self, instance):
        pass  # Já está na tela de perfil

    def go_to_notifs(self, instance):
        if 'notifs' in self.manager.screen_names:
            self.manager.current = 'notifs'
        else:
            print("Erro: tela 'notifications' não encontrada")

    def go_to_privacy(self, instance):
        if 'privacy' in self.manager.screen_names:
            self.manager.current = 'privacy'
        else:
            print("Erro: tela 'privacy' não encontrada")

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

    # ==================== Salvar Perfil ====================
    def save_profile(self, instance):
        nome = self.name_input.text
        email = self.email_input.text
        cep = self.cep_input.text
        telefone = self.phone_input.text
        print(f"Salvo: Nome={nome}, Email={email}, CEP={cep}, Telefone={telefone}")
