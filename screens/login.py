from kivy.uix.screenmanager import Screen # Importa a classe Screen para gerenciar múltiplas telas
from kivy.uix.boxlayout import BoxLayout # Importa BoxLayout para organizar widgets em layouts lineares (vertical ou horizontal)
from kivy.uix.label import Label # Importa Label para exibir texto estático
from kivy.uix.button import Button # Importa Button para criar botões clicáveis
from kivy.uix.textinput import TextInput # Importa TextInput para campos de entrada de texto
from kivy.uix.image import Image # Importa Image para exibir imagens
from kivy.uix.widget import Widget # Importa Widget, uma classe base para elementos de interface vazios ou genéricos (usado para espaçamento)
from kivy.graphics import Color, Rectangle # Importa Color e Rectangle para desenhar formas e definir cores no canvas do Kivy
from kivy.uix.popup import Popup # Importa Popup para exibir janelas de diálogo ou mensagens
from kivy.app import App # Importa a classe App, a base para qualquer aplicação Kivy
import os # Módulo para interagir com o sistema operacional (caminhos de arquivo, etc.)
import json # Módulo para trabalhar com dados JSON (serialização e desserialização)
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

# --- Classe da Tela de Login ---

class LoginScreen(Screen):
    """
    Representa a tela de login do aplicativo, onde os usuários podem
    inserir suas credenciais (CPF e senha) para acessar o sistema.
    Permite também a navegação para a tela de cadastro.
    """
    def __init__(self, **kwargs):
        """
        Inicializa a tela de login, configurando o layout da interface,
        campos de entrada e botões.
        """
        super().__init__(**kwargs)

        # Layout principal vertical, com preenchimento e espaçamento, para centralizar o conteúdo
        main_layout = BoxLayout(orientation='vertical', padding=60, spacing=20)
        self.add_widget(main_layout) # Adiciona o layout principal à tela

        # --- Fundo do Layout Principal ---
        # Desenha um retângulo com uma cor de fundo específica para o main_layout.
        with main_layout.canvas.before:
            Color(0.922, 0.933, 0.941, 0.831) # Cor de fundo (um tom de cinza/azul claro com transparência)
            self.bg_rect = Rectangle(size=main_layout.size, pos=main_layout.pos)
        # Vincula o tamanho e a posição do retângulo ao tamanho e posição do main_layout,
        # garantindo que o fundo se ajuste se o layout for redimensionado ou movido.
        main_layout.bind(size=self._update_bg_rect, pos=self._update_bg_rect)

        # --- Logo ---
        # Imagem do logo do aplicativo
        logo = Image(
            source=resource_path(os.path.join('resources', 'logo.png')), # Caminho da imagem do logo, compatível com PyInstaller
            size_hint=(1, None), # Ocupa 100% da largura disponível, altura automática
            height=120, # Altura fixa da imagem
            fit_mode='contain' # Ajusta a imagem para caber na área, mantendo a proporção
        )
        main_layout.add_widget(logo) # Adiciona o logo ao layout principal

        # --- Títulos da Tela ---
        # Título principal do aplicativo
        main_layout.add_widget(Label(
            text='Arruma Minha Cidade',
            font_size=28,
            size_hint=(1, None), # Ocupa 100% da largura, altura automática
            height=60,
            color=(0.094, 0.208, 0.349, 0.839), # Cor do texto (um tom de azul escuro)
            font_name='Roboto' # Fonte Roboto
        ))

        # Título da seção de Login
        main_layout.add_widget(Label(
            text='Login',
            font_size=30,
            color=(0.094, 0.208, 0.349, 0.839) # Cor do texto (azul escuro)
        ))

        # --- Campo CPF ---
        # Layout para o label "CPF:" e o TextInput do CPF
        cpf_layout = BoxLayout(orientation='vertical', spacing=5)
        cpf_layout.add_widget(Label(
            text='CPF:', font_size=13, color=(0.094, 0.208, 0.349, 0.839) # Label do campo CPF
        ))
        self.cpf_input = TextInput(
            multiline=False, # Campo de texto de linha única
            size_hint=(0.20, None), # Ocupa 20% da largura disponível, altura automática
            height=30, # Altura fixa
            pos_hint={'center_x': 0.5} # Centraliza o TextInput horizontalmente
        )
        cpf_layout.add_widget(self.cpf_input) # Adiciona o TextInput ao layout do CPF
        main_layout.add_widget(cpf_layout) # Adiciona o layout do CPF ao layout principal

        # --- Campo Senha ---
        # Layout para o label "Senha:" e o TextInput da Senha
        senha_layout = BoxLayout(orientation='vertical', spacing=5)
        senha_layout.add_widget(Label(
            text='Senha:', font_size=13, color=(0.094, 0.208, 0.349, 0.839) # Label do campo Senha
        ))
        self.senha_input = TextInput(
            multiline=False, # Campo de texto de linha única
            password=True, # Oculta os caracteres digitados (para senhas)
            size_hint=(0.20, None), # Ocupa 20% da largura disponível, altura automática
            height=30, # Altura fixa
            pos_hint={'center_x': 0.5} # Centraliza o TextInput horizontalmente
        )
        senha_layout.add_widget(self.senha_input) # Adiciona o TextInput ao layout da senha
        main_layout.add_widget(senha_layout) # Adiciona o layout da senha ao layout principal

        # Espaçador para aumentar a distância visual entre os campos e os botões
        main_layout.add_widget(Widget(size_hint_y=None, height=30))

        # --- Botão Entrar ---
        login_button = Button(
            text='Entrar',
            size_hint=(0.2, None), # Ocupa 20% da largura, altura automática
            height=50, # Altura fixa
            background_color=(0.855, 0.855, 0.878, 0.831), # Cor de fundo do botão (cinza claro)
            pos_hint={'center_x': 0.5} # Centraliza o botão horizontalmente
        )
        login_button.bind(on_press=self.login_action) # Vincula o evento de clique ao método login_action
        main_layout.add_widget(login_button)

        # --- Botão Cadastro ---
        signup_button = Button(
            text='Cadastro',
            size_hint=(0.2, None), # Ocupa 20% da largura, altura automática
            height=50, # Altura fixa
            background_color=(0.855, 0.855, 0.878, 0.831), # Cor de fundo do botão (cinza claro)
            pos_hint={'center_x': 0.5} # Centraliza o botão horizontalmente
        )
        signup_button.bind(on_press=self.signup_action) # Vincula o evento de clique ao método signup_action
        main_layout.add_widget(signup_button)

        # Label para exibir mensagens de erro (inicialmente vazio)
        self.error_label = Label(text='', font_size=13, color=(1, 0, 0, 1)) # Cor do texto: vermelho
        main_layout.add_widget(self.error_label)

        # Nome do arquivo JSON onde os dados dos usuários estão armazenados
        self.users_json = "usuarios.json"

    # --- Métodos Auxiliares de UI ---

    def _update_bg_rect(self, instance, value):
        """
        Atualiza a posição e o tamanho do retângulo de fundo
        para que ele se ajuste ao layout principal quando este for redimensionado.
        """
        self.bg_rect.pos = instance.pos
        self.bg_rect.size = instance.size

    # --- Métodos de Lógica de Negócio ---

    def login_action(self, instance):
        """
        Processa a tentativa de login do usuário.
        Verifica as credenciais (CPF e senha) contra os dados armazenados em 'usuarios.json'.
        Redireciona para a tela apropriada (admin ou landing) ou exibe um erro.
        """
        cpf = self.cpf_input.text # Obtém o CPF digitado pelo usuário
        senha = self.senha_input.text # Obtém a senha digitada pelo usuário

        users_data = [] # Inicializa a lista de dados de usuários vazia
        try:
            # Tenta abrir e carregar o arquivo JSON de usuários
            with open(self.users_json, "r", encoding="utf-8") as f:
                users_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # Se o arquivo não existir ou estiver corrompido, a lista de usuários permanece vazia
            users_data = []

        usuario_encontrado = None # Variável para armazenar o usuário encontrado, se houver
        # Itera sobre os usuários carregados para encontrar uma correspondência de CPF e senha
        for user in users_data:
            if user.get("cpf") == cpf and user.get("senha") == senha:
                usuario_encontrado = user # Usuário encontrado
                break # Sai do loop assim que encontrar o usuário

        if usuario_encontrado:
            # Se um usuário for encontrado, verifica se o campo "seguindo" existe, caso contrário, adiciona
            if "seguindo" not in usuario_encontrado:
                usuario_encontrado["seguindo"] = []
            print(f"Usuário {cpf} logado com sucesso!") # Mensagem no console para depuração
            # Armazena as informações do usuário logado na instância principal do aplicativo
            App.get_running_app().usuario_logado = usuario_encontrado

            # Redireciona para a tela de 'admin' se o usuário for um administrador
            if usuario_encontrado.get("is_admin", False): # Assume False se 'is_admin' não estiver presente
                if self.manager and 'admin' in self.manager.screen_names:
                    self.manager.current = 'admin'
            # Caso contrário, redireciona para a tela de 'landing' (página inicial do usuário comum)
            elif self.manager and 'landing' in self.manager.screen_names:
                self.manager.current = 'landing'
        else:
            # Se nenhum usuário for encontrado com as credenciais fornecidas, exibe um popup de erro
            popup = Popup(
                title='Erro de Login',
                content=Label(text='CPF ou senha incorretos!'),
                size_hint=(None, None), # Tamanho fixo para o popup
                size=(350, 180)
            )
            popup.open() # Abre o popup

    # --- Métodos de Navegação ---

    def signup_action(self, instance):
        """
        Navega para a tela de Cadastro quando o botão 'Cadastro' é pressionado.
        """
        if self.manager and 'cadastro' in self.manager.screen_names:
            self.manager.current = 'cadastro' # Define a tela 'cadastro' como a tela atual