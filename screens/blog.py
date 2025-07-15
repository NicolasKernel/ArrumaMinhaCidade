from kivy.uix.screenmanager import Screen # Importa a classe Screen para criar telas gerenciáveis
from kivy.uix.boxlayout import BoxLayout # Importa BoxLayout para organizar widgets em linha ou coluna
from kivy.uix.gridlayout import GridLayout # Importa GridLayout para organizar widgets em uma grade
from kivy.uix.label import Label # Importa Label para exibir texto
from kivy.uix.button import Button # Importa Button para criar botões clicáveis
from kivy.uix.scrollview import ScrollView # Importa ScrollView para criar áreas com rolagem
from kivy.uix.image import Image # Importa Image para exibir imagens
from kivy.uix.popup import Popup # Importa Popup para exibir janelas de aviso ou informação
from kivy.graphics import Color, Rectangle # Importa Color e Rectangle para desenhar formas e definir cores no canvas do Kivy
from kivy.uix.textinput import TextInput # Importa TextInput para campos de entrada de texto
from kivy.uix.spinner import Spinner # Importa Spinner para criar menus suspensos (dropdowns)
from kivy.uix.widget import Widget # Importa Widget, uma classe base para elementos de interface vazios ou genéricos
import os # Módulo para interagir com o sistema operacional (caminhos de arquivo, etc.)
import json # Módulo para trabalhar com dados JSON (serialização e desserialização)
import sys # Módulo para acessar parâmetros específicos do sistema (usado para PyInstaller)
from datetime import datetime # Módulo para trabalhar com datas e horas
from kivy.app import App # Importa a classe App, a base para qualquer aplicação Kivy

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

def carregar_todos_usuarios():
    """
    Carrega todos os dados dos usuários do arquivo 'usuarios.json'.
    
    Retorna:
        list: Uma lista de dicionários, onde cada dicionário representa um usuário.
              Retorna uma lista vazia se o arquivo não for encontrado ou estiver corrompido.
    """
    try:
        with open("usuarios.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Captura erros se o arquivo não existe ou se o JSON é inválido
        return []

def salvar_todos_usuarios(usuarios):
    """
    Salva a lista de usuários no arquivo 'usuarios.json'.
    
    Args:
        usuarios (list): Uma lista de dicionários contendo os dados de todos os usuários.
    
    O arquivo é salvo com indentação para legibilidade e suporta caracteres Unicode.
    """
    with open("usuarios.json", "w", encoding="utf-8") as f:
        json.dump(usuarios, f, ensure_ascii=False, indent=4)

# --- Classe da Tela do Blog ---

class BlogScreen(Screen):
    """
    Representa a tela principal do blog/atualizações de serviços.
    Permite visualizar, filtrar, ordenar e seguir/deixar de seguir serviços.
    """
    def __init__(self, **kwargs):
        """
        Inicializa a tela, configurando o layout da interface,
        variáveis de estado e carregando os dados iniciais.
        """
        super().__init__(**kwargs)
        self.json_file = "services_updates.json"  # Arquivo JSON para armazenar status e atualizações dos serviços

        # Lista para armazenar os dados de todos os serviços carregados do JSON
        self.service_updates = []
        # Conjunto para armazenar os IDs dos serviços que o usuário atual está seguindo.
        # Usado para buscas rápidas e garantia de unicidade.
        self.seguindo_servicos = set()

        # Layout principal horizontal que divide a tela em duas grandes áreas
        main_layout = BoxLayout(orientation='horizontal', spacing=10)

        # Barra lateral esquerda: para navegação, ocupa 10% da largura
        left_layout = BoxLayout(orientation='vertical', size_hint_x=0.1, padding=10, spacing=10)
        # Área da direita: ocupa 90% da largura, organizada em 2 linhas (barra superior de usuário + conteúdo)
        right_layout = GridLayout(cols=1, rows=2, size_hint_x=0.9, padding=10, spacing=10)

        # Adiciona os layouts filhos ao layout principal
        main_layout.add_widget(left_layout)
        main_layout.add_widget(right_layout)
        # Adiciona o layout principal à tela
        self.add_widget(main_layout)

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
        # Título da seção de serviços na barra lateral
        title = Label(
            text='Serviços',
            font_size=22,
            size_hint=(1, None), # Largura 100%, altura automática
            height=60,
            color=(0, 0, 0, 1), # Cor do texto: preto
            font_name='Roboto' # Fonte Roboto
        )
        left_layout.add_widget(title)

        # Logo do aplicativo
        logo = Image(
            source=resource_path(os.path.join('resources', 'logo.png')), # Caminho da imagem, compatível com PyInstaller
            size_hint=(1, None), # Largura 100%, altura automática
            height=120,
            fit_mode='contain' # Ajusta a imagem para caber sem cortar
        )
        left_layout.add_widget(logo)
        
        # Um widget vazio para preencher espaço e empurrar os botões para baixo
        left_layout.add_widget(Widget())

        # Lista de botões de navegação para a barra lateral
        buttons = [
            ('Ir para Landing', self.go_to_landing),
            ('Ir para lista de Serviços', self.go_to_blog),
            ('Ir para Notificações', self.go_to_notifs),
            ('Solicitar Serviço', self.go_to_services),
            ('Sair', self.go_to_login)
        ]
        # Cria e adiciona cada botão à barra lateral
        for text, callback in buttons:
            btn = Button(
                text=text,
                size_hint=(1, 0.5), # Largura 100%, altura relativa (0.5 do espaço restante)
                background_color=(0.1, 0.7, 0.3, 1), # Cor de fundo do botão (verde)
                color=(1, 1, 1, 1) # Cor do texto do botão (branco)
            )
            btn.bind(on_press=callback) # Vincula o evento de clique ao método de callback
            left_layout.add_widget(btn)

        # ==================== Área de Usuário Direita (topo) ====================
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
        self.user_label = Label(
            text='', # Texto inicial vazio
            font_size=20,
            color=(0, 0, 0, 1), # Cor do texto: preto
            size_hint=(None, None), # Tamanho fixo
            size=(150, 60),
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

        # Adiciona a barra superior ao layout da direita
        right_layout.add_widget(top_bar)

        # ==================== Conteúdo Principal Direita ====================
        # Área principal para exibir os posts de atualização de serviços
        right_content = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # Layout para os controles de filtro e pesquisa
        filter_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, spacing=10)

        # Spinner (dropdown) para selecionar a categoria de filtro (Bairro, Rua, Tipo de Serviço, Todos)
        self.filter_spinner = Spinner(
            text='Filtrar por', # Texto padrão
            values=('Bairro', 'Rua', 'Tipo de Serviço', 'Todos'), # Opções do spinner
            size_hint_x=None, # Largura fixa
            width=150
        )
        # Vincula a mudança de texto no spinner à função de pesquisa
        self.filter_spinner.bind(text=self.on_search_text)
        filter_layout.add_widget(self.filter_spinner)

        # Campo de entrada de texto para pesquisa
        self.search_input = TextInput(
            hint_text='Pesquisar...', # Texto de dica
            size_hint_y=None, # Altura fixa
            height=40,
            multiline=False # Uma única linha de texto
        )
        # Vincula a mudança de texto no campo de pesquisa à função de pesquisa
        self.search_input.bind(text=self.on_search_text)
        filter_layout.add_widget(self.search_input)

        # Spinner (dropdown) para selecionar o critério de ordenação (Data de Criação, Última Atualização)
        self.sort_spinner = Spinner(
            text='Ordenar por', # Texto padrão
            values=('Data de Criação', 'Última Atualização'), # Opções do spinner
            size_hint_x=None, # Largura fixa
            width=150
        )
        # Vincula a mudança de texto no spinner à função de ordenação
        self.sort_spinner.bind(text=self.on_sort_change)
        filter_layout.add_widget(self.sort_spinner)

        # Adiciona o layout de filtro ao conteúdo principal
        right_content.add_widget(filter_layout)

        # Título da seção de atualizações de serviços
        title = Label(
            text='Atualizações de Serviços',
            font_size=24,
            size_hint_y=None, # Altura fixa
            height=50,
            color=(0, 0, 0, 1), # Cor do texto: preto
            font_name='Roboto',
            halign='center', # Alinhamento horizontal centralizado
            text_size=(None, None) # Permite que o texto se ajuste automaticamente
        )
        right_content.add_widget(title)

        # ScrollView para permitir a rolagem da lista de posts se houver muitos
        self.scroll = ScrollView(size_hint=(1, 1))
        # BoxLayout vertical para conter os posts individuais.
        # size_hint_y=None e bind(minimum_height...) garantem que o layout cresça conforme os posts são adicionados.
        self.posts_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            spacing=15, # Espaçamento entre os posts
            padding=[10, 10, 10, 10]
        )
        # Garante que a altura do posts_layout seja pelo menos a altura mínima necessária para todos os seus filhos
        self.posts_layout.bind(minimum_height=self.posts_layout.setter('height'))

        # Desenha um retângulo cinza claro como fundo para o posts_layout
        with self.posts_layout.canvas.before:
            Color(0.95, 0.95,0.95,1) # Cor cinza claro
            self.posts_rect = Rectangle(size=self.posts_layout.size, pos=self.posts_layout.pos)
        # Vincula o redimensionamento e reposicionamento do retângulo ao tamanho e posição do posts_layout
        self.posts_layout.bind(size=self._update_posts_rect, pos=self._update_posts_rect)

        # Adiciona o layout dos posts ao ScrollView
        self.scroll.add_widget(self.posts_layout)
        # Adiciona o ScrollView ao conteúdo principal da direita
        right_content.add_widget(self.scroll)

        # Adiciona o conteúdo principal da direita ao layout da direita
        right_layout.add_widget(right_content)

        # Carrega os dados dos serviços do arquivo JSON ao iniciar a tela
        self.load_services_from_json()

        # Atualiza a exibição dos posts na interface com os dados carregados
        self.update_posts(self.service_updates)

    def on_pre_enter(self, *args):
        """
        Método chamado antes da tela ser exibida.
        Usado para atualizar informações dinâmicas, como o nome do usuário logado
        e os serviços que ele segue.
        """
        app = App.get_running_app() # Obtém a instância principal do aplicativo
        usuario_nome = "Usuário" # Nome padrão, caso não haja usuário logado

        # Verifica se há um usuário logado e obtém seu nome e serviços seguidos
        if hasattr(app, "usuario_logado") and app.usuario_logado:
            usuario_nome = app.usuario_logado.get("username", "Usuário")
            # Carrega os IDs dos serviços que o usuário logado está seguindo
            self.seguindo_servicos = set(app.usuario_logado.get("seguindo", []))
        
        # Atualiza o label com a mensagem de boas-vindas ao usuário
        self.user_label.text = f'Olá, {usuario_nome}!'
        # Recarrega os serviços do JSON para garantir que os dados estejam atualizados
        self.load_services_from_json()

    def load_services_from_json(self):
        """
        Carrega todos os dados dos serviços do arquivo JSON (`self.json_file`)
        para a lista `self.service_updates`.
        
        Inclui lógica para converter formatos de dados JSON antigos para o formato atual
        esperado, garantindo compatibilidade.
        """
        try:
            with open(self.json_file, 'r', encoding="utf-8") as f:
                all_updates = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # Se o arquivo não existir ou estiver corrompido, inicializa como vazio
            all_updates = {}
            return

        # Verifica se o conteúdo do JSON é um dicionário (formato esperado)
        if not isinstance(all_updates, dict):
            print(f"Erro: Formato inválido em {self.json_file}. Obtendo o dicionário esperado.")
            return

        self.service_updates = [] # Limpa a lista antes de carregar novamente
        for service_title, service_data in all_updates.items():
            # Lógica para converter o formato antigo (lista de updates) para o novo (dicionário completo de serviço)
            if isinstance(service_data, list):
                print(f"Convertendo formato antigo para {service_title}.")
                # Cria um dicionário de serviço com dados padrão e as atualizações existentes
                service_data = {
                    'id': '000AAA', # ID padrão, idealmente deveria ser único e gerado
                    'title': service_title,
                    'description': 'Descrição não disponível',
                    'date': '01/01/2023',
                    'address': 'Endereço não disponível',
                    'image': os.path.join('images', 'default.png'), # Imagem padrão
                    'status': 'Em análise',
                    'type': 'Serviço Geral',
                    'last_update': '01/01/2023 00:00',
                    'updates': service_data
                }
                all_updates[service_title] = service_data # Atualiza o dicionário principal
                # Salva o arquivo JSON com o novo formato para persistência
                with open(self.json_file, 'w', encoding="utf-8") as f:
                    json.dump(all_updates, f, indent=4, ensure_ascii=False)

            # Garante que todos os campos necessários estejam presentes no dicionário de serviço,
            # fornecendo valores padrão se ausentes.
            service = {
                'id': service_data.get('id', '000AAA'),
                'title': service_title,
                'description': service_data.get('description', 'Descrição não disponível'),
                'date': service_data.get('date', '01/01/2023'),
                'address': service_data.get('address', 'Endereço não disponível'),
                'image': service_data.get('image', resource_path(os.path.join('resources', 'default.png'))),
                'status': service_data.get('status', 'Em análise'),
                'type': service_data.get('type', 'Serviço Geral'),
                'last_update': service_data.get('last_update', f"{service_data.get('date', '01/01/2023')} 00:00"),
                'updates': service_data.get('updates', [])
            }
            self.service_updates.append(service) # Adiciona o serviço à lista

        # Atualiza a exibição dos posts na interface com os serviços carregados
        self.update_posts(self.service_updates)

    def add_service(self, new_service):
        """
        Adiciona um novo serviço à lista de atualizações e o exibe no topo.
        
        Args:
            new_service (dict): Um dicionário contendo os dados do novo serviço.
        """
        # Insere o novo serviço no início da lista para que apareça como o mais recente
        self.service_updates.insert(0, new_service)
        # Atualiza a exibição dos posts para incluir o novo serviço
        self.update_posts(self.service_updates)

    def update_posts(self, updates):
        """
        Atualiza a exibição dos posts de serviços na interface.
        
        Args:
            updates (list): Uma lista de dicionários de serviços a serem exibidos.
                            Essa lista já deve estar filtrada e ordenada.
        """
        self.posts_layout.clear_widgets() # Limpa todos os posts existentes no layout

        for update in updates:
            # Cria um BoxLayout horizontal para cada post de serviço
            post = BoxLayout(
                orientation='horizontal',
                size_hint_y=None, # Altura fixa para cada post
                height=320,
                padding=[10, 5, 10, 5],
                spacing=10
            )
            # Desenha um fundo branco para cada post
            with post.canvas.before:
                Color(1, 1, 1, 1) # Cor branca
                post.post_rect = Rectangle(size=post.size, pos=post.pos)
            # Vincula o redimensionamento e reposicionamento do retângulo ao tamanho e posição do post
            post.bind(size=self._update_post_rect, pos=self._update_post_rect)

            # Adiciona comportamento de clique ao post.
            # `on_post_touch_down` é chamado quando o post é tocado.
            post.bind(on_touch_down=self.on_post_touch_down)
            post.update_data = update  # Armazena os dados completos do serviço no widget para fácil acesso

            # Imagem do serviço
            service_image = Image(
                source=update['image'], # Caminho da imagem do serviço
                size_hint_x=0.3, # Ocupa 30% da largura do post
                size_hint_y=None,
                height=230,
                fit_mode='contain'
            )
            post.add_widget(service_image)

            # Layout vertical para as informações de texto do serviço
            text_layout = BoxLayout(
                orientation='vertical',
                size_hint_x=0.7, # Ocupa 70% da largura do post
                spacing=5
            )

            # Label para o título do serviço
            title_label = Label(
                text=update['title'],
                font_size=18,
                color=(0, 0, 0, 1),
                size_hint_y=None,
                padding=[0, 20, 0, 0],
                height=40,
                halign='left',
                valign='middle',
                text_size=(None, None)
            )
            title_label.bind(size=title_label.setter('text_size'))
            text_layout.add_widget(title_label)

            # Label para a descrição do serviço
            desc_label = Label(
                text=update['description'],
                font_size=14,
                color=(0, 0, 0, 1),
                size_hint_y=None,
                height=80,
                halign='left',
                valign='top',
                text_size=(None, None)
            )
            desc_label.bind(size=desc_label.setter('text_size'))
            text_layout.add_widget(desc_label)

            # Label para o tipo de serviço
            type_label = Label(
                text=f'Tipo: {update.get("type", "Serviço Geral")}',
                font_size=12,
                color=(0.5, 0.5, 0.5, 1), # Cor cinza
                size_hint_y=None,
                height=30,
                halign='left',
                valign='middle',
                text_size=(None, None)
            )
            type_label.bind(size=type_label.setter('text_size'))
            text_layout.add_widget(type_label)

            # Label para o endereço do serviço
            address_label = Label(
                text=f'Endereço: {update["address"]}',
                font_size=12,
                color=(0.5, 0.5, 0.5, 1),
                size_hint_y=None,
                height=30,
                halign='left',
                valign='middle',
                text_size=(None, None)
            )
            address_label.bind(size=address_label.setter('text_size'))
            text_layout.add_widget(address_label)

            # Label para o status do serviço
            status_label = Label(
                text=f'Status: {update["status"]}',
                font_size=12,
                color=(0.5, 0.5, 0.5, 1),
                size_hint_y=None,
                height=30,
                halign='left',
                valign='middle',
                text_size=(None, None)
            )
            status_label.bind(size=status_label.setter('text_size'))
            text_layout.add_widget(status_label)

            # Label para a data do serviço
            date_label = Label(
                text=f'Data: {update["date"]}',
                font_size=12,
                color=(0.5, 0.5, 0.5, 1),
                size_hint_y=None,
                height=30,
                halign='left',
                valign='middle',
                text_size=(None, None)
            )
            date_label.bind(size=date_label.setter('text_size'))
            text_layout.add_widget(date_label)

            # Botão de "Seguir" ou "Deixar de Seguir" para o serviço
            follow_btn = Button(
                # O texto muda dinamicamente com base se o serviço já está sendo seguido
                text='Seguir' if update['id'] not in self.seguindo_servicos else 'Deixar de Seguir',
                size_hint=(None, None),
                size=(120, 40),
                background_color=(0.2, 0.5, 1, 1), # Cor de fundo (azul)
                color=(1, 1, 1, 1) # Cor do texto (branco)
            )
            # Define a função de callback para o botão de seguir/deixar de seguir
            def toggle_follow(btn, update=update):
                app = App.get_running_app() # Obtém a instância do aplicativo
                
                # Verifica se o serviço já está sendo seguido
                if update['id'] in self.seguindo_servicos:
                    self.seguindo_servicos.remove(update['id']) # Remove da lista de seguidos
                    btn.text = 'Seguir' # Altera o texto do botão
                else:
                    self.seguindo_servicos.add(update['id']) # Adiciona à lista de seguidos
                    btn.text = 'Deixar de Seguir' # Altera o texto do botão

                # Atualiza os dados do usuário logado no objeto 'app.usuario_logado'
                if hasattr(app, "usuario_logado") and app.usuario_logado:
                    app.usuario_logado["seguindo"] = list(self.seguindo_servicos) # Converte o set para lista

                    # Carrega todos os usuários, encontra o usuário logado e atualiza seus serviços seguidos
                    usuarios = carregar_todos_usuarios()
                    for user in usuarios:
                        if user.get("cpf") == app.usuario_logado.get("cpf"):
                            user["seguindo"] = app.usuario_logado["seguindo"]
                            break
                    salvar_todos_usuarios(usuarios) # Salva as alterações de volta no arquivo JSON

                # Sincroniza o conjunto de serviços seguidos com os dados mais recentes do usuário logado
                self.seguindo_servicos = set(app.usuario_logado.get("seguindo", []))
            
            follow_btn.bind(on_press=toggle_follow) # Vincula o evento de clique à função toggle_follow
            text_layout.add_widget(follow_btn) # Adiciona o botão ao layout de texto

            post.add_widget(text_layout) # Adiciona o layout de texto ao post
            self.posts_layout.add_widget(post) # Adiciona o post completo ao layout de posts

    def on_post_touch_down(self, instance, touch):
        """
        Manipula o evento de toque/clique em um post de serviço.
        
        Verifica se o toque ocorreu em um botão filho do post para evitar
        conflitos (se for um botão, o clique é tratado pelo botão, não pelo post).
        Se o toque não for em um botão e for no post, navega para a tela
        de detalhes do serviço.
        """
        # Itera sobre os filhos do post para verificar se o toque foi em um botão
        for child in instance.children:
            if isinstance(child, Button) and child.collide_point(*touch.pos):
                return False # O toque foi em um botão, não processa o clique no post
            # Se o filho for um layout (como text_layout), verifica seus filhos também
            if hasattr(child, 'children'):
                for subchild in child.children:
                    if isinstance(subchild, Button) and subchild.collide_point(*touch.pos):
                        return False

        # Se o toque ocorreu no post (e não em um botão filho)
        if instance.collide_point(*touch.pos):
            self.go_to_service_update(instance.update_data) # Navega para a tela de detalhes
            return True # O evento foi tratado
        return False # O evento não foi tratado por este widget

    def on_search_text(self, instance, value):
        """
        Filtra os posts de serviços com base no texto de pesquisa e na categoria selecionada.
        """
        filtro = self.search_input.text.lower() # Converte o texto de pesquisa para minúsculas
        categoria = self.filter_spinner.text # Obtém a categoria selecionada no spinner

        # Lógica de filtragem baseada na categoria
        if categoria == 'Todos' or categoria == 'Filtrar por':
            # Filtra por título, descrição, endereço ou tipo de serviço
            filtrados = [
                s for s in self.service_updates
                if filtro in s['title'].lower() or filtro in s['description'].lower() or filtro in s['address'].lower() or filtro in s.get('type', '').lower()
            ]
        elif categoria == 'Bairro':
            # Filtra por endereço que contenha o termo "bairro"
            filtrados = [
                s for s in self.service_updates
                if filtro in s['address'].lower() and 'bairro' in s['address'].lower()
            ]
        elif categoria == 'Rua':
            # Filtra por endereço que contenha "rua" ou "av" (avenida)
            filtrados = [
                s for s in self.service_updates
                if filtro in s['address'].lower() and ('rua' in s['address'].lower() or 'av' in s['address'].lower())
            ]
        elif categoria == 'Tipo de Serviço':
            # Filtra pelo tipo de serviço
            filtrados = [
                s for s in self.service_updates
                if filtro in s.get('type', '').lower()
            ]
        else:
            # Caso nenhuma categoria específica seja selecionada ou haja um erro, mostra todos os serviços
            filtrados = self.service_updates

        self.apply_sort(filtrados) # Aplica a ordenação após a filtragem

    def on_sort_change(self, instance, value):
        """
        Chama a função para aplicar a ordenação quando o spinner de ordenação é alterado.
        """
        self.apply_sort(self.service_updates) # Aplica a ordenação na lista completa de serviços (a filtragem é feita antes)

    def apply_sort(self, updates):
        """
        Aplica a ordenação aos posts e atualiza a exibição na interface.
        
        Args:
            updates (list): A lista de serviços (já filtrada) a ser ordenada.
        """
        sort_type = self.sort_spinner.text # Obtém o tipo de ordenação selecionado no spinner
        try:
            if sort_type == 'Data de Criação':
                # Ordena pela data de criação (string '%d/%m/%Y') em ordem decrescente
                sorted_updates = sorted(
                    updates,
                    key=lambda x: datetime.strptime(x['date'], '%d/%m/%Y'),
                    reverse=True
                )
            else:  # 'Última Atualização'
                # Ordena pela data da última atualização (string '%d/%m/%Y %H:%M') em ordem decrescente
                sorted_updates = sorted(
                    updates,
                    key=lambda x: datetime.strptime(x['last_update'], '%d/%m/%Y %H:%M'),
                    reverse=True
                )
        except ValueError as e:
            # Captura erros se o formato da data estiver incorreto
            print(f"Erro na ordenação: {e}. Usando data de criação como padrão.")
            # Volta a ordenar pela data de criação como fallback
            sorted_updates = sorted(
                updates,
                key=lambda x: datetime.strptime(x['date'], '%d/%m/%Y'),
                reverse=True
            )
        self.update_posts(sorted_updates) # Atualiza a exibição com a lista ordenada

    # --- Métodos Auxiliares para Atualização de Retângulos (Fundos) ---
    # Esses métodos garantem que os fundos coloridos se ajustem ao tamanho
    # e posição dos layouts aos quais estão vinculados, mantendo a consistência visual.

    def _update_left_rect(self, instance, value):
        self.left_rect.pos = instance.pos
        self.left_rect.size = instance.size

    def _update_right_rect(self, instance, value):
        self.right_rect.pos = instance.pos
        self.right_rect.size = instance.size

    def _update_posts_rect(self, instance, value):
        self.posts_rect.pos = instance.pos
        self.posts_rect.size = instance.size

    def _update_post_rect(self, instance, value):
        instance.post_rect.pos = instance.pos
        instance.post_rect.size = instance.size

    # --- Métodos de Navegação entre Telas ---
    # Estes métodos são responsáveis por mudar de tela dentro do ScreenManager.
    # Cada método acessa o ScreenManager do aplicativo e define a tela atual (current)
    # para a tela desejada.

    def go_to_landing(self, instance):
        """Navega para a tela de Landing."""
        self.manager.current = 'landing'

    def go_to_login(self, instance):
        """Navega para a tela de Login."""
        self.manager.current = 'login'

    def go_to_notifs(self, instance):
        """Navega para a tela de Notificações."""
        self.manager.current = 'notifs'

    def go_to_profile(self, instance):
        """Navega para a tela de Perfil."""
        self.manager.current = 'profile'

    def go_to_blog(self, instance):
        """Navega para a tela do Blog (a tela atual)."""
        self.manager.current = 'blog'

    def go_to_services(self, instance):
        """Navega para a tela de Solicitação de Serviços."""
        self.manager.current = 'services'

    def _on_profile_pic_touch(self, instance, touch):
        """
        Manipula o evento de toque na imagem de perfil.
        Se o toque estiver dentro dos limites da imagem, navega para a tela de perfil.
        """
        if instance.collide_point(*touch.pos):
            self.go_to_profile(instance)
            return True
        return False

    def go_to_service_update(self, update_data):
        """
        Navega para a tela de detalhes de um serviço específico.
        
        Args:
            update_data (dict): Os dados completos do serviço a serem exibidos na tela de detalhes.
        """
        # Obtém a instância da tela de detalhes de serviço
        service_update_detail_screen = self.manager.get_screen('service_update_detail')
        # Define os dados do serviço na tela de detalhes
        service_update_detail_screen.set_service_data(update_data)
        # Navega para a tela de detalhes
        self.manager.current = 'service_update_detail'