from kivy.uix.screenmanager import Screen # Importa a classe Screen, fundamental para gerenciar múltiplas telas em um aplicativo Kivy.
from kivy.uix.boxlayout import BoxLayout # Importa BoxLayout, um layout que organiza os widgets em uma única linha (horizontal ou vertical).
from kivy.uix.gridlayout import GridLayout # Importa GridLayout, um layout que organiza os widgets em uma grade (linhas e colunas).
from kivy.uix.label import Label # Importa Label, usado para exibir texto estático na interface do usuário.
from kivy.uix.button import Button # Importa Button, um widget interativo que executa uma ação quando clicado.
from kivy.uix.textinput import TextInput # Importa TextInput, um widget para entrada de texto pelo usuário.
from kivy.uix.image import Image # Importa Image, usado para exibir imagens.
from kivy.uix.widget import Widget # Importa Widget, a classe base para todos os elementos visuais na Kivy. É usado aqui como um "espaçador" flexível.
from kivy.uix.spinner import Spinner # Importa Spinner, um widget que exibe uma lista suspensa de opções.
from kivy.graphics import Color, Rectangle # Importa Color e Rectangle para desenhar formas e definir cores diretamente no canvas de um widget.
from kivy.uix.popup import Popup # Importa Popup, uma pequena janela que aparece sobre o conteúdo principal, geralmente para mensagens ou entradas curtas.
from kivy.app import App # Importa a classe App, a classe base para qualquer aplicação Kivy.
import os # Importa o módulo os, que fornece funções para interagir com o sistema operacional (caminhos de arquivo, diretórios, etc.).
import sys # Importa o módulo sys, que fornece acesso a parâmetros e funções específicas do sistema (usado aqui para PyInstaller).
import json # Importa o módulo json, para trabalhar com dados no formato JSON (serialização e desserialização).
from datetime import datetime # Importa datetime do módulo datetime, para trabalhar com datas e horas.
import random # Importa o módulo random, para gerar números aleatórios.
import string # Importa o módulo string, que contém constantes de string (letras, dígitos, etc.).
import shutil # Importa o módulo shutil, que oferece operações de alto nível em arquivos e coleções de arquivos (usado para copiar arquivos).
from tkinter import filedialog, Tk # Importa filedialog e Tk do módulo tkinter, para abrir uma janela de seleção de arquivos nativa do sistema operacional.

def resource_path(relative_path):
    """
    Retorna o caminho absoluto para recursos (imagens, etc.)
    quando o aplicativo é empacotado com PyInstaller.
    Se não estiver rodando como um executável PyInstaller,
    retorna o caminho relativo ao diretório atual do script.
    """
    if hasattr(sys, '_MEIPASS'): # Verifica se o aplicativo está sendo executado como um executável PyInstaller.
        return os.path.join(sys._MEIPASS, relative_path) # Retorna o caminho dentro do diretório temporário do PyInstaller.
    return os.path.join(os.path.abspath("."), relative_path) # Retorna o caminho relativo ao diretório de execução do script.

class ServicesScreen(Screen):
    """
    Representa a tela onde os usuários podem solicitar e criar novos serviços.
    Inclui um formulário para preencher os detalhes do serviço e botões de navegação.
    """
    def __init__(self, **kwargs):
        """
        Inicializa a tela de serviços, configurando o layout e os widgets.
        """
        super().__init__(**kwargs)
        self.json_file = "services_updates.json"  # Define o nome do arquivo JSON para salvar os dados dos serviços.
        self.service_types = [ # Lista de tipos de serviço disponíveis para seleção.
            'Infraestrutura e Mobilidade',
            'Saneamento Básico',
            'Limpeza e Manutenção Urbana',
            'Planejamento Urbano'
        ]

        # Layout principal da tela, organizado horizontalmente, dividindo em barra lateral e área de conteúdo.
        main_layout = BoxLayout(orientation='horizontal', spacing=10)

        # Barra lateral esquerda para navegação, ocupa 10% da largura.
        left_layout = BoxLayout(orientation='vertical', size_hint_x=0.1, padding=10, spacing=10)
        # Área da direita: GridLayout com 2 linhas (área de usuário no topo, formulário abaixo), ocupa 90% da largura.
        right_layout = GridLayout(cols=1, rows=2, size_hint_x=0.9, padding=10, spacing=10)

        main_layout.add_widget(left_layout) # Adiciona a barra lateral ao layout principal.
        main_layout.add_widget(right_layout) # Adiciona a área de conteúdo ao layout principal.
        self.add_widget(main_layout) # Adiciona o layout principal à tela.

        # Desenha um retângulo cinza claro como fundo para o left_layout.
        with left_layout.canvas.before:
            Color(0.9, 0.9, 0.9, 1) # Cor cinza.
            self.left_rect = Rectangle(size=left_layout.size, pos=left_layout.pos)
        # Vincula o redimensionamento e reposicionamento do retângulo ao tamanho e posição do left_layout.
        left_layout.bind(size=self._update_left_rect, pos=self._update_left_rect)

        # Desenha um retângulo branco como fundo para o right_layout.
        with right_layout.canvas.before:
            Color(1, 1, 1, 1) # Cor branca.
            self.right_rect = Rectangle(size=right_layout.size, pos=right_layout.pos)
        # Vincula o redimensionamento e reposicionamento do retângulo ao tamanho e posição do right_layout.
        right_layout.bind(size=self._update_right_rect, pos=self._update_right_rect)

        # ==================== Conteúdo da Barra Lateral Esquerda ====================
        title = Label(
            text='Novo Serviço', # Título da seção.
            font_size=22,
            size_hint=(1, None), # Largura flexível, altura fixa.
            height=60,
            color=(0, 0, 0, 1), # Cor do texto preto.
            font_name='Roboto' # Define a fonte.
        )
        left_layout.add_widget(title)

        logo = Image(
            source=resource_path(os.path.join('resources', 'logo.png')), # Caminho da imagem do logo.
            size_hint=(1, None),
            height=120,
            fit_mode='contain' # Ajusta a imagem para caber sem cortar.
        )
        left_layout.add_widget(logo)

        left_layout.add_widget(Widget()) # Adiciona um widget flexível para ocupar o espaço restante, empurrando os botões para baixo.

        # Lista de tuplas com texto do botão e sua função de callback.
        buttons = [
            ('Ir para lista de Serviços', self.go_to_landing), # Este parece ser um botão duplicado com 'Ir para lista de Serviços' abaixo. Pode ser um erro ou intenção de ter dois caminhos para a mesma tela.
            ('Ir para lista de Serviços', self.go_to_blog), # Navega para a tela do blog/lista de serviços.
            ('Ir para Notificações', self.go_to_notifs), # Navega para a tela de notificações.
            ('Solicitar Serviço', self.go_to_services), # Já está nesta tela, mostrará um popup.
            ('Sair', self.go_to_login) # Navega para a tela de login.
        ]
        # Cria e adiciona botões dinamicamente à barra lateral.
        for text, callback in buttons:
            btn = Button(
                text=text,
                size_hint=(1, 0.5), # Ocupa a largura total da barra lateral, altura proporcional.
                background_color=(0.1, 0.7, 0.3, 1), # Cor de fundo verde.
                color=(1, 1, 1, 1) # Cor do texto branco.
            )
            btn.bind(on_press=callback) # Associa a função de callback ao evento de clique do botão.
            left_layout.add_widget(btn)

        # ==================== Área de Usuário Direita (topo) ====================
        top_bar = BoxLayout(
            orientation='horizontal',
            size_hint_y=None, # Altura fixa.
            height=80,
            padding=10,
            spacing=10
        )
        top_bar.add_widget(Widget(size_hint_x=1)) # Widget flexível para empurrar o texto do usuário e a imagem para a direita.

        self.user_label = Label(
            text='Olá, Usuário!', # Texto inicial, será atualizado dinamicamente.
            font_size=20,
            color=(0, 0, 0, 1),
            size_hint=(None, None), # Tamanho fixo.
            size=(150, 60),
            halign='right', # Alinhamento horizontal à direita.
            valign='middle' # Alinhamento vertical ao meio.
        )
        self.user_label.bind(size=self.user_label.setter('text_size')) # Garante que o texto se adapte ao tamanho do label.
        top_bar.add_widget(self.user_label)

        profile_pic = Image(
            source=resource_path(os.path.join('resources', 'logo.png')), # Imagem do perfil (temporariamente o logo).
            size_hint=(None, None),
            size=(60, 60),
            fit_mode='contain'
        )
        profile_pic.bind(on_touch_down=self._on_profile_pic_touch) # Vincula um evento de toque à imagem do perfil.
        top_bar.add_widget(profile_pic)
        self.profile_pic = profile_pic # Armazena a referência para a imagem do perfil.

        right_layout.add_widget(top_bar) # Adiciona a barra superior de usuário ao layout da direita.

        # ==================== Formulário de Criação de Serviço ====================
        right_content = BoxLayout(orientation='vertical', spacing=10, padding=[10, 5, 10, 10])

        # Título do formulário.
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

        # Layout para os campos do formulário.
        form_layout = BoxLayout(orientation='vertical', spacing=10, padding=20)

        # Campo Nome do Serviço
        form_layout.add_widget(Label(text='Nome do Serviço:', font_size=14, color=(0, 0, 0, 1), size_hint_y=None, height=30))
        self.service_name_input = TextInput(
            hint_text='Digite o nome do serviço',
            multiline=False, # Uma única linha de texto.
            size_hint_y=None,
            height=40
        )
        form_layout.add_widget(self.service_name_input)

        # Campo Descrição
        form_layout.add_widget(Label(text='Descrição do Serviço:', font_size=14, color=(0, 0, 0, 1), size_hint_y=None, height=30))
        self.description_input = TextInput(
            hint_text='Digite a descrição do serviço',
            multiline=True, # Permite múltiplas linhas de texto.
            size_hint_y=None,
            height=80
        )
        form_layout.add_widget(self.description_input)

        # Campo Endereço
        form_layout.add_widget(Label(text='Endereço:', font_size=14, color=(0, 0, 0, 1), size_hint_y=None, height=30))
        self.address_input = TextInput(
            hint_text='Digite o endereço (ex: Rua Exemplo)',
            multiline=False,
            size_hint_y=None,
            height=40
        )
        form_layout.add_widget(self.address_input)

        # Campo Número do Endereço
        form_layout.add_widget(Label(text='Número do Endereço:', font_size=14, color=(0, 0, 0, 1), size_hint_y=None, height=30))
        self.number_input = TextInput(
            hint_text='Digite o número',
            multiline=False,
            size_hint_y=None,
            height=40
        )
        form_layout.add_widget(self.number_input)

        # Campo Bairro
        form_layout.add_widget(Label(text='Bairro:', font_size=14, color=(0, 0, 0, 1), size_hint_y=None, height=30))
        self.bairro_input = TextInput(
            hint_text='Digite o bairro',
            multiline=False,
            size_hint_y=None,
            height=40
        )
        form_layout.add_widget(self.bairro_input)

        # Campo Tipo de Serviço (Spinner)
        form_layout.add_widget(Label(text='Tipo de Serviço:', font_size=14, color=(0, 0, 0, 1), size_hint_y=None, height=30))
        self.service_type_spinner = Spinner(
            text='Selecione o tipo de serviço', # Texto padrão exibido.
            values=self.service_types, # Opções do spinner.
            size_hint_y=None,
            height=40
        )
        form_layout.add_widget(self.service_type_spinner)

        # Botão para carregar imagem
        form_layout.add_widget(Label(text='Imagem do Serviço:', font_size=14, color=(0, 0, 0, 1), size_hint_y=None, height=30))
        self.image_button = Button(
            text='Selecionar Imagem',
            size_hint_y=None,
            height=40,
            background_color=(0.2, 0.6, 1, 1), # Cor de fundo azul.
            color=(1, 1, 1, 1) # Cor do texto branco.
        )
        self.image_button.bind(on_press=self.show_file_chooser) # Vincula o clique ao método show_file_chooser.
        form_layout.add_widget(self.image_button)

        # Campo para digitar/exibir o caminho da imagem.
        self.image_input = TextInput(
            hint_text='Digite o caminho da imagem (ex: images/servico.png)',
            multiline=False,
            size_hint_y=None,
            height=40
        )
        form_layout.add_widget(self.image_input)

        # Botão para criar o serviço.
        create_button = Button(
            text='Criar Serviço',
            size_hint=(1, None),
            height=50,
            background_color=(0.1, 0.7, 0.3, 1), # Cor de fundo verde.
            color=(1, 1, 1, 1) # Cor do texto branco.
        )
        create_button.bind(on_press=self.create_service) # Vincula o clique ao método create_service.
        form_layout.add_widget(create_button)

        right_content.add_widget(form_layout) # Adiciona o formulário ao conteúdo da direita.
        right_layout.add_widget(right_content) # Adiciona o conteúdo da direita ao layout principal da direita.

    def _update_left_rect(self, instance, value):
        """Atualiza a posição e o tamanho do retângulo de fundo do left_layout."""
        self.left_rect.pos = instance.pos
        self.left_rect.size = instance.size

    def _update_right_rect(self, instance, value):
        """Atualiza a posição e o tamanho do retângulo de fundo do right_layout."""
        self.right_rect.pos = instance.pos
        self.right_rect.size = instance.size

    def generate_unique_id(self):
        """
        Gera um ID único alfanumérico com 3 números e 3 letras.
        Verifica se o ID gerado já existe no arquivo JSON para garantir unicidade.
        """
        try:
            with open(self.json_file, 'r') as f:
                all_updates = json.load(f) # Carrega os dados existentes.
        except (FileNotFoundError, json.JSONDecodeError):
            all_updates = {} # Se o arquivo não existir ou estiver vazio/corrompido, inicializa como vazio.

        existing_ids = []
        # Percorre todos os serviços para coletar IDs existentes.
        for service_data in all_updates.values():
            if isinstance(service_data, dict) and 'id' in service_data:
                existing_ids.append(service_data['id'])

        while True: # Loop para garantir um ID único.
            numbers = ''.join(random.choices(string.digits, k=3)) # Gera 3 dígitos aleatórios.
            letters = ''.join(random.choices(string.ascii_uppercase, k=3)) # Gera 3 letras maiúsculas aleatórias.
            new_id = numbers + letters # Combina números e letras.
            if new_id not in existing_ids: # Verifica se o ID já existe.
                return new_id # Retorna o ID se for único.

    def show_file_chooser(self, instance):
        """
        Abre um seletor de arquivos nativo do sistema operacional usando a biblioteca tkinter.
        Permite ao usuário selecionar uma imagem e preenche o campo de texto `image_input` com o caminho.
        """
        try:
            root = Tk() # Inicializa a janela Tkinter.
            root.withdraw() # Esconde a janela principal do Tkinter, para que apenas o seletor de arquivos seja visível.
            
            file_path = filedialog.askopenfilename( # Abre a caixa de diálogo para seleção de arquivo.
                filetypes=[("Imagens", "*.png *.jpg *.jpeg")] # Filtra para mostrar apenas arquivos de imagem.
            )
            
            root.destroy() # Destrói a janela Tkinter após a seleção.
            
            if file_path:
                self.image_input.text = file_path # Preenche o campo de texto com o caminho do arquivo selecionado.
            else:
                popup = Popup( # Exibe um popup de aviso se nenhuma imagem for selecionada.
                    title='Aviso',
                    content=Label(text='Nenhuma imagem selecionada!'),
                    size_hint=(None, None),
                    size=(400, 200)
                )
                popup.open()
        except Exception as e: # Captura e exibe erros que podem ocorrer durante a seleção do arquivo.
            popup = Popup(
                title='Erro',
                content=Label(text=f'Erro ao selecionar imagem: {str(e)}'),
                size_hint=(None, None),
                size=(400, 200)
            )
            popup.open()

    def create_service(self, instance):
        """
        Coleta os dados do formulário, valida, gera um ID único, salva a imagem
        e adiciona o novo serviço ao arquivo JSON e à lista de serviços exibida na BlogScreen.
        """
        service_id = self.generate_unique_id() # Gera um ID único para o novo serviço.
        service_name = self.service_name_input.text.strip() # Obtém o nome do serviço (removendo espaços extras).
        description = self.description_input.text.strip() # Obtém a descrição.
        address = self.address_input.text.strip() # Obtém o endereço.
        number = self.number_input.text.strip() # Obtém o número do endereço.
        bairro = self.bairro_input.text.strip() # Obtém o bairro.
        image_path = self.image_input.text.strip() # Obtém o caminho da imagem.
        service_type = self.service_type_spinner.text.strip() # Obtém o tipo de serviço.

        # Validação dos campos obrigatórios.
        if not all([service_name, description, address, bairro, service_type != 'Selecione o tipo de serviço']):
            popup = Popup(
                title='Erro',
                content=Label(text='Por favor, preencha todos os campos obrigatórios, incluindo o tipo de serviço!'),
                size_hint=(None, None),
                size=(400, 200)
            )
            popup.open()
            return

        # Formata o endereço completo.
        full_address = f"{address}, {number}, {bairro}"

        current_date = datetime.now().strftime('%d/%m/%Y') # Obtém a data atual formatada.

        # Processa a imagem: copia para a pasta 'images' se um caminho válido for fornecido,
        # caso contrário, usa uma imagem padrão.
        if image_path and os.path.isfile(image_path):
            images_dir = os.path.join(os.path.abspath("."), 'images') # Define o diretório de destino para imagens.
            if not os.path.exists(images_dir):
                os.makedirs(images_dir) # Cria o diretório 'images' se ele não existir.
            img_name = f"{service_id}_{os.path.basename(image_path)}" # Cria um nome único para a imagem (ID + nome original).
            dest_path = os.path.join(images_dir, img_name) # Define o caminho completo de destino.
            try:
                shutil.copy(image_path, dest_path) # Copia o arquivo da imagem.
                image_path = os.path.join('images', img_name) # Atualiza o caminho da imagem para o caminho relativo dentro do projeto.
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
            image_path = os.path.join('images', 'default.png') # Usa imagem padrão se nenhuma for selecionada ou for inválida.

        # Cria o dicionário com os dados do novo serviço.
        new_service = {
            'id': service_id,
            'title': service_name,
            'description': description,
            'date': current_date,
            'address': full_address,
            'image': image_path,
            'status': 'Em análise', # Status inicial padrão.
            'type': service_type,
            'last_update': f"{current_date} 00:00" # Data da última atualização (inicialmente a data de criação).
        }

        # Salva o novo serviço no arquivo JSON.
        try:
            with open(self.json_file, 'r') as f:
                all_updates = json.load(f) # Carrega os serviços existentes.
        except (FileNotFoundError, json.JSONDecodeError):
            all_updates = {} # Inicializa se o arquivo não existir ou estiver vazio/corrompido.

        all_updates[service_name] = new_service # Adiciona o novo serviço ao dicionário, usando o nome como chave.

        with open(self.json_file, 'w') as f:
            json.dump(all_updates, f, indent=4) # Salva todos os serviços de volta no JSON, com formatação para legibilidade.

        # Adiciona o serviço à lista de atualizações na BlogScreen (se ela existir).
        if 'blog' in self.manager.screen_names:
            blog_screen = self.manager.get_screen('blog')
            blog_screen.add_service(new_service) # Chama um método na BlogScreen para adicionar o novo serviço.

        # Mostra um popup de sucesso.
        popup = Popup(
            title='Sucesso',
            content=Label(text='Serviço criado com sucesso!'),
            size_hint=(None, None),
            size=(400, 200)
        )
        popup.open()

        # Limpa os campos do formulário após a criação do serviço.
        self.service_name_input.text = ''
        self.description_input.text = ''
        self.address_input.text = ''
        self.number_input.text = ''
        self.bairro_input.text = ''
        self.image_input.text = ''
        self.service_type_spinner.text = 'Selecione o tipo de serviço' # Reseta o spinner para o texto padrão.

    def on_pre_enter(self, *args):
        """
        Este método é chamado antes da tela se tornar ativa.
        Ele atualiza o label de saudação com o nome do usuário logado.
        """
        app = App.get_running_app() # Obtém a instância do aplicativo Kivy em execução.
        usuario_nome = "Usuário" # Nome padrão.
        if hasattr(app, "usuario_logado") and app.usuario_logado: # Verifica se há um usuário logado nos atributos do aplicativo.
            usuario_nome = app.usuario_logado.get("username", "Usuário") # Obtém o nome de usuário se disponível.
        self.user_label.text = f'Olá, {usuario_nome}!' # Atualiza o texto do label.
        
    # ==================== Métodos de Navegação ====================
    # Estes métodos são responsáveis por mudar a tela atual do ScreenManager.
    # Cada método verifica se a tela de destino existe no ScreenManager antes de tentar mudar.

    def go_to_landing(self, instance):
        """Navega para a tela 'landing'."""
        if 'landing' in self.manager.screen_names:
            self.manager.current = 'landing'
        else:
            print("Erro: tela 'landing' não encontrada")
    
    def go_to_perfil(self, instance):
        """Navega para a tela 'perfil'."""
        if 'perfil' in self.manager.screen_names:
            self.manager.current = 'perfil'
        else:
            print("Erro: tela 'perfil' não encontrada")

    def go_to_blog(self, instance):
        """Navega para a tela 'blog' (lista de serviços)."""
        if 'blog' in self.manager.screen_names:
            self.manager.current = 'blog'
        else:
            print("Erro: tela 'blog' não encontrada")

    def go_to_services(self, instance):
        """
        Método para o botão "Solicitar Serviço".
        Como o usuário já está nesta tela, um popup é exibido informando isso.
        """
        popup = Popup(
            title='Aviso',
            content=Label(text='Você já está na solicitação de serviços.'),
            size_hint=(None, None),
            size=(350, 180)
        )
        popup.open()

    def go_to_notifs(self, instance):
        """Navega para a tela 'notifications'."""
        if 'notifications' in self.manager.screen_names:
            self.manager.current = 'notifications'
        else:
            print("Erro: tela 'notifications' não encontrada")

    def go_to_login(self, instance):
        """Navega para a tela 'login' (sair do aplicativo)."""
        if 'login' in self.manager.screen_names:
            self.manager.current = 'login'
        else:
            print("Erro: tela 'login' não encontrada")

    def _on_profile_pic_touch(self, instance, touch):
        """
        Detecta um toque na imagem de perfil e navega para a tela de perfil.
        """
        if instance.collide_point(*touch.pos): # Verifica se o toque ocorreu dentro dos limites da imagem.
            if 'perfil' in self.manager.screen_names:
                self.manager.current = 'perfil'
            else:
                print("Erro: tela 'perfil' não encontrada")