from kivy.uix.screenmanager import Screen # Importa a classe Screen para criar telas gerenciáveis em um ScreenManager
from kivy.uix.boxlayout import BoxLayout # Importa BoxLayout para organizar widgets em layouts lineares (vertical ou horizontal)
from kivy.uix.gridlayout import GridLayout # Importa GridLayout para organizar widgets em uma grade (não usado diretamente neste código)
from kivy.uix.label import Label # Importa Label para exibir texto estático
from kivy.uix.button import Button # Importa Button para criar botões clicáveis
from kivy.uix.image import Image # Importa Image para exibir imagens
from kivy.uix.screenmanager import ScreenManager, NoTransition, SlideTransition # Importa ScreenManager e tipos de transição (NoTransition, SlideTransition) para gerenciar múltiplas telas. Embora ScreenManager seja importado, o uso direto aqui é implicitamente via `self.manager`.
from kivy.uix.widget import Widget # Importa Widget, uma classe base para elementos de interface vazios ou genéricos (usado para espaçamento)
from kivy.graphics import Color, Rectangle # Importa Color e Rectangle para desenhar formas e definir cores no canvas do Kivy
from kivy.uix.textinput import TextInput # Importa TextInput para campos de entrada de texto (não usado diretamente neste código)
from kivy.uix.popup import Popup # Importa Popup para exibir janelas de diálogo ou mensagens
from kivy.uix.switch import Switch # Importa Switch para criar um controle de alternância (não usado diretamente neste código)
import os # Módulo para interagir com o sistema operacional (caminhos de arquivo, etc.)
from kivy.app import App # Importa a classe App, a base para qualquer aplicação Kivy
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

# --- Classe da Tela de Perfil ---

class PerfilScreen(Screen):
    """
    Representa a tela de perfil do usuário. Exibe as informações do usuário
    logado e oferece botões para navegar para outras telas do aplicativo.
    """
    def __init__(self, **kwargs):
        """
        Inicializa a tela de perfil, configurando o layout principal,
        a barra lateral de navegação e a área de exibição das informações do perfil.
        """
        super().__init__(**kwargs)

        # Layout principal horizontal que divide a tela em duas grandes áreas: navegação e conteúdo
        main_layout = BoxLayout(orientation='horizontal', spacing=10)

        # Barra lateral esquerda: ocupa 10% da largura da tela, para navegação
        left_layout = BoxLayout(orientation='vertical', size_hint_x=0.1, padding=10, spacing=10)
        # Lado direito: ocupa 90% da largura, organizado verticalmente para exibir as informações do perfil
        right_layout = BoxLayout(orientation='vertical', padding=30, spacing=15, size_hint_x=0.9)

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

        # ==================== Barra Lateral Esquerda ====================

        # Título da tela na barra lateral
        title = Label(
            text='Perfil',
            font_size=24,
            size_hint=(1, 0.2), # Ocupa 100% da largura da barra lateral, e 20% da altura disponível
            color=(0, 0, 0, 1), # Cor do texto: preto
            font_name='Roboto' # Fonte Roboto
        )
        left_layout.add_widget(title)

        # Logo do aplicativo na barra lateral
        logo = Image(
            source=resource_path(os.path.join('resources', 'logo.png')), # Caminho da imagem, compatível com PyInstaller
            size_hint=(1, None), # Largura 100%, altura automática
            height=150, # Altura fixa da imagem
            fit_mode='contain' # Ajusta a imagem para caber sem cortar
        )
        left_layout.add_widget(logo)
        
        # Widget vazio para preencher o espaço restante e empurrar os botões para baixo
        left_layout.add_widget(Widget())
        
        # Botões de navegação para outras telas
        buttons = [
            ('Ir para Landing', self.go_to_landing), # Botão para a tela de landing
            ('Ir para lista de Serviços', self.go_to_blog), # Botão para a tela de blog/lista de serviços
            ('Ir para Notificações', self.go_to_notifs), # Botão para a tela de notificações
            ('Solicitar Serviço', self.go_to_services), # Botão para a tela de solicitação de serviços
            ('Sair', self.go_to_login) # Botão para sair (voltar para a tela de login)
        ]
        # Loop para criar e adicionar cada botão à barra lateral
        for text, callback in buttons:
            btn = Button(
                text=text,
                size_hint=(1, 0.5), # Largura 100%, altura 50% do espaço restante (distribuição vertical)
                background_color=(0.812, 0.812, 0.812, 1), # Cor de fundo do botão (cinza claro)
                color=(1, 1, 1, 1) # Cor do texto do botão (branco)
            )
            btn.bind(on_press=callback) # Vincula o evento de clique ao método de callback
            left_layout.add_widget(btn)

        # ==================== Conteúdo da Direita: Informações do Usuário ====================
        # Layout que conterá as informações detalhadas do usuário
        self.info_layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        right_layout.add_widget(self.info_layout) # Adiciona este layout à área direita

    # ==================== Métodos de Ciclo de Vida e Atualização de Dados ====================

    def on_pre_enter(self, *args):
        """
        Método chamado antes da tela ser exibida.
        Limpa as informações antigas e carrega as informações do usuário logado.
        """
        self.info_layout.clear_widgets() # Limpa quaisquer widgets de informação anteriores
        app = App.get_running_app() # Obtém a instância principal do aplicativo
        # Tenta obter o objeto do usuário logado do aplicativo
        usuario = getattr(app, "usuario_logado", None)
        
        if usuario:
            # Adiciona um título para a seção de informações
            self.info_layout.add_widget(Label(
                text="[b]Informações do Usuário:[/b]", # Texto em negrito (markup=True)
                font_size=20,
                color=(0, 0, 0, 1), # Cor do texto: preto
                markup=True, # Habilita o uso de marcação (ex: [b] para negrito)
                size_hint_y=None, # Altura automática pelo conteúdo
                height=40
            ))
            # Itera sobre os pares chave-valor do dicionário do usuário e os exibe
            for key, value in usuario.items():
                self.info_layout.add_widget(Label(
                    text=f"[b]{key}:[/b] {value}", # Exibe chave e valor em negrito para a chave
                    font_size=16,
                    color=(0.1, 0.1, 0.1, 1), # Cor do texto: cinza escuro
                    markup=True, # Habilita o uso de marcação
                    size_hint_y=None, # Altura automática pelo conteúdo
                    height=30
                ))
        else:
            # Se não houver usuário logado, exibe uma mensagem de erro
            self.info_layout.add_widget(Label(
                text="Nenhum usuário logado.",
                font_size=18,
                color=(1, 0, 0, 1), # Cor do texto: vermelho
                size_hint_y=None,
                height=40
            ))

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

    # ==================== Métodos de Navegação entre Telas ====================
    # Cada método acessa o ScreenManager do aplicativo e define a tela atual (current)
    # para a tela desejada, após verificar se a tela existe.

    def go_to_landing(self, instance):
        """Navega para a tela de Landing (página inicial)."""
        if 'landing' in self.manager.screen_names:
            self.manager.current = 'landing'
        else:
            print("Erro: tela 'landing' não encontrada") # Loga um erro se a tela não estiver registrada
    
    def go_to_perfil(self, instance):
        """
        Exibe um popup informando que o usuário já está na tela de perfil,
        pois o botão 'Ir para Perfil' está na própria PerfilScreen.
        """
        popup = Popup(
            title='Aviso',
            content=Label(text='Você já está no seu perfil.'),
            size_hint=(None, None),
            size=(350, 180)
        )
        popup.open()

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
        # Note: o nome da tela aqui é 'notifications', enquanto no código anterior era 'notifs'.
        # É importante que todos os nomes de tela sejam consistentes no ScreenManager.
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