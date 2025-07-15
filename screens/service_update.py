from kivy.uix.screenmanager import Screen # Importa a classe Screen, que é a base para criar diferentes "telas" em um aplicativo Kivy, permitindo a navegação entre elas.
from kivy.uix.boxlayout import BoxLayout # Importa BoxLayout, um layout que organiza widgets em uma única linha, seja horizontal ou verticalmente.
from kivy.uix.label import Label # Importa Label, usado para exibir texto estático na interface.
from kivy.uix.button import Button # Importa Button, um widget interativo que executa uma ação quando clicado.
from kivy.uix.textinput import TextInput # Importa TextInput, um widget para entrada de texto pelo usuário.
from kivy.uix.scrollview import ScrollView # Importa ScrollView, um contêiner que permite que seu conteúdo seja rolado se for maior que a área visível.
from kivy.uix.image import Image # Importa Image, usado para exibir imagens.
from kivy.uix.spinner import Spinner # Importa Spinner, um widget que exibe uma lista suspensa de opções.
from kivy.graphics import Color, Rectangle # Importa Color e Rectangle para desenhar formas e definir cores diretamente no canvas de um widget.
import os # Importa o módulo os, que fornece funções para interagir com o sistema operacional, como manipulação de caminhos de arquivo.
from datetime import datetime # Importa datetime do módulo datetime, para trabalhar com datas e horas.
import json # Importa o módulo json, para trabalhar com dados no formato JSON (serializar e desserializar).
from kivy.app import App # Importa a classe App, a classe base para qualquer aplicação Kivy.

class ServiceUpdateScreen(Screen):
    """
    Representa a tela de detalhes e atualização de um serviço.
    Permite visualizar informações do serviço, alterar seu status (apenas para administradores)
    e adicionar novas atualizações.
    """
    def __init__(self, **kwargs):
        """
        Inicializa a tela de detalhes de atualização de serviço.
        Configura os layouts, widgets e atributos iniciais.
        """
        super().__init__(**kwargs)
        self.update_data = None  # Dicionário que irá conter os dados do serviço atual (título, descrição, etc.).
        self.current_user = "Administrador"  # Nome do usuário logado (fixo para fins de demonstração).
        self.is_admin = True  # Flag booleana indicando se o usuário tem privilégios de administrador (fixo para demonstração).
        self.json_file = "services_updates.json"  # Nome do arquivo JSON onde as atualizações e status dos serviços são salvos.

        # Layout principal da tela, organizado verticalmente com preenchimento e espaçamento.
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Título da tela, exibindo "Detalhes da Atualização".
        self.title_label = Label(
            text='Detalhes da Atualização',
            font_size=24,
            size_hint_y=None, # A altura não será baseada na proporção, mas sim no valor fixo 'height'.
            height=50,
            color=(0, 0, 0, 1), # Cor do texto preto.
            font_name='Roboto', # Define a fonte como Roboto.
            halign='center', # Alinhamento horizontal do texto ao centro.
            text_size=(None, None) # Permite que o texto se adapte à largura do widget (vinculado abaixo).
        )
        # Vincula a propriedade 'width' do Label à sua 'text_size' para que o texto quebre linhas se for muito longo.
        self.title_label.bind(width=lambda instance, value: setattr(instance, 'text_size', (instance.width, None)))
        main_layout.add_widget(self.title_label)

        # Layout para a imagem do serviço e seus detalhes, organizado horizontalmente.
        content_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=200, spacing=10)
        # Desenha um retângulo cinza claro como fundo para o content_layout.
        with content_layout.canvas.before:
            Color(0.98, 0.98, 0.98, 1)  # Cor cinza claro (quase branco).
            self.content_rect = Rectangle(size=content_layout.size, pos=content_layout.pos)
        # Vincula o redimensionamento e reposicionamento do retângulo ao tamanho e posição do content_layout.
        content_layout.bind(size=self._update_content_rect, pos=self._update_content_rect)

        # Widget de imagem para exibir a foto do serviço.
        self.service_image = Image(
            source='', # A fonte da imagem será definida dinamicamente.
            size_hint_x=0.3, # Ocupa 30% da largura do content_layout.
            size_hint_y=None, # Altura automática.
            height=180, # Altura fixa da imagem.
            fit_mode='contain' # Ajusta a imagem para caber dentro dos limites sem cortar.
        )
        content_layout.add_widget(self.service_image)

        # Layout para os detalhes textuais do serviço, organizado verticalmente.
        details_layout = BoxLayout(orientation='vertical', size_hint_x=0.7, padding=[5, 5, 5, 5], spacing=5)
        
        # Label para a descrição do serviço.
        self.desc_label = Label(
            text='', # Texto será definido dinamicamente.
            font_size=14,
            color=(0, 0, 0, 1), # Cor do texto preto.
            size_hint_y=None,
            height=80, # Altura fixa.
            halign='left', # Alinhamento horizontal à esquerda.
            valign='top', # Alinhamento vertical ao topo.
            text_size=(None, None) # Permite que o texto se adapte à largura do widget.
        )
        self.desc_label.bind(width=lambda instance, value: setattr(instance, 'text_size', (instance.width, None)))
        details_layout.add_widget(self.desc_label)

        # Label para o endereço do serviço.
        self.address_label = Label(
            text='', # Texto será definido dinamicamente.
            font_size=12,
            color=(0.5, 0.5, 0.5, 1), # Cor do texto cinza.
            size_hint_y=None,
            height=30,
            halign='left',
            valign='middle', # Alinhamento vertical ao meio.
            text_size=(None, None)
        )
        self.address_label.bind(width=lambda instance, value: setattr(instance, 'text_size', (instance.width, None)))
        details_layout.add_widget(self.address_label)

        # Label para exibir o status atual do serviço.
        self.status_label = Label(
            text='Status: ', # Texto inicial.
            font_size=12,
            color=(0.5, 0.5, 0.5, 1),
            size_hint_y=None,
            height=30,
            halign='left',
            valign='middle',
            text_size=(None, None)
        )
        self.status_label.bind(width=lambda instance, value: setattr(instance, 'text_size', (instance.width, None)))
        details_layout.add_widget(self.status_label)

        # Label para exibir a data do serviço.
        self.date_label = Label(
            text='', # Texto será definido dinamicamente.
            font_size=12,
            color=(0.5, 0.5, 0.5, 1),
            size_hint_y=None,
            height=30,
            halign='left',
            valign='middle',
            text_size=(None, None)
        )
        self.date_label.bind(width=lambda instance, value: setattr(instance, 'text_size', (instance.width, None)))
        details_layout.add_widget(self.date_label)

        content_layout.add_widget(details_layout) # Adiciona o layout de detalhes ao layout de conteúdo.
        main_layout.add_widget(content_layout) # Adiciona o layout de conteúdo ao layout principal.

        # Área para seleção de status (apenas visível/editável por administradores).
        status_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, spacing=10)
        status_label = Label(
            text='Andamento da Obra:',
            font_size=14,
            color=(0, 0, 0, 1),
            size_hint_x=0.3, # Ocupa 30% da largura do layout de status.
            halign='left',
            valign='middle',
            text_size=(None, None)
        )
        status_label.bind(width=lambda instance, value: setattr(instance, 'text_size', (instance.width, None)))
        status_layout.add_widget(status_label)

        # Spinner (menu suspenso) para selecionar o status do serviço.
        self.status_spinner = Spinner(
            text='Em análise', # Texto inicial do spinner.
            values=('Em análise', 'Em andamento', 'Concluída'), # Opções de status disponíveis.
            size_hint_x=0.7, # Ocupa 70% da largura do layout de status.
            font_size=14,
            disabled=not self.is_admin # Desabilita o spinner se o usuário não for administrador.
        )
        self.status_spinner.bind(text=self.update_status) # Vincula a mudança de texto no spinner ao método update_status.
        status_layout.add_widget(self.status_spinner)
        main_layout.add_widget(status_layout)

        # Label para indicar a seção de atualizações do administrador.
        admin_update_label = Label(
            text='Atualizações do Administrador',
            font_size=18,
            size_hint_y=None,
            height=40,
            color=(0, 0, 0, 1),
            halign='left',
            text_size=(None, None)
        )
        admin_update_label.bind(width=lambda instance, value: setattr(instance, 'text_size', (instance.width, None)))
        main_layout.add_widget(admin_update_label)

        # ScrollView para permitir a rolagem das atualizações antigas.
        self.admin_scroll = ScrollView(size_hint=(1, 0.3)) # Ocupa 100% da largura e 30% da altura restante.
        # BoxLayout vertical dentro do ScrollView para conter as atualizações.
        self.admin_updates_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None, # Altura adaptativa ao conteúdo.
            spacing=10,
            padding=[10, 10, 10, 10]
        )
        # Vincula a altura do layout à sua altura mínima, garantindo que o ScrollView funcione.
        self.admin_updates_layout.bind(minimum_height=self.admin_updates_layout.setter('height'))
        # Desenha um retângulo cinza claro como fundo para o layout de atualizações.
        with self.admin_updates_layout.canvas.before:
            Color(0.95, 0.95, 0.95, 1)  # Cor cinza mais escura.
            self.admin_updates_rect = Rectangle(size=self.admin_updates_layout.size, pos=self.admin_updates_layout.pos)
        # Vincula o redimensionamento e reposicionamento do retângulo ao tamanho e posição do layout.
        self.admin_updates_layout.bind(size=self._update_admin_updates_rect, pos=self._update_admin_updates_rect)
        self.admin_scroll.add_widget(self.admin_updates_layout)
        main_layout.add_widget(self.admin_scroll)

        # Campo de entrada de texto para o administrador digitar novas atualizações.
        self.admin_input = TextInput(
            hint_text='Digite uma nova atualização...', # Texto de dica.
            size_hint=(1, None),
            height=60,
            multiline=True, # Permite múltiplas linhas de texto.
            font_size=14
        )
        main_layout.add_widget(self.admin_input)

        # Botão para enviar a atualização digitada.
        submit_button = Button(
            text='Enviar Atualização',
            size_hint=(0.8, None), # Ocupa 80% da largura, com altura automática.
            height=50,
            background_color=(0.1, 0.7, 0.3, 1), # Cor de fundo verde.
            color=(1, 1, 1, 1), # Cor do texto branco.
            pos_hint={'center_x': 0.5} # Centraliza o botão horizontalmente.
        )
        submit_button.bind(on_press=self.submit_admin_update) # Vincula o clique ao método submit_admin_update.
        main_layout.add_widget(submit_button)

        # Botão para voltar para a tela de administração.
        back_button = Button(
            text='Voltar para Admin',
            size_hint=(0.8, None),
            height=50,
            background_color=(0.1, 0.7, 0.3, 1),
            color=(1, 1, 1, 1),
            pos_hint={'center_x': 0.5}
        )
        back_button.bind(on_press=self.go_to_admin) # Vincula o clique ao método go_to_admin.
        main_layout.add_widget(back_button)

        self.add_widget(main_layout) # Adiciona o layout principal à tela.

    def set_update_data(self, update):
        """
        Define os dados da atualização de serviço a serem exibidos na tela.
        Este método é chamado por outra tela (ex: a tela de listagem de serviços)
        para passar os dados do serviço selecionado.
        Carrega as atualizações históricas do arquivo JSON.

        Args:
            update (dict): Um dicionário contendo os dados do serviço.
        """
        self.update_data = update # Armazena os dados do serviço.
        self.title_label.text = update['title'] # Define o título do serviço.
        self.service_image.source = update['image'] # Define a imagem do serviço.
        self.desc_label.text = update['description'] # Define a descrição.
        self.address_label.text = f'Endereço: {update["address"]}' # Define o endereço.
        self.status_label.text = f'Status: {update["status"]}' # Define o status.
        self.date_label.text = f'Data: {update["date"]}' # Define a data.
        self.status_spinner.text = update['status'] # Define o texto inicial do spinner com o status atual.
        
        self.admin_updates_layout.clear_widgets() # Limpa as atualizações antigas antes de carregar novas.
        
        # Carrega todas as atualizações de serviços do arquivo JSON.
        try:
            with open(self.json_file, 'r') as f:
                all_updates = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # Se o arquivo não existir ou estiver vazio/corrompido, inicializa como um dicionário vazio.
            all_updates = {}
        
        # Garante que 'all_updates' seja um dicionário. Se não for (formato JSON antigo), reinicializa.
        if not isinstance(all_updates, dict):
            print(f"Erro: Formato inválido em {self.json_file}. Esperado dicionário, encontrado {type(all_updates)}.")
            all_updates = {}
        
        # Obtém os dados do serviço específico pelo seu título.
        service_data = all_updates.get(self.update_data['title'], {})
        
        # Se os dados do serviço forem uma lista (formato antigo), converte para o novo formato de dicionário.
        if isinstance(service_data, list):
            print(f"Convertendo formato antigo para {self.update_data['title']}.")
            service_data = {
                'id': self.update_data.get('id', '000AAA'), # Mantém o ID ou usa um padrão.
                'title': self.update_data['title'],
                'description': self.update_data.get('description', 'Descrição não disponível'),
                'date': self.update_data.get('date', '01/01/2023'),
                'address': self.update_data.get('address', 'Endereço não disponível'),
                'image': self.update_data.get('image', os.path.join('images', 'default.png')),
                'status': self.update_data.get('status', 'Em análise'),
                'type': self.update_data.get('type', 'Serviço Geral'),
                'last_update': self.update_data.get('last_update', '01/01/2023 00:00'),
                'updates': service_data # As antigas atualizações (lista) são colocadas sob a chave 'updates'.
            }
            all_updates[self.update_data['title']] = service_data # Atualiza no dicionário geral.
            # Salva a nova estrutura convertida de volta no arquivo JSON.
            with open(self.json_file, 'w') as f:
                json.dump(all_updates, f, indent=4)
        
        # Obtém a lista de atualizações para o serviço atual.
        service_updates = service_data.get('updates', [])
        
        # Tenta ordenar as atualizações por data, da mais recente para a mais antiga.
        try:
            service_updates.sort(
                key=lambda x: datetime.strptime(x['date'], '%d/%m/%Y %H:%M'), # Converte a string de data para um objeto datetime para ordenação.
                reverse=True # Ordem decrescente (mais recente primeiro).
            )
        except (KeyError, ValueError) as e:
            print(f"Erro ao ordenar atualizações: {e}") # Exibe erro se a chave 'date' estiver faltando ou o formato for inválido.
        
        # Exibe cada atualização no layout de atualizações do administrador.
        for update in service_updates:
            # Cria um layout vertical para cada atualização individual.
            update_layout = BoxLayout(
                orientation='vertical',
                size_hint_y=None,
                height=80, # Altura fixa para cada bloco de atualização.
                padding=[5, 5, 5, 5],
                spacing=5
            )
            # Desenha um fundo branco para cada bloco de atualização.
            with update_layout.canvas.before:
                Color(1, 1, 1, 1)  # Cor branca.
                update_layout.rect = Rectangle(size=update_layout.size, pos=update_layout.pos)
            # Vincula o retângulo ao tamanho/posição do layout de atualização.
            update_layout.bind(size=self._update_update_rect, pos=self._update_update_rect)

            # Label para o texto da atualização.
            update_label = Label(
                text=update['text'], # Texto da atualização.
                font_size=14,
                color=(0, 0, 0, 1),
                size_hint_y=None,
                height=40,
                halign='left',
                valign='top',
                text_size=(None, None)
            )
            update_label.bind(width=lambda instance, value: setattr(instance, 'text_size', (instance.width, None)))
            update_layout.add_widget(update_label)

            # Label para exibir o usuário e a data da atualização.
            meta_label = Label(
                text=f'Por: {update["user"]} em {update["date"]}', # Exibe usuário e data.
                font_size=12,
                color=(0.5, 0.5, 0.5, 1),
                size_hint_y=None,
                height=30,
                halign='left',
                valign='middle',
                text_size=(None, None)
            )
            meta_label.bind(width=lambda instance, value: setattr(instance, 'text_size', (instance.width, None)))
            update_layout.add_widget(meta_label)

            self.admin_updates_layout.add_widget(update_layout) # Adiciona o bloco de atualização ao layout principal de atualizações.

    def update_status(self, instance, value):
        """
        Atualiza o status do serviço quando o Spinner é modificado e salva no JSON.

        Args:
            instance: A instância do widget que disparou o evento (o Spinner).
            value (str): O novo valor do status selecionado.
        """
        if not self.is_admin: # Se o usuário não for administrador, não permite a alteração.
            return 
        
        self.update_data['status'] = value # Atualiza o status no objeto de dados do serviço.
        self.status_label.text = f'Status: {value}' # Atualiza o label de status na UI.
        
        # Salva o status atualizado no arquivo JSON.
        try:
            with open(self.json_file, 'r') as f:
                all_updates = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            all_updates = {} # Inicializa se o arquivo não existir ou estiver corrompido.
        
        # Garante que 'all_updates' seja um dicionário.
        if not isinstance(all_updates, dict):
            print(f"Erro: Formato inválido em {self.json_file}. Reinicializando.")
            all_updates = {}
        
        service_title = self.update_data['title']
        # Obtém os dados do serviço atual, ou um dicionário padrão se não existir.
        service_data = all_updates.get(service_title, {'updates': [], 'status': 'Em análise'})
        
        # Verifica e corrige o formato se 'service_data' for uma lista (formato antigo).
        if isinstance(service_data, list):
            print(f"Convertendo formato antigo para {service_title}.")
            service_data = {
                'id': self.update_data.get('id', '000AAA'),
                'title': service_title,
                'description': self.update_data.get('description', 'Descrição não disponível'),
                'date': self.update_data.get('date', '01/01/2023'),
                'address': self.update_data.get('address', 'Endereço não disponível'),
                'image': self.update_data.get('image', os.path.join('images', 'default.png')),
                'status': value, # O novo status já está aqui.
                'type': self.update_data.get('type', 'Serviço Geral'),
                'last_update': self.update_data.get('last_update', '01/01/2023 00:00'),
                'updates': service_data # As atualizações antigas (lista) são migradas.
            }
        
        service_data['status'] = value # Atualiza o status dentro dos dados do serviço.
        all_updates[service_title] = service_data # Atualiza o dicionário geral.
        
        # Salva todos os dados atualizados de volta no arquivo JSON.
        with open(self.json_file, 'w') as f:
            json.dump(all_updates, f, indent=4)
        
        # Tenta atualizar o status na lista de serviços da BlogScreen (se ela existir).
        if 'blog' in self.manager.screen_names:
            blog_screen = self.manager.get_screen('blog')
            for service in blog_screen.service_updates:
                if service['title'] == service_title:
                    service['status'] = value # Atualiza o status do serviço na lista interna da BlogScreen.
                    break
            blog_screen.update_posts(blog_screen.service_updates) # Força a BlogScreen a recarregar seus posts com o novo status.

    def submit_admin_update(self, instance):
        """
        Processa o envio de uma nova atualização do administrador.
        Adiciona a atualização à UI e salva no arquivo JSON, além de notificar usuários.
        """
        update_text = self.admin_input.text.strip() # Obtém o texto do campo de entrada, removendo espaços em branco.
        if update_text: # Verifica se o texto não está vazio.
            current_time = datetime.now().strftime('%d/%m/%Y %H:%M') # Obtém a data e hora atual formatada.
            
            # Cria um novo BoxLayout para exibir a nova atualização.
            update_layout = BoxLayout(
                orientation='vertical',
                size_hint_y=None,
                height=80,
                padding=[5, 5, 5, 5],
                spacing=5
            )
            with update_layout.canvas.before:
                Color(1, 1, 1, 1)  # Fundo branco.
                update_layout.rect = Rectangle(size=update_layout.size, pos=update_layout.pos)
            update_layout.bind(size=self._update_update_rect, pos=self._update_update_rect)

            update_label = Label(
                text=update_text,
                font_size=14,
                color=(0, 0, 0, 1),
                size_hint_y=None,
                height=40,
                halign='left',
                valign='top',
                text_size=(None, None)
            )
            update_label.bind(width=lambda instance, value: setattr(instance, 'text_size', (instance.width, None)))
            update_layout.add_widget(update_label)

            meta_label = Label(
                text=f'Por: {self.current_user} em {current_time}',
                font_size=12,
                color=(0.5, 0.5, 0.5, 1),
                size_hint_y=None,
                height=30,
                halign='left',
                valign='middle',
                text_size=(None, None)
            )
            meta_label.bind(width=lambda instance, value: setattr(instance, 'text_size', (instance.width, None)))
            update_layout.add_widget(meta_label)

            self.admin_updates_layout.add_widget(update_layout, index=0) # Adiciona a nova atualização no topo da lista.
            
            # Salva a nova atualização no arquivo JSON.
            try:
                with open(self.json_file, 'r') as f:
                    all_updates = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                all_updates = {}
            
            # Garante que 'all_updates' seja um dicionário.
            if not isinstance(all_updates, dict):
                print(f"Erro: Formato inválido em {self.json_file}. Reinicializando.")
                all_updates = {}
            
            service_title = self.update_data['title']
            # Obtém os dados do serviço atual.
            service_data = all_updates.get(service_title, {'updates': [], 'status': 'Em análise'})
            
            # Verifica e corrige o formato se 'service_data' for uma lista (formato antigo).
            if isinstance(service_data, list):
                print(f"Convertendo formato antigo para {service_title}.")
                service_data = {
                    'id': self.update_data.get('id', '000AAA'),
                    'title': service_title,
                    'description': self.update_data.get('description', 'Descrição não disponível'),
                    'date': self.update_data.get('date', '01/01/2023'),
                    'address': self.update_data.get('address', 'Endereço não disponível'),
                    'image': self.update_data.get('image', os.path.join('images', 'default.png')),
                    'status': self.update_data.get('status', 'Em análise'),
                    'type': self.update_data.get('type', 'Serviço Geral'),
                    'last_update': self.update_data.get('last_update', '01/01/2023 00:00'),
                    'updates': service_data
                }
            
            # Garante que a chave 'updates' exista nos dados do serviço.
            if 'updates' not in service_data:
                service_data['updates'] = []
            
            # Adiciona a nova atualização à lista de atualizações do serviço.
            service_data['updates'].append({
                'id': self.update_data.get('id', '000AAA'), # Inclui o ID do serviço na atualização.
                'text': update_text,
                'user': self.current_user,
                'date': current_time
            })
            
            service_data['last_update'] = current_time # Atualiza a data da última atualização do serviço.
            
            # Reordena as atualizações (mais recentes primeiro).
            try:
                service_data['updates'].sort(
                    key=lambda x: datetime.strptime(x['date'], '%d/%m/%Y %H:%M'),
                    reverse=True
                )
            except (KeyError, ValueError) as e:
                print(f"Erro ao ordenar atualizações: {e}")
            
            all_updates[service_title] = service_data # Atualiza o dicionário geral de todos os serviços.
            
            # Salva o dicionário de todos os serviços de volta no arquivo JSON.
            with open(self.json_file, 'w') as f:
                json.dump(all_updates, f, indent=4)
            
            # Atualiza a BlogScreen com a nova data de última atualização.
            if 'blog' in self.manager.screen_names:
                blog_screen = self.manager.get_screen('blog')
                for service in blog_screen.service_updates:
                    if service['title'] == service_title:
                        service['last_update'] = current_time # Atualiza o 'last_update' na lista da BlogScreen.
                        break
                blog_screen.update_posts(blog_screen.service_updates) # Força a BlogScreen a recarregar.
            
            # Envia notificação para usuários que estão "seguindo" este serviço.
            app = App.get_running_app()
            service_id = self.current_service_id() # Obtém o ID do serviço atual.
            usuarios = carregar_todos_usuarios() # Carrega todos os usuários do arquivo.
            for user in usuarios:
                if "seguindo" in user and service_id in user["seguindo"]: # Verifica se o usuário segue o serviço.
                    if "notificacoes" not in user:
                        user["notificacoes"] = [] # Cria a lista de notificações se não existir.
                    user["notificacoes"].append({ # Adiciona uma nova notificação.
                        "title": self.title_label.text,
                        "description": self.desc_label.text,
                        "address": self.address_label.text,
                        "status": self.status_spinner.text,
                        "date": current_time,
                        "image": self.service_image.source
                    })
            salvar_todos_usuarios(usuarios) # Salva os usuários com as novas notificações.
            
            self.admin_input.text = '' # Limpa o campo de entrada de texto após o envio.

    def current_service_id(self):
        """
        Retorna o ID do serviço atual que está sendo exibido.
        Retorna um ID padrão se os dados do serviço não estiverem definidos ou não contiverem um ID.
        """
        if self.update_data and 'id' in self.update_data:
            return self.update_data['id']
        return '000AAA' # ID padrão para casos onde o ID não está disponível.

    def go_to_admin(self, instance):
        """
        Navega de volta para a tela de administração.
        """
        if 'admin' in self.manager.screen_names: # Verifica se a tela 'admin' está registrada no ScreenManager.
            self.manager.current = 'admin' # Define a tela atual como 'admin'.
        else:
            print("Erro: tela 'admin' não encontrada") # Loga um erro se a tela não for encontrada.

    # Métodos auxiliares para atualizar a posição e o tamanho dos retângulos de fundo.
    # São chamados quando os layouts vinculados mudam de tamanho ou posição, garantindo que o fundo se ajuste.
    def _update_content_rect(self, instance, value):
        self.content_rect.pos = instance.pos
        self.content_rect.size = instance.size

    def _update_admin_updates_rect(self, instance, value):
        self.admin_updates_rect.pos = instance.pos
        self.admin_updates_rect.size = instance.size

    def _update_update_rect(self, instance, value):
        instance.rect.pos = instance.pos
        instance.rect.size = instance.size

def carregar_todos_usuarios():
    """
    Carrega todos os dados de usuários do arquivo 'usuarios.json'.
    Retorna uma lista de dicionários, cada um representando um usuário.
    Lida com casos de arquivo não encontrado ou JSON inválido.
    """
    try:
        with open("usuarios.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return [] # Retorna uma lista vazia se o arquivo não existir ou estiver corrompido.

def salvar_todos_usuarios(usuarios):
    """
    Salva a lista de dados de usuários no arquivo 'usuarios.json'.
    Usa codificação UTF-8 e formatação indentada para legibilidade.
    """
    with open("usuarios.json", "w", encoding="utf-8") as f:
        json.dump(usuarios, f, ensure_ascii=False, indent=4) # 'ensure_ascii=False' permite caracteres não-ASCII (como acentos) no JSON.