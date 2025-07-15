from kivy.uix.screenmanager import Screen # Importa a classe Screen para criar telas gerenciáveis em um ScreenManager
from kivy.uix.boxlayout import BoxLayout # Importa BoxLayout para organizar widgets em linha ou coluna
from kivy.uix.label import Label # Importa Label para exibir texto estático
from kivy.uix.button import Button # Importa Button para criar botões clicáveis
from kivy.uix.textinput import TextInput # Importa TextInput para campos de entrada de texto
from kivy.graphics import Color, Rectangle # Importa Color e Rectangle para desenhar formas e definir cores no canvas do Kivy
from kivy.uix.image import Image # Importa Image para exibir imagens
from kivy.uix.popup import Popup # Importa Popup para exibir janelas de diálogo ou mensagens
from kivy.uix.widget import Widget # Importa Widget, uma classe base para elementos de interface vazios ou genéricos
import os # Módulo para interagir com o sistema operacional (caminhos de arquivo, etc.)
import sys # Módulo para acessar parâmetros específicos do sistema (usado para PyInstaller)
import json # Módulo para trabalhar com dados JSON (serialização e desserialização)
from models.user import User # Importa a classe User do módulo models.user (presume-se que define a estrutura de um usuário)
from utils.validation import validate_cep, validate_cpf # Importa funções de validação de CEP e CPF do módulo utils.validation

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

# --- Classe da Tela de Cadastro ---

class CadastroScreen(Screen):
    """
    Representa a tela de cadastro de novos usuários no aplicativo.
    Permite ao usuário inserir suas informações e registrar-se no sistema.
    """
    def __init__(self, **kwargs):
        """
        Inicializa a tela de cadastro, configurando o layout da interface,
        campos de entrada e botões.
        """
        super().__init__(**kwargs)
        self.users_json = "usuarios.json" # Define o nome do arquivo JSON onde os dados dos usuários serão armazenados

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

        # Título da seção de Cadastro
        main_layout.add_widget(Label(
            text='Cadastro',
            font_size=30,
            color=(0.094, 0.208, 0.349, 0.839) # Cor do texto (azul escuro)
        ))

        # --- Campos de Entrada de Dados ---

        # Campo Nome de Usuário
        main_layout.add_widget(Label(text='Nome:', font_size=13, color=(0.094, 0.208, 0.349, 0.839)))
        self.nome_input = TextInput(multiline=False, size_hint=(1, None), height=40) # Campo de texto de linha única
        main_layout.add_widget(self.nome_input)

        # Espaço extra para separar visualmente os campos
        main_layout.add_widget(Widget(size_hint_y=None, height=20))

        # Layout horizontal para agrupar os campos de Telefone e CPF lado a lado
        telefone_cpf_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint=(1, None), height=40)

        # Campo Telefone
        telefone_layout = BoxLayout(orientation='vertical', size_hint=(1, 3)) # Layout interno para o label e input do telefone
        telefone_layout.add_widget(Label(text='Telefone:', font_size=13, color=(0.094, 0.208, 0.349, 0.839)))
        self.telefone_input = TextInput(multiline=False, size_hint=(1, None), height=40)
        telefone_layout.add_widget(self.telefone_input)
        telefone_cpf_layout.add_widget(telefone_layout) # Adiciona o layout do telefone ao layout horizontal

        # Campo CPF
        cpf_layout = BoxLayout(orientation='vertical', size_hint=(1, 3)) # Layout interno para o label e input do CPF
        cpf_layout.add_widget(Label(text='CPF:', font_size=13, color=(0.094, 0.208, 0.349, 0.839)))
        self.cpf_input = TextInput(multiline=False, size_hint=(1, None), height=40)
        cpf_layout.add_widget(self.cpf_input)
        telefone_cpf_layout.add_widget(cpf_layout) # Adiciona o layout do CPF ao layout horizontal

        main_layout.add_widget(telefone_cpf_layout) # Adiciona o layout horizontal ao layout principal

        # Campo Senha
        main_layout.add_widget(Label(text='Senha:', font_size=13, color=(0.094, 0.208, 0.349, 0.839)))
        self.senha_input = TextInput(multiline=False, password=True, size_hint=(1, None), height=40) # Campo de senha (caracteres ocultos)
        main_layout.add_widget(self.senha_input)

        # Campo CEP
        main_layout.add_widget(Label(text='CEP:', font_size=13, color=(0.094, 0.208, 0.349, 0.839)))
        self.cep_input = TextInput(multiline=False, size_hint=(1, None), height=40)
        main_layout.add_widget(self.cep_input)

        # Campo Bairro
        main_layout.add_widget(Label(text='Bairro:', font_size=13, color=(0.094, 0.208, 0.349, 0.839)))
        self.bairro_input = TextInput(multiline=False, size_hint=(1, None), height=40)
        main_layout.add_widget(self.bairro_input)

        # --- Botões de Ação ---

        # Botão de Enviar (para submeter o formulário de cadastro)
        submit_button = Button(
            text='Enviar',
            size_hint_x=1, # Ocupa 100% da largura disponível
            height=45,
            background_color=(0.855, 0.855, 0.878, 0.831) # Cor de fundo do botão (cinza claro)
        )
        submit_button.bind(on_press=self.submit_action) # Vincula o evento de clique ao método submit_action
        main_layout.add_widget(submit_button)

        # Botão de Voltar (para retornar à tela de login)
        back_button = Button(
            text='Voltar',
            size_hint_x=1, # Ocupa 100% da largura disponível
            height=45,
            background_color=(0.855, 0.855, 0.878, 0.831) # Cor de fundo do botão (cinza claro)
        )
        back_button.bind(on_press=self.goto_login) # Vincula o evento de clique ao método goto_login
        main_layout.add_widget(back_button)

        # Label para exibir mensagens de informação ou erro ao usuário
        self.info_label = Label(text='', font_size=13, color=(0, 0.5, 0, 1)) # Texto inicial vazio, cor verde
        main_layout.add_widget(self.info_label)

    # --- Métodos Auxiliares de UI ---

    def _update_bg_rect(self, instance, value):
        """
        Atualiza a posição e o tamanho do retângulo de fundo
        para que ele se ajuste ao layout principal quando este for redimensionado.
        """
        self.bg_rect.pos = instance.pos
        self.bg_rect.size = instance.size

    # --- Métodos de Lógica de Negócio ---

    def submit_action(self, instance):
        """
        Processa a submissão do formulário de cadastro.
        Realiza validações, cria um objeto de usuário e salva os dados em um arquivo JSON.
        """
        # Validação de CPF: Chama a função validate_cpf importada
        if not validate_cpf(self.cpf_input.text):
            # Exibe um popup de erro se o CPF for inválido
            popup = Popup(
                title='CPF inválido',
                content=Label(text='O CPF informado é inválido.'),
                size_hint=(None, None), # Tamanho fixo para o popup
                size=(350, 180)
            )
            popup.open()
            return # Interrompe a execução se a validação falhar

        # Validação de CEP: Chama a função validate_cep importada
        if not validate_cep(self.cep_input.text):
            # Exibe um popup de erro se o CEP for inválido
            popup = Popup(
                title='CEP inválido',
                content=Label(text='O CEP informado é inválido ou não existe.'),
                size_hint=(None, None),
                size=(350, 180)
            )
            popup.open()
            return # Interrompe a execução se a validação falhar

        # Cria uma instância da classe User com os dados inseridos no formulário
        user = User(
            username=self.nome_input.text,
            email="",  # O campo de email não está presente na UI atual, então é deixado vazio
            telefone=self.telefone_input.text,
            cpf=self.cpf_input.text,
            cep=self.cep_input.text,
            bairro=self.bairro_input.text,
            senha=self.senha_input.text,
            is_admin=False # Novos usuários são cadastrados como não-administradores por padrão
        )

        # Carrega os usuários existentes do arquivo JSON
        try:
            with open(self.users_json, "r", encoding="utf-8") as f:
                users_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # Se o arquivo não existir ou estiver corrompido, inicia com uma lista vazia de usuários
            users_data = []

        # Adiciona os dados do novo usuário à lista de usuários existentes
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

        # Salva a lista atualizada de usuários de volta no arquivo JSON
        with open(self.users_json, "w", encoding="utf-8") as f:
            json.dump(users_data, f, ensure_ascii=False, indent=4) # Salva com formatação para legibilidade

        # Exibe um popup de confirmação de cadastro bem-sucedido
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

    # --- Métodos de Navegação ---

    def goto_login(self, instance):
        """
        Navega de volta para a tela de login.
        Verifica se a tela 'login' está registrada no ScreenManager antes de tentar a transição.
        """
        if self.manager and 'login' in self.manager.screen_names:
            self.manager.current = 'login' # Define a tela 'login' como a tela atual