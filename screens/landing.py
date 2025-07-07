from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput # Não usado neste código, pode ser removido se não for usar.
from kivy.uix.scrollview import ScrollView
from kivy.app import App
import os
import sys

def resource_path(relative_path):
    """Retorna o caminho absoluto para uso com PyInstaller."""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

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
            source=resource_path(os.path.join('resources', 'logo.png')),
            size_hint=(1, None),
            height=300,
            fit_mode='contain'
        )
        left_layout.add_widget(logo)

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
                size_hint=(1, 0.2),
                background_color=(0.1, 0.7, 0.3, 1),
                color=(1, 1, 1, 1)
            )
            btn.bind(on_press=callback)
            left_layout.add_widget(btn)

        # ==================== Layout da Direita: Barra Superior (INTACTA) ====================

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
        usuario_nome = "Usuário"
        app = App.get_running_app()
        if hasattr(app, "usuario_logado") and app.usuario_logado:
            usuario_nome = app.usuario_logado.get("username", "Usuário")
        self.user_label = Label(
            text=f'Olá, {usuario_nome}!',
            font_size=20,
            color=(0, 0, 0, 1),
            size_hint=(None, None),
            size=(200, 60),
            halign='right',
            valign='middle'
        )
        self.user_label.bind(size=self.user_label.setter('text_size'))
        top_bar.add_widget(self.user_label)

        # Foto de perfil
        profile_pic = Image(
            source=resource_path(os.path.join('resources', 'logo.png')),
            size_hint=(None, None),
            size=(60, 60),
            fit_mode='contain'
        )
        # Torna a imagem clicável
        profile_pic.bind(on_touch_down=self._on_profile_pic_touch)
        top_bar.add_widget(profile_pic)
        self.profile_pic = profile_pic  # Salva referência se precisar

        # Adiciona a top_bar na primeira linha do right_layout
        right_layout.add_widget(top_bar)

        # ==================== Layout da Direita: Conteúdo Principal (COM MELHORIAS) ====================

        # Adiciona um ScrollView para o conteúdo principal do lado direito
        # Isso garante que o texto seja rolavel se for maior que a tela
        scroll_view_content = ScrollView(
            size_hint=(1, 1), # Ocupa todo o espaço restante no right_layout
            do_scroll_x=False # Desativa a rolagem horizontal
        )

        # BoxLayout para o conteúdo do ScrollView
        right_content = BoxLayout(
            orientation='vertical',
            spacing=20,
            padding=30,
            size_hint_y=None # Importante para o ScrollView funcionar corretamente
        )
        # Define a altura do BoxLayout de acordo com a altura mínima de seus filhos
        right_content.bind(minimum_height=right_content.setter('height'))

        # Adiciona o BoxLayout de conteúdo ao ScrollView
        scroll_view_content.add_widget(right_content)

        # Adiciona o ScrollView (com o conteúdo) à segunda linha do right_layout
        right_layout.add_widget(scroll_view_content)


        # ======= Título principal =======
        title_label = Label(
            text="Ajude a Construir a Cidade Perfeita com o Arruma Minha Cidade!",
            font_size=23,
            bold=True,
            color=(0.1, 0.3, 0.6, 1),
            halign='center',
            valign='top',
            size_hint_y=None # Altura será definida pelo texto
        )
        # Vincula o text_size à largura do right_content para que ele se ajuste dinamicamente
        title_label.bind(width=lambda instance, value: setattr(instance, 'text_size', (value, None)))
        right_content.add_widget(title_label)


        # ======= Subtítulo =======
        subtitle_label = Label(
            text="Cansado de buracos nas ruas, iluminação pública falha ou lixo acumulado?\n"
                 "Com o Arruma Minha Cidade, você tem o poder de fazer a diferença!",
            font_size=19,
            color=(0.2, 0.2, 0.2, 1),
            halign='center',
            valign='top',
            size_hint_y=None
        )
        subtitle_label.bind(width=lambda instance, value: setattr(instance, 'text_size', (value, None)))
        right_content.add_widget(subtitle_label)


        # ======= Texto explicativo =======
        explanation_label = Label(
            text="Nossa aplicação facilita a comunicação entre você e a prefeitura. "
                 "De forma rápida e intuitiva, você pode reportar problemas em sua rua, bairro ou qualquer canto da cidade. "
                 "Tire uma foto, adicione uma breve descrição e envie – pronto! Sua solicitação será encaminhada diretamente aos órgãos responsáveis.",
            font_size=18,
            color=(0.1, 0.1, 0.1, 1),
            halign='center',
            valign='top',
            size_hint_y=None
        )
        explanation_label.bind(width=lambda instance, value: setattr(instance, 'text_size', (value, None)))
        right_content.add_widget(explanation_label)

        # ======= O que você pode fazer =======
        what_you_can_do_label = Label(
            text="O Que Você Pode Fazer com o Arruma Minha Cidade:",
            font_size=23,
            color=(0.1, 0.3, 0.6, 1),
            halign='center',
            valign='top',
            size_hint_y=None
        )
        what_you_can_do_label.bind(width=lambda instance, value: setattr(instance, 'text_size', (value, None)))
        right_content.add_widget(what_you_can_do_label)

        # ======= Lista de funcionalidades =======
        features_label = Label(
            text=(
                "[b]• Reportar Problemas de Forma Simples:[/b] "
                "Buracos, calçadas danificadas, lixo, iluminação, sinalização, vazamentos e muito mais. "
                "Basta alguns cliques para registrar sua ocorrência.\n\n"
                "[b]• Acompanhar o Progresso em Tempo Real:[/b] "
                "Chega de incertezas! Visualize o status de suas solicitações e saiba quando o problema foi recebido, está em andamento ou foi solucionado.\n\n"
                "[b]• Contribuir para uma Cidade Melhor:[/b] "
                "Sua participação é fundamental para tornar Fortaleza um lugar mais agradável e funcional para todos. "
                "Cada reporte é um passo em direção à cidade que queremos."
            ),
            font_size=18,
            color=(0, 0, 0, 1),
            halign='center',
            valign='top',
            markup=True,
            size_hint_y=None
        )
        features_label.bind(width=lambda instance, value: setattr(instance, 'text_size', (value, None)))
        right_content.add_widget(features_label)


    # ==================== Métodos de Atualização ====================

    def _update_left_rect(self, instance, value):
        self.left_rect.pos = instance.pos
        self.left_rect.size = instance.size

    def _update_right_rect(self, instance, value):
        self.right_rect.pos = instance.pos
        self.right_rect.size = instance.size

    def _update_top_bar_rect(self, instance, value):
        # Este método não é mais necessário se top_bar não tiver um Rectangle próprio
        # ou se ele estiver sendo atualizado indiretamente.
        pass

    # ==================== Métodos de Navegação ====================
    def go_to_landing(self, instance):
        popup = Popup(
            title='Aviso',
            content=Label(text='Você já está na tela de landing.'),
            size_hint=(None, None),
            size=(350, 180)
        )
        popup.open()

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

    def on_pre_enter(self, *args):
        # Atualiza o nome do usuário sempre que entrar na tela
        usuario_nome = "Usuário"
        app = App.get_running_app()
        if hasattr(app, "usuario_logado") and app.usuario_logado:
            usuario_nome = app.usuario_logado.get("username", "Usuário")
        self.user_label.text = f'Olá, {usuario_nome}!'

    def _on_profile_pic_touch(self, instance, touch):
        if instance.collide_point(*touch.pos):
            if 'perfil' in self.manager.screen_names:
                self.manager.current = 'perfil'
            else:
                print("Erro: tela 'perfil' não encontrada")