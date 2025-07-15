from kivy.uix.screenmanager import Screen # Importa a classe Screen para criar telas gerenciáveis
from kivy.uix.boxlayout import BoxLayout # Importa BoxLayout para organizar widgets em linha ou coluna
from kivy.uix.gridlayout import GridLayout # Importa GridLayout para organizar widgets em uma grade
from kivy.uix.label import Label # Importa Label para exibir texto
from kivy.uix.button import Button # Importa Button para criar botões clicáveis
from kivy.uix.image import Image # Importa Image para exibir imagens
from kivy.uix.widget import Widget # Importa Widget, uma classe base para elementos de interface vazios ou genéricos
from kivy.graphics import Color, Rectangle # Importa Color e Rectangle para desenhar formas e definir cores no canvas do Kivy
from kivy.uix.popup import Popup # Importa Popup para exibir janelas de aviso ou informação
from kivy.uix.textinput import TextInput # Importa TextInput para campos de entrada de texto (comentário: não é usado neste código, pode ser removido)
from kivy.uix.scrollview import ScrollView # Importa ScrollView para criar áreas com rolagem
from kivy.app import App # Importa a classe App, a base para qualquer aplicação Kivy
import os # Módulo para interagir com o sistema operacional (caminhos de arquivo, etc.)
import sys # Módulo para acessar parâmetros específicos do sistema (usado para PyInstaller)

# --- Funções Auxiliares ---

def resource_path(relative_path):
    """
    Retorna o caminho absoluto para um recurso, garantindo que o aplicativo encontre os
    arquivos necessários tanto em ambiente de desenvolvimento quanto após ser empacotado
    com PyInstaller.

    Se o aplicativo estiver sendo executado como um executável PyInstaller,
    sys._MEIPASS aponta para o diretório temporário onde os recursos são extraídos.
    Caso contrário, busca no diretório atual do script.
    """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# --- Classe da Tela de Landing (Página Inicial) ---

class LandingScreen(Screen):
    """
    Representa a tela de 'landing page' ou página inicial do aplicativo.
    É a primeira tela que o usuário vê após o login, apresentando uma
    visão geral do aplicativo e opções de navegação.
    """
    def __init__(self, **kwargs):
        """
        Inicializa a tela de landing, configurando o layout principal,
        a barra lateral, a barra superior e o conteúdo principal com informações
        sobre o aplicativo.
        """
        super().__init__(**kwargs)

        # Layout principal horizontal que divide a tela em duas grandes áreas
        main_layout = BoxLayout(orientation='horizontal', spacing=10)

        # Barra lateral esquerda: ocupa 25% da largura da tela
        left_layout = BoxLayout(orientation='vertical', size_hint_x=0.25, padding=10, spacing=10)
        # Área da direita: ocupa 75% da largura, organizada em 2 linhas (barra superior de usuário + conteúdo)
        right_layout = GridLayout(cols=1, rows=2, size_hint_x=0.75, padding=10, spacing=10)

        # Adiciona os layouts filhos ao layout principal
        main_layout.add_widget(left_layout)
        main_layout.add_widget(right_layout)

        # Adiciona o layout principal à tela
        self.add_widget(main_layout)

        # --- Fundos Coloridos para os Layouts ---
        # Desenha um retângulo cinza claro como fundo para a barra lateral esquerda
        with left_layout.canvas.before:
            Color(0.9, 0.9, 0.9, 1) # Cor cinza claro (RGB, Alpha)
            self.left_rect = Rectangle(size=left_layout.size, pos=left_layout.pos)
        # Vincula o redimensionamento e reposicionamento do retângulo ao tamanho e posição do left_layout
        left_layout.bind(size=self._update_left_rect, pos=self._update_left_rect)

        # Desenha um retângulo branco como fundo para a área direita
        with right_layout.canvas.before:
            Color(1, 1, 1, 1) # Cor branca
            self.right_rect = Rectangle(size=right_layout.size, pos=right_layout.pos)
        # Vincula o redimensionamento e reposicionamento do retângulo ao tamanho e posição do right_layout
        right_layout.bind(size=self._update_right_rect, pos=self._update_right_rect)

        # ==================== Layout da Esquerda (Barra Lateral) ====================

        # Título principal do aplicativo na barra lateral
        title = Label(
            text='Arruma Minha Cidade',
            font_size=24,
            size_hint=(1, 0.2), # Largura 100%, altura 20% do espaço disponível
            color=(0, 0, 0, 1), # Cor do texto: preto
            font_name='Roboto' # Fonte Roboto
        )
        left_layout.add_widget(title)

        # Logo do aplicativo na barra lateral
        logo = Image(
            source=resource_path(os.path.join('resources', 'logo.png')), # Caminho da imagem, compatível com PyInstaller
            size_hint=(1, None), # Largura 100%, altura automática
            height=300, # Altura fixa da imagem
            fit_mode='contain' # Ajusta a imagem para caber sem cortar
        )
        left_layout.add_widget(logo)

        # Botões de navegação na barra lateral
        buttons = [
            ('Ir para Landing', self.go_to_landing), # Botão para a própria tela de landing (com aviso)
            ('Ir para lista de Serviços', self.go_to_blog), # Botão para a tela de blog/lista de serviços
            ('Ir para Notificações', self.go_to_notifs), # Botão para a tela de notificações
            ('Solicitar Serviço', self.go_to_services), # Botão para a tela de solicitação de serviços
            ('Sair', self.go_to_login) # Botão para sair (voltar para a tela de login)
        ]
        # Loop para criar e adicionar cada botão à barra lateral
        for text, callback in buttons:
            btn = Button(
                text=text,
                size_hint=(1, 0.2), # Largura 100%, altura 20% do espaço restante (distribuição vertical)
                background_color=(0.1, 0.7, 0.3, 1), # Cor de fundo do botão (verde)
                color=(1, 1, 1, 1) # Cor do texto do botão (branco)
            )
            btn.bind(on_press=callback) # Vincula o evento de clique ao método de callback
            left_layout.add_widget(btn)

        # ==================== Layout da Direita: Barra Superior (Perfil do Usuário) ====================

        # Barra superior contendo o nome do usuário e a imagem de perfil
        top_bar = BoxLayout(
            orientation='horizontal',
            size_hint_y=None, # Altura fixa
            height=80,
            padding=10,
            spacing=10
        )

        # Widget vazio para empurrar o nome do usuário e a imagem para a direita
        top_bar.add_widget(Widget(size_hint_x=1))

        # Label para exibir o nome do usuário logado (será atualizado em on_pre_enter)
        usuario_nome = "Usuário" # Nome padrão, caso não haja usuário logado
        app = App.get_running_app() # Obtém a instância principal do aplicativo
        # Verifica se há um usuário logado e obtém seu nome
        if hasattr(app, "usuario_logado") and app.usuario_logado:
            usuario_nome = app.usuario_logado.get("username", "Usuário")
        self.user_label = Label(
            text=f'Olá, {usuario_nome}!',
            font_size=20,
            color=(0, 0, 0, 1), # Cor do texto: preto
            size_hint=(None, None), # Tamanho fixo
            size=(200, 60),
            halign='right', # Alinhamento horizontal à direita
            valign='middle' # Alinhamento vertical ao meio
        )
        # Garante que o texto se ajuste ao tamanho do label
        self.user_label.bind(size=self.user_label.setter('text_size'))
        top_bar.add_widget(self.user_label)

        # Imagem de perfil (clicável para ir para a tela de perfil)
        profile_pic = Image(
            source=resource_path(os.path.join('resources', 'logo.png')), # Caminho da imagem do perfil
            size_hint=(None, None), # Tamanho fixo
            size=(60, 60),
            fit_mode='contain'
        )
        # Vincula o evento de toque à função que leva para a tela de perfil
        profile_pic.bind(on_touch_down=self._on_profile_pic_touch)
        top_bar.add_widget(profile_pic)
        self.profile_pic = profile_pic # Armazena a referência para uso posterior

        # Adiciona a barra superior à primeira linha do right_layout (o GridLayout)
        right_layout.add_widget(top_bar)

        # ==================== Layout da Direita: Conteúdo Principal (Scrollable) ====================

        # Adiciona um ScrollView para permitir a rolagem do conteúdo principal se este exceder a altura da tela
        scroll_view_content = ScrollView(
            size_hint=(1, 1), # Ocupa todo o espaço restante disponível
            do_scroll_x=False # Desativa a rolagem horizontal
        )

        # BoxLayout vertical que conterá todo o texto e informações da landing page.
        # size_hint_y=None e bind(minimum_height...) são cruciais para que o ScrollView
        # funcione corretamente, permitindo que o conteúdo "cresça" e se torne rolavel.
        right_content = BoxLayout(
            orientation='vertical',
            spacing=20, # Espaçamento entre os widgets internos
            padding=30, # Preenchimento interno
            size_hint_y=None # Essencial: altura será determinada pelo conteúdo mínimo
        )
        # Vincula a altura do right_content à altura mínima necessária para conter todos os seus filhos,
        # garantindo que o ScrollView possa rolar quando o conteúdo for maior que a área visível.
        right_content.bind(minimum_height=right_content.setter('height'))

        # Adiciona o BoxLayout de conteúdo ao ScrollView
        scroll_view_content.add_widget(right_content)

        # Adiciona o ScrollView (que agora contém o right_content) à segunda linha do right_layout
        right_layout.add_widget(scroll_view_content)

        # ======= Título principal do conteúdo =======
        title_label = Label(
            text="Ajude a Construir a Cidade Perfeita com o Arruma Minha Cidade!",
            font_size=23,
            bold=True, # Texto em negrito
            color=(0.1, 0.3, 0.6, 1), # Cor do texto (azul)
            halign='center', # Alinhamento horizontal centralizado
            valign='top', # Alinhamento vertical no topo
            size_hint_y=None # Altura será definida automaticamente pelo texto
        )
        # Vincula o 'text_size' à largura do label para que o texto quebre linhas automaticamente
        title_label.bind(width=lambda instance, value: setattr(instance, 'text_size', (value, None)))
        right_content.add_widget(title_label)

        # ======= Subtítulo =======
        subtitle_label = Label(
            text="Cansado de buracos nas ruas, iluminação pública falha ou lixo acumulado?\n"
                 "Com o Arruma Minha Cidade, você tem o poder de fazer a diferença!",
            font_size=19,
            color=(0.2, 0.2, 0.2, 1), # Cor cinza escuro
            halign='center',
            valign='top',
            size_hint_y=None
        )
        subtitle_label.bind(width=lambda instance, value: setattr(instance, 'text_size', (value, None)))
        right_content.add_widget(subtitle_label)

        # ======= Texto explicativo sobre a funcionalidade do aplicativo =======
        explanation_label = Label(
            text="Nossa aplicação facilita a comunicação entre você e a prefeitura. "
                 "De forma rápida e intuitiva, você pode reportar problemas em sua rua, bairro ou qualquer canto da cidade. "
                 "Tire uma foto, adicione uma breve descrição e envie – pronto! Sua solicitação será encaminhada diretamente aos órgãos responsáveis.",
            font_size=18,
            color=(0.1, 0.1, 0.1, 1), # Cor preta quase total
            halign='center',
            valign='top',
            size_hint_y=None
        )
        explanation_label.bind(width=lambda instance, value: setattr(instance, 'text_size', (value, None)))
        right_content.add_widget(explanation_label)

        # ======= Título da seção "O que você pode fazer" =======
        what_you_can_do_label = Label(
            text="O Que Você Pode Fazer com o Arruma Minha Cidade:",
            font_size=23,
            color=(0.1, 0.3, 0.6, 1), # Cor azul
            halign='center',
            valign='top',
            size_hint_y=None
        )
        what_you_can_do_label.bind(width=lambda instance, value: setattr(instance, 'text_size', (value, None)))
        right_content.add_widget(what_you_can_do_label)

        # ======= Lista detalhada de funcionalidades =======
        features_label = Label(
            text=(
                "[b]• Reportar Problemas de Forma Simples:[/b] " # [b]...[/b] para negrito (markup)
                "Buracos, calçadas danificadas, lixo, iluminação, sinalização, vazamentos e muito mais. "
                "Basta alguns cliques para registrar sua ocorrência.\n\n" # \n\n para quebra de linha com espaçamento
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
            markup=True, # Habilita o uso de tags de formatação de texto (ex: [b] para negrito)
            size_hint_y=None
        )
        features_label.bind(width=lambda instance, value: setattr(instance, 'text_size', (value, None)))
        right_content.add_widget(features_label)

    # ==================== Métodos de Atualização de Fundos ====================
    # Estes métodos são chamados quando o tamanho ou a posição dos layouts vinculados mudam,
    # garantindo que os retângulos de fundo se ajustem corretamente.

    def _update_left_rect(self, instance, value):
        """Atualiza a posição e o tamanho do retângulo de fundo do layout esquerdo."""
        self.left_rect.pos = instance.pos
        self.left_rect.size = instance.size

    def _update_right_rect(self, instance, value):
        """Atualiza a posição e o tamanho do retângulo de fundo do layout direito."""
        self.right_rect.pos = instance.pos
        self.right_rect.size = instance.size

    def _update_top_bar_rect(self, instance, value):
        """
        Este método está presente mas é marcado como 'pass' porque
        a `top_bar` pode não ter um `Rectangle` diretamente associado a ele
        neste layout específico, ou seu fundo é tratado de outra forma.
        Pode ser removido se não houver uso.
        """
        pass

    # ==================== Métodos de Navegação entre Telas ====================
    # Cada método acessa o ScreenManager do aplicativo e define a tela atual (current)
    # para a tela desejada, após verificar se a tela existe.

    def go_to_landing(self, instance):
        """
        Exibe um popup informando que o usuário já está na tela de landing,
        pois o botão 'Ir para Landing' está na própria LandingScreen.
        """
        popup = Popup(
            title='Aviso',
            content=Label(text='Você já está na tela de landing.'),
            size_hint=(None, None),
            size=(350, 180)
        )
        popup.open()

    def go_to_perfil(self, instance):
        """Navega para a tela de Perfil."""
        if 'perfil' in self.manager.screen_names:
            self.manager.current = 'perfil'
        else:
            print("Erro: tela 'perfil' não encontrada") # Loga um erro se a tela não estiver registrada

    def go_to_blog(self, instance):
        """Navega para a tela de Blog (lista de serviços/atualizações)."""
        if 'blog' in self.manager.screen_names:
            self.manager.current = 'blog'
        else:
            print("Erro: tela 'blog' não encontrada")

    def go_to_services(self, instance):
        """Navega para a tela de Solicitação de Serviços."""
        if 'services' in self.manager.screen_names:
            self.manager.current = 'services'
        else:
            print("Erro: tela 'services' não encontrada")

    def go_to_notifs(self, instance):
        """Navega para a tela de Notificações."""
        if 'notifications' in self.manager.screen_names:
            self.manager.current = 'notifications'
        else:
            print("Erro: tela 'notifications' não encontrada")

    def go_to_login(self, instance):
        """Navega para a tela de Login (usado para 'Sair')."""
        if 'login' in self.manager.screen_names:
            self.manager.current = 'login'
        else:
            print("Erro: tela 'login' não encontrada")

    def on_pre_enter(self, *args):
        """
        Método chamado antes da tela ser exibida.
        Usado para atualizar dinamicamente o nome do usuário na barra superior.
        """
        usuario_nome = "Usuário" # Nome padrão
        app = App.get_running_app() # Obtém a instância do aplicativo
        # Verifica se há um usuário logado e atualiza o nome
        if hasattr(app, "usuario_logado") and app.usuario_logado:
            usuario_nome = app.usuario_logado.get("username", "Usuário")
        self.user_label.text = f'Olá, {usuario_nome}!' # Atualiza o texto do label

    def _on_profile_pic_touch(self, instance, touch):
        """
        Manipula o evento de toque/clique na imagem de perfil.
        Se o toque estiver dentro dos limites da imagem, navega para a tela de perfil.
        """
        if instance.collide_point(*touch.pos):
            if 'perfil' in self.manager.screen_names:
                self.manager.current = 'perfil'
            else:
                print("Erro: tela 'perfil' não encontrada")