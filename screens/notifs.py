from kivy.uix.screenmanager import Screen # Importa a classe Screen do módulo kivy.uix.screenmanager, que permite criar múltiplas telas e alternar entre elas.
from kivy.uix.boxlayout import BoxLayout # Importa BoxLayout do módulo kivy.uix.boxlayout, um layout que organiza os widgets em uma única linha, seja horizontalmente ou verticalmente.
from kivy.uix.gridlayout import GridLayout # Importa GridLayout do módulo kivy.uix.gridlayout, um layout que organiza os widgets em uma grade de linhas e colunas.
from kivy.uix.label import Label # Importa Label do módulo kivy.uix.label, usado para exibir texto estático na interface do usuário.
from kivy.uix.button import Button # Importa Button do módulo kivy.uix.button, um widget que permite a interação do usuário através de cliques.
from kivy.uix.scrollview import ScrollView # Importa ScrollView do módulo kivy.uix.scrollview, que permite rolar o conteúdo de um widget quando ele excede o tamanho disponível na tela.
from kivy.uix.image import Image # Importa Image do módulo kivy.uix.image, usado para exibir imagens na interface.
from kivy.graphics import Color, Rectangle # Importa Color e Rectangle do módulo kivy.graphics. Color é usado para definir a cor de elementos gráficos e Rectangle para desenhar retângulos.
from kivy.uix.widget import Widget # Importa Widget do módulo kivy.uix.widget, a classe base para todos os elementos visuais na Kivy. Usado aqui como um espaçador flexível.
from kivy.uix.spinner import Spinner # Importa Spinner do módulo kivy.uix.spinner, um widget de lista suspensa para seleção de opções.
from kivy.uix.textinput import TextInput # Importa TextInput do módulo kivy.uix.textinput, um campo de entrada de texto onde o usuário pode digitar.
from kivy.app import App # Importa App do módulo kivy.app, a classe principal para qualquer aplicação Kivy.
from kivy.uix.popup import Popup # Importa Popup do módulo kivy.uix.popup, uma pequena janela flutuante usada para exibir mensagens ou solicitar entradas.
import json # Importa o módulo json, para trabalhar com dados no formato JSON (serialização e desserialização).
import datetime # Importa o módulo datetime, para trabalhar com datas e horas.
import sys # Importa o módulo sys, que fornece acesso a parâmetros e funções específicas do sistema. Usado para identificar se o aplicativo está rodando via PyInstaller.
import os # Importa o módulo os, que fornece funções para interagir com o sistema operacional, como manipulação de caminhos de arquivo.

def resource_path(relative_path):
    """
    Retorna o caminho absoluto para recursos (imagens, etc.) quando o aplicativo é empacotado com PyInstaller.
    Se não estiver rodando como um executável PyInstaller, retorna o caminho relativo ao diretório atual do script.
    Isso garante que os recursos sejam encontrados tanto em desenvolvimento quanto no aplicativo compilado.
    """
    if hasattr(sys, '_MEIPASS'): # Verifica se o aplicativo está sendo executado como um executável PyInstaller. '_MEIPASS' é um atributo adicionado pelo PyInstaller.
        return os.path.join(sys._MEIPASS, relative_path) # Se sim, retorna o caminho dentro do diretório temporário criado pelo PyInstaller.
    return os.path.join(os.path.abspath("."), relative_path) # Caso contrário, retorna o caminho relativo ao diretório onde o script está sendo executado.

class NotifsScreen(Screen):
    """
    Representa a tela de Notificações no aplicativo.
    Esta tela exibe atualizações e informações sobre os serviços que o usuário está seguindo.
    """
    def __init__(self, **kwargs):
        """
        Inicializa a tela de Notificações, configurando seu layout e componentes visuais.
        """
        super().__init__(**kwargs) # Chama o construtor da classe base Screen.

        # Layout principal da tela, organizado horizontalmente. Ele dividirá a tela em uma barra lateral e uma área de conteúdo principal.
        main_layout = BoxLayout(orientation='horizontal', spacing=10)

        # Barra lateral esquerda: Um BoxLayout vertical, que ocupará 10% da largura da tela. Contém botões de navegação e o logo.
        left_layout = BoxLayout(orientation='vertical', size_hint_x=0.1, padding=10, spacing=10)
        # Área da direita: Um GridLayout com 1 coluna e 2 linhas. Ocupará 90% da largura. A linha superior será para informações do usuário e a inferior para o conteúdo principal.
        right_layout = GridLayout(cols=1, rows=2, size_hint_x=0.9, padding=10, spacing=10)

        # Adiciona os layouts esquerdo e direito ao layout principal.
        main_layout.add_widget(left_layout)
        main_layout.add_widget(right_layout)
        # Adiciona o layout principal à própria tela de Notificações.
        self.add_widget(main_layout)

        # Configuração do fundo para o `left_layout` (barra lateral).
        # Usa `canvas.before` para desenhar um retângulo antes dos widgets serem desenhados, servindo como fundo.
        with left_layout.canvas.before:
            Color(0.9, 0.9, 0.9, 1) # Define a cor do fundo como cinza claro (RGB + Alpha).
            self.left_rect = Rectangle(size=left_layout.size, pos=left_layout.pos) # Cria um retângulo com o tamanho e posição iniciais do left_layout.
        # Vincula os eventos de `size` (tamanho) e `pos` (posição) do `left_layout` para atualizar o retângulo de fundo.
        left_layout.bind(size=self._update_left_rect, pos=self._update_left_rect)

        # Configuração do fundo para o `right_layout` (área de conteúdo principal).
        with right_layout.canvas.before:
            Color(1, 1, 1, 1) # Define a cor do fundo como branco.
            self.right_rect = Rectangle(size=right_layout.size, pos=right_layout.pos) # Cria um retângulo com o tamanho e posição iniciais do right_layout.
        # Vincula os eventos de `size` e `pos` do `right_layout` para atualizar o retângulo de fundo.
        right_layout.bind(size=self._update_right_rect, pos=self._update_right_rect)

        # ==================== Conteúdo da Barra Lateral Esquerda ====================
        # Título da barra lateral.
        title = Label(
            text='Notificações', # Texto exibido.
            font_size=22, # Tamanho da fonte.
            size_hint=(1, None), # Ocupa 100% da largura disponível na barra lateral, altura é fixa.
            height=60, # Altura fixa do label.
            color=(0, 0, 0, 1), # Cor do texto preta.
            font_name='Roboto' # Fonte utilizada (assumindo que 'Roboto' esteja disponível).
        )
        left_layout.add_widget(title) # Adiciona o título à barra lateral.

        # Logo da aplicação.
        logo = Image(
            source=resource_path(os.path.join('resources', 'logo.png')), # Caminho da imagem do logo, usando `resource_path` para compatibilidade com PyInstaller.
            size_hint=(1, None), # Ocupa 100% da largura, altura é fixa.
            height=120, # Altura fixa da imagem.
            fit_mode='contain' # A imagem será redimensionada para caber dentro de suas proporções, sem cortar.
        )
        left_layout.add_widget(logo) # Adiciona o logo à barra lateral.
        
        left_layout.add_widget(Widget()) # Adiciona um Widget genérico que atua como um "espaçador" flexível. Ele se expandirá para preencher o espaço vertical disponível, empurrando os botões de navegação para a parte inferior da barra lateral.

        # Lista de botões de navegação na barra lateral. Cada tupla contém o texto do botão e a função de callback associada.
        buttons = [
            ('Ir para Landing', self.go_to_landing), # Navega para a tela "Landing".
            ('Ir para lista de Serviços', self.go_to_blog), # Navega para a tela "Blog" (que lista serviços/posts).
            ('Ir para Notificações', self.go_to_notifs), # Navega para a própria tela de Notificações (exibirá um popup de aviso).
            ('Solicitar Serviço', self.go_to_services), # Navega para a tela "Services" (onde o usuário pode solicitar um novo serviço).
            ('Sair', self.go_to_login) # Navega para a tela "Login" (efetivamente "saindo" do aplicativo ou da sessão atual).
        ]
        # Loop para criar e adicionar cada botão à barra lateral.
        for text, callback in buttons:
            btn = Button(
                text=text, # Texto do botão.
                size_hint=(1, 0.5), # Ocupa 100% da largura da barra lateral, e 50% do espaço vertical disponível para os botões.
                background_color=(0.1, 0.7, 0.3, 1), # Cor de fundo do botão (verde).
                color=(1, 1, 1, 1) # Cor do texto do botão (branco).
            )
            btn.bind(on_press=callback) # Associa a função de callback ao evento de clique do botão.
            left_layout.add_widget(btn) # Adiciona o botão à barra lateral.

        # ==================== Barra Superior na Área Direita (informações do usuário) ====================
        top_bar = BoxLayout(
            orientation='horizontal', # Organiza os widgets horizontalmente.
            size_hint_y=None, # Altura fixa.
            height=80, # Altura da barra superior.
            padding=10, # Preenchimento interno.
            spacing=10 # Espaçamento entre os widgets.
        )

        top_bar.add_widget(Widget(size_hint_x=1)) # Adiciona um Widget flexível que empurra o `user_label` e `profile_pic` para a direita.
        
        self.user_label = Label(
            text=f'', # Texto inicial vazio, será preenchido dinamicamente com o nome do usuário.
            font_size=20, # Tamanho da fonte.
            color=(0, 0, 0, 1), # Cor do texto preta.
            size_hint=(None, None), # Tamanho fixo para o label.
            size=(200, 60), # Largura e altura fixas.
            halign='right', # Alinhamento horizontal do texto à direita.
            valign='middle' # Alinhamento vertical do texto ao meio.
        )
        self.user_label.bind(size=self.user_label.setter('text_size')) # Garante que o texto se adapte ao tamanho do label.
        top_bar.add_widget(self.user_label) # Adiciona o label do usuário à barra superior.

        profile_pic = Image(
            source=resource_path(os.path.join('resources', 'logo.png')), # Imagem do perfil (atualmente usa o logo).
            size_hint=(None, None), # Tamanho fixo para a imagem.
            size=(60, 60), # Largura e altura fixas.
            fit_mode='contain' # A imagem será redimensionada para caber sem cortar.
        )
        profile_pic.bind(on_touch_down=self._on_profile_pic_touch) # Vincula um evento de toque à imagem do perfil para navegação.
        top_bar.add_widget(profile_pic) # Adiciona a imagem do perfil à barra superior.
        self.profile_pic = profile_pic # Armazena uma referência à imagem do perfil para uso posterior, se necessário.

        right_layout.add_widget(top_bar) # Adiciona a barra superior (com info do usuário) à primeira linha do `right_layout`.

        # ==================== Conteúdo Principal da Área Direita (lista de notificações) ====================
        right_content = BoxLayout(orientation='vertical', spacing=10, padding=10) # Layout vertical para o conteúdo principal.

        # Título da seção de notificações.
        title = Label(
            text='Notificações dos Serviços que você segue', # Texto do título.
            font_size=24, # Tamanho da fonte.
            size_hint_y=None, # Altura fixa.
            height=50, # Altura do label.
            color=(0, 0, 0, 1), # Cor do texto preta.
            font_name='Roboto', # Fonte.
            halign='center', # Alinhamento horizontal centralizado.
            text_size=(None, None) # O texto se ajustará ao tamanho do label.
        )
        right_content.add_widget(title) # Adiciona o título ao conteúdo da direita.

        # ScrollView para a lista de notificações, permitindo rolagem se houver muitas.
        self.scroll = ScrollView(size_hint=(1, 1)) # Ocupa todo o espaço restante no `right_content`.
        self.notif_layout = BoxLayout(
            orientation='vertical', # Organiza as notificações verticalmente.
            size_hint_y=None, # A altura será ajustada automaticamente com base no conteúdo (`minimum_height`).
            spacing=15, # Espaçamento entre as notificações individuais.
            padding=[10, 10, 10, 10] # Preenchimento interno do layout.
        )
        # Vincula o `minimum_height` do `notif_layout` à sua própria `height`, fazendo com que ele se expanda para conter todos os widgets filhos.
        self.notif_layout.bind(minimum_height=self.notif_layout.setter('height'))

        # Desenha um fundo cinza claro para o `notif_layout`.
        with self.notif_layout.canvas.before:
            Color(0.95, 0.95, 0.95, 1) # Cor cinza bem claro.
            self.notif_rect = Rectangle(size=self.notif_layout.size, pos=self.notif_layout.pos) # Cria o retângulo de fundo.
        # Vincula os eventos de `size` e `pos` do `notif_layout` para atualizar o retângulo de fundo.
        self.notif_layout.bind(size=self._update_notif_rect, pos=self._update_notif_rect)

        self.scroll.add_widget(self.notif_layout) # Adiciona o `notif_layout` (onde as notificações são colocadas) ao ScrollView.
        right_content.add_widget(self.scroll) # Adiciona o ScrollView ao conteúdo da direita.

        right_layout.add_widget(right_content) # Adiciona o `right_content` (que inclui o título e o ScrollView de notificações) à segunda linha do `right_layout`.

    def on_pre_enter(self, *args):
        """
        Este método é chamado automaticamente pelo ScreenManager pouco antes da tela se tornar a tela atual.
        Ele é usado para carregar e exibir as notificações relevantes para o usuário logado.
        """
        app = App.get_running_app()
        usuario_nome = "Usuário"
        if hasattr(app, "usuario_logado") and app.usuario_logado:
            usuario_nome = app.usuario_logado.get("username", "Usuário")
        self.user_label.text = f'{usuario_nome}'

        self.notif_posts = []
        if app.usuario_logado and "seguindo" in app.usuario_logado:
            try:
                with open("services_updates.json", "r", encoding="utf-8") as f:
                    all_services = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                all_services = {}

            for service in all_services.values():
                service_id = service.get("id")
                if service_id and service_id in app.usuario_logado["seguindo"]:
                    updates = service.get("updates", [])
                    for update in updates:
                        # Adiciona também o campo 'cep' e 'solicitante' se existirem
                        self.notif_posts.append({
                            "id": service_id,
                            "title": service.get("title", ""),
                            "text": update.get("text", ""),
                            "date": update.get("date", ""),
                            "cep": service.get("cep", "Não informado"),
                            "solicitante": service.get("solicitante", "Não informado")
                        })

        def parse_date(d):
            try:
                return datetime.datetime.strptime(d, "%d/%m/%Y %H:%M")
            except Exception:
                return datetime.datetime.min
        self.notif_posts.sort(key=lambda x: parse_date(x.get("date", "")), reverse=True)
        self.update_notifs(self.notif_posts)

    def update_notifs(self, notif_posts):
        """
        Atualiza o layout que exibe as notificações, removendo as antigas e adicionando as novas.
        Agora exibe também o CEP e o solicitante, se existirem.
        """
        self.notif_layout.clear_widgets()
        if not notif_posts:
            if not any(isinstance(child, Label) and "aparecerão aqui" in child.text for child in self.notif_layout.children):
                self.notif_layout.add_widget(Label(
                    text="As notificações dos serviços que você segue aparecerão aqui.",
                    font_size=16,
                    color=(0.5, 0.5, 0.5, 1),
                    size_hint_y=None,
                    height=40
                ))
            return

        for notif in notif_posts:
            post = BoxLayout(
                orientation='vertical',
                size_hint_y=None,
                height=100,
                padding=[10, 5, 10, 5],
                spacing=5
            )
            with post.canvas.before:
                Color(1, 1, 1, 1)
                post.post_rect = Rectangle(size=post.size, pos=post.pos)
            post.bind(size=self._update_post_rect, pos=self._update_post_rect)

            # Linha principal: ID, Título, Data
            top_row = BoxLayout(orientation='horizontal', size_hint_y=None, height=30, spacing=10)
            id_label = Label(
                text=f'ID: {notif.get("id", "")}',
                font_size=12,
                color=(0, 0, 0, 1),
                size_hint_x=0.2,
                halign='left',
                valign='middle'
            )
            title_label = Label(
                text=f'Título: {notif.get("title", "")}',
                font_size=14,
                color=(0, 0, 0, 1),
                size_hint_x=0.5,
                halign='left',
                valign='middle'
            )
            date_label = Label(
                text=f'Data: {notif.get("date", "")}',
                font_size=12,
                color=(0.5, 0.5, 0.5, 1),
                size_hint_x=0.3,
                halign='left',
                valign='middle'
            )
            for lbl in [id_label, title_label, date_label]:
                lbl.bind(size=lbl.setter('text_size'))
                top_row.add_widget(lbl)
            post.add_widget(top_row)

            # Linha de atualização
            update_label = Label(
                text=f'Atualização: {notif.get("text", "")}',
                font_size=12,
                color=(0, 0, 0, 1),
                size_hint_y=None,
                height=25,
                halign='left',
                valign='middle'
            )
            update_label.bind(size=update_label.setter('text_size'))
            post.add_widget(update_label)

            # Linha de CEP e Solicitante (se existirem)
            info_row = BoxLayout(orientation='horizontal', size_hint_y=None, height=25, spacing=10)
            cep_label = Label(
                text=f'CEP: {notif.get("cep", "Não informado")}',
                font_size=12,
                color=(0.3, 0.3, 0.3, 1),
                size_hint_x=0.5,
                halign='left',
                valign='middle'
            )
            solicitante_label = Label(
                text=f'Solicitante: {notif.get("solicitante", "Não informado")}',
                font_size=12,
                color=(0.3, 0.3, 0.3, 1),
                size_hint_x=0.5,
                halign='left',
                valign='middle'
            )
            for lbl in [cep_label, solicitante_label]:
                lbl.bind(size=lbl.setter('text_size'))
                info_row.add_widget(lbl)
            post.add_widget(info_row)

            self.notif_layout.add_widget(post) # Adiciona o `post` (o "card" de notificação) ao `notif_layout` principal.

    def _update_left_rect(self, instance, value):
        """
        Callback para atualizar a posição e o tamanho do retângulo de fundo do left_layout
        sempre que o left_layout mudar de tamanho ou posição.
        """
        self.left_rect.pos = instance.pos
        self.left_rect.size = instance.size

    def _update_right_rect(self, instance, value):
        """
        Callback para atualizar a posição e o tamanho do retângulo de fundo do right_layout
        sempre que o right_layout mudar de tamanho ou posição.
        """
        self.right_rect.pos = instance.pos
        self.right_rect.size = instance.size

    def _update_notif_rect(self, instance, value):
        """
        Callback para atualizar a posição e o tamanho do retângulo de fundo do notif_layout
        sempre que o notif_layout mudar de tamanho ou posição.
        """
        self.notif_rect.pos = instance.pos
        self.notif_rect.size = instance.size

    def _update_post_rect(self, instance, value):
        """
        Callback para atualizar a posição e o tamanho do retângulo de fundo de um post de notificação individual
        sempre que o post mudar de tamanho ou posição.
        """
        instance.post_rect.pos = instance.pos
        instance.post_rect.size = instance.size

    # ==================== Métodos de Navegação ====================
    # Estes métodos são responsáveis por alternar a tela atual no ScreenManager.
    # Cada método verifica se a tela de destino existe no `self.manager.screen_names` antes de tentar mudar,
    # para evitar erros se uma tela não estiver registrada.

    def go_to_landing(self, instance):
        """Navega para a tela 'landing'."""
        if 'landing' in self.manager.screen_names: # Verifica se a tela 'landing' está registrada no ScreenManager.
            self.manager.current = 'landing' # Define a tela 'landing' como a tela atual.
        else:
            print("Erro: tela 'landing' não encontrada") # Imprime um erro se a tela não for encontrada.
    
    def go_to_perfil(self, instance):
        """Navega para a tela 'perfil'."""
        if 'perfil' in self.manager.screen_names:
            self.manager.current = 'perfil'
        else:
            print("Erro: tela 'perfil' não encontrada")

    def go_to_blog(self, instance):
        """Navega para a tela 'blog' (que provavelmente lista os serviços ou posts)."""
        if 'blog' in self.manager.screen_names:
            self.manager.current = 'blog'
        else:
            print("Erro: tela 'blog' não encontrada")

    def go_to_services(self, instance):
        """Navega para a tela 'services' (onde o usuário pode solicitar um novo serviço)."""
        if 'services' in self.manager.screen_names:
            self.manager.current = 'services'
        else:
            print("Erro: tela 'services' não encontrada")

    def go_to_notifs(self, instance):
        """
        Este método é chamado quando o botão 'Ir para Notificações' é clicado.
        Como o usuário já está nesta tela, um Popup de aviso é exibido.
        """
        popup = Popup(
            title='Aviso', # Título do popup.
            content=Label(text='Você já está na tela de notificações.'), # Mensagem exibida no popup.
            size_hint=(None, None), # Tamanho fixo para o popup.
            size=(350, 180) # Largura e altura do popup.
        )
        popup.open() # Abre o popup.

    def go_to_login(self, instance):
        """Navega para a tela 'login' (usada para sair ou fazer logout)."""
        if 'login' in self.manager.screen_names:
            self.manager.current = 'login'
        else:
            print("Erro: tela 'login' não encontrada")

    def _on_profile_pic_touch(self, instance, touch):
        """
        Manipula o evento de toque na imagem de perfil.
        Se a imagem for tocada, navega para a tela 'perfil'.
        """
        if instance.collide_point(*touch.pos): # Verifica se as coordenadas do toque (`touch.pos`) estão dentro da área da imagem (`instance`).
            if 'perfil' in self.manager.screen_names:
                self.manager.current = 'perfil'
            else:
                print("Erro: tela 'perfil' não encontrada")