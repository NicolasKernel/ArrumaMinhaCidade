from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.app import App
import os
import json
import sys

# Função utilitária para lidar com caminhos de recursos em aplicativos empacotados com PyInstaller.
# Isso garante que imagens e outros arquivos sejam encontrados corretamente.
def resource_path(relative_path):
    """Retorna o caminho absoluto para uso com PyInstaller."""
    if hasattr(sys, '_MEIPASS'):
        # Se o aplicativo estiver sendo executado como um executável PyInstaller,
        # _MEIPASS aponta para a pasta temporária onde os recursos são extraídos.
        return os.path.join(sys._MEIPASS, relative_path)
    # Caso contrário (se estiver executando o script Python diretamente),
    # assume que os recursos estão no diretório de trabalho atual.
    return os.path.join(os.path.abspath("."), relative_path)

# A classe AdminScreen herda de Screen, que é uma das telas gerenciadas pelo ScreenManager do Kivy.
class AdminScreen(Screen):
    # O método __init__ é o construtor da classe, chamado quando uma instância de AdminScreen é criada.
    def __init__(self, **kwargs):
        # Chama o construtor da classe base (Screen).
        super().__init__(**kwargs)
        # Define os nomes dos arquivos JSON que armazenarão os dados de usuários e atualizações de serviço.
        self.users_json = "usuarios.json"
        self.services_updates_json = "services_updates.json" # Caminho para o JSON de serviços

        # ==================== Configuração de Layouts Principais ====================
        # O layout principal organiza a tela horizontalmente.
        main_layout = BoxLayout(orientation='horizontal', spacing=10)

        # O layout da esquerda ocupa 25% da largura e organiza seus widgets verticalmente.
        left_layout = BoxLayout(orientation='vertical', size_hint_x=0.25, padding=10, spacing=10)
        # O layout da direita ocupa 75% da largura e é um GridLayout com 1 coluna e 2 linhas (barra superior e conteúdo).
        right_layout = GridLayout(cols=1, rows=2, size_hint_x=0.75, padding=10, spacing=10)

        # Adiciona os layouts esquerdo e direito ao layout principal.
        main_layout.add_widget(left_layout)
        main_layout.add_widget(right_layout)

        # Adiciona o layout principal (que contém todos os outros) à tela AdminScreen.
        self.add_widget(main_layout)

        # ==================== Estilização de Fundo dos Layouts ====================
        # Desenha um retângulo cinza claro como fundo para o layout da esquerda.
        with left_layout.canvas.before:
            Color(0.9, 0.9, 0.9, 1) # Cor cinza claro (R, G, B, Alpha)
            self.left_rect = Rectangle(size=left_layout.size, pos=left_layout.pos)
        # Vincula o tamanho e a posição do retângulo ao tamanho e posição do left_layout,
        # garantindo que o fundo se ajuste se o layout mudar.
        left_layout.bind(size=self._update_left_rect, pos=self._update_left_rect)

        # Desenha um retângulo branco como fundo para o layout da direita.
        with right_layout.canvas.before:
            Color(1, 1, 1, 1) # Cor branca
            self.right_rect = Rectangle(size=right_layout.size, pos=right_layout.pos)
        # Vincula o tamanho e a posição do retângulo ao tamanho e posição do right_layout.
        right_layout.bind(size=self._update_right_rect, pos=self._update_right_rect)

        # ==================== Layout da Esquerda: Conteúdo ====================
        # Título do painel do administrador.
        title = Label(
            text='Painel do Administrador',
            font_size=24,
            size_hint=(1, 0.2), # Ocupa a largura total, 20% da altura disponível.
            color=(0, 0, 0, 1), # Texto preto
            font_name='Roboto' # Fonte Roboto
        )
        left_layout.add_widget(title)

        # Imagem de logo.
        logo = Image(
            # Usa resource_path para encontrar a imagem de forma robusta.
            source=resource_path(os.path.join('resources', 'logo.png')),
            size_hint=(1, None), # Ocupa a largura total, altura fixa.
            height=300,
            fit_mode='contain' # Ajusta a imagem para caber na área, mantendo a proporção.
        )
        left_layout.add_widget(logo)

        # Lista de botões para o layout da esquerda (apenas "Voltar à Login" no momento).
        buttons = [
            ('Voltar à Login', self.go_to_login),
        ]
        # Cria e adiciona cada botão ao layout da esquerda.
        for text, callback in buttons:
            btn = Button(
                text=text,
                size_hint=(1, 0.2), # Ocupa a largura total, 20% da altura disponível.
                background_color=(0.1, 0.7, 0.3, 1), # Cor de fundo verde
                color=(1, 1, 1, 1) # Texto branco
            )
            btn.bind(on_press=callback) # Associa a função de callback ao evento de pressionar o botão.
            left_layout.add_widget(btn)

        # ==================== Layout da Direita: Barra Superior ====================
        # Barra superior para exibir informações do administrador.
        top_bar = BoxLayout(
            orientation='horizontal', # Layout horizontal
            size_hint_y=None, # Altura fixa
            height=80,
            padding=10,
            spacing=10
        )

        # Adiciona um widget flexível para empurrar o conteúdo para a direita.
        top_bar.add_widget(Widget(size_hint_x=1))

        # Recupera o nome de usuário do administrador logado.
        admin_nome = "Administrador"
        app = App.get_running_app() # Obtém a instância atual do aplicativo Kivy.
        if hasattr(app, "usuario_logado") and app.usuario_logado:
            # Se um usuário estiver logado e a informação estiver disponível, usa o nome do usuário.
            admin_nome = app.usuario_logado.get("username", "Administrador")
        # Rótulo para exibir o nome do administrador.
        self.admin_label = Label(
            text=f'Admin: {admin_nome}',
            font_size=20,
            color=(0, 0, 0, 1), # Texto preto
            size_hint=(None, None), # Tamanho fixo
            size=(200, 60),
            halign='right', # Alinhamento horizontal à direita
            valign='middle' # Alinhamento vertical ao meio
        )
        # Vincula o tamanho do rótulo para ajustar o tamanho do texto.
        self.admin_label.bind(size=self.admin_label.setter('text_size'))
        top_bar.add_widget(self.admin_label)

        # Imagem de perfil (atualmente usa a mesma logo).
        profile_pic = Image(
            source=resource_path(os.path.join('resources', 'logo.png')),
            size_hint=(None, None),
            size=(60, 60),
            fit_mode='contain'
        )
        top_bar.add_widget(profile_pic)

        # Adiciona a barra superior ao layout da direita.
        right_layout.add_widget(top_bar)

        # ==================== Layout da Direita: Conteúdo Principal ====================
        # Layout para o conteúdo principal da área direita.
        right_content = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # Lista de botões de administração e suas respectivas funções.
        admin_buttons = [
            ('Alterar Dados do Usuário', self.show_edit_user_form),
            ('Excluir Solicitação', self.show_delete_request_form),
            ('Listar Usuários/Solicitações', self.list_users_requests),
            ('Atualizar Serviço', self.show_update_service_form) 
        ]
        # Cria e adiciona cada botão de administração.
        for text, callback in admin_buttons:
            btn = Button(
                text=text,
                size_hint=(1, None), # Ocupa a largura total, altura fixa.
                height=50,
                background_color=(1, 0.4, 0.4, 1), # Cor de fundo vermelho claro
                color=(1, 1, 1, 1) # Texto branco
            )
            btn.bind(on_press=callback) # Associa a função de callback ao evento de pressionar.
            right_content.add_widget(btn)

        # Área rolável para exibir a lista de usuários e solicitações.
        self.scroll = ScrollView(size_hint=(1, 1)) # Ocupa o espaço restante.
        # Layout interno do ScrollView, que conterá as informações e se ajustará ao conteúdo.
        self.info_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10)
        # Garante que a altura do info_layout se expanda para acomodar o conteúdo.
        self.info_layout.bind(minimum_height=self.info_layout.setter('height'))
        self.scroll.add_widget(self.info_layout) # Adiciona o info_layout ao ScrollView.
        right_content.add_widget(self.scroll) # Adiciona o ScrollView ao conteúdo da direita.

        # Adiciona o conteúdo da direita ao layout da direita.
        right_layout.add_widget(right_content)

    # ==================== Métodos de Atualização de UI ====================
    # Métodos para ajustar o tamanho e a posição dos retângulos de fundo.
    def _update_left_rect(self, instance, value):
        self.left_rect.pos = instance.pos
        self.left_rect.size = instance.size

    def _update_right_rect(self, instance, value):
        self.right_rect.pos = instance.pos
        self.right_rect.size = instance.size

    # ==================== Métodos de Manipulação de JSON ====================
    # Carrega os dados dos usuários do arquivo JSON.
    def load_users_data(self):
        try:
            with open(self.users_json, "r", encoding="utf-8") as f:
                return json.load(f) # Carrega e retorna a lista de usuários.
        except (FileNotFoundError, json.JSONDecodeError):
            # Se o arquivo não existir ou estiver corrompido, retorna uma lista vazia.
            return []

    # Salva os dados dos usuários no arquivo JSON.
    def save_users_data(self, data):
        with open(self.users_json, "w", encoding="utf-8") as f:
            # Salva os dados formatados com indentação para facilitar a leitura.
            json.dump(data, f, ensure_ascii=False, indent=4)

    # Carrega os dados dos serviços (solicitações) do arquivo JSON.
    def load_services_data(self):
        try:
            with open(self.services_updates_json, "r", encoding="utf-8") as f:
                return json.load(f) # Carrega e retorna o dicionário de serviços.
        except (FileNotFoundError, json.JSONDecodeError):
            # Se o arquivo não existir ou estiver corrompido, retorna um dicionário vazio.
            return {}

    # Salva os dados dos serviços no arquivo JSON.
    def save_services_data(self, data):
        with open(self.services_updates_json, "w", encoding="utf-8") as f:
            # Salva os dados formatados com indentação.
            json.dump(data, f, ensure_ascii=False, indent=4)

    # ==================== Métodos de Administração ====================

    # Exibe um formulário em um popup para editar os dados de um usuário.
    def show_edit_user_form(self, instance, prefill_user=None):
        # Aumenta o tamanho do popup para acomodar todos os campos de edição.
        popup_content = BoxLayout(orientation='vertical', padding=10, spacing=10, size_hint=(None, None), size=(300, 450))
        popup_content.add_widget(Label(text='Editar Usuário', size_hint_y=None, height=30))

        # Cria campos de entrada de texto para cada dado do usuário.
        # O CPF é somente leitura se um usuário for pré-selecionado para edição.
        cpf_input = TextInput(hint_text='CPF do Usuário', size_hint_y=None, height=40, readonly=bool(prefill_user))
        username_input = TextInput(hint_text='Nome de Usuário', size_hint_y=None, height=40)
        email_input = TextInput(hint_text='Email', size_hint_y=None, height=40)
        telefone_input = TextInput(hint_text='Telefone', size_hint_y=None, height=40)
        # Campo de senha é oculto e indica que pode ser deixado em branco para não alterar.
        senha_input = TextInput(hint_text='Senha (deixe em branco para não alterar)', password=True, size_hint_y=None, height=40)
        cep_input = TextInput(hint_text='CEP', size_hint_y=None, height=40)
        bairro_input = TextInput(hint_text='Bairro', size_hint_y=None, height=40)

        # Se um usuário for passado (para edição de um usuário existente), pré-preenche os campos.
        if prefill_user:
            cpf_input.text = prefill_user.get("cpf", "")
            username_input.text = prefill_user.get("username", "")
            email_input.text = prefill_user.get("email", "")
            telefone_input.text = prefill_user.get("telefone", "")
            # A senha não é pré-preenchida por segurança.
            cep_input.text = prefill_user.get("cep", "")
            bairro_input.text = prefill_user.get("bairro", "")

        # Adiciona todos os campos de entrada ao conteúdo do popup.
        popup_content.add_widget(cpf_input)
        popup_content.add_widget(username_input)
        popup_content.add_widget(email_input)
        popup_content.add_widget(telefone_input)
        popup_content.add_widget(senha_input)
        popup_content.add_widget(cep_input)
        popup_content.add_widget(bairro_input)

        # Botão para salvar as alterações.
        save_btn = Button(text='Salvar', size_hint_y=None, height=40)
        # Define a função que será chamada ao pressionar o botão "Salvar".
        def save_user(_):
            cpf = cpf_input.text.strip()
            if not cpf:
                self.show_popup('Erro', 'Informe o CPF do usuário.')
                return
            
            users_data = self.load_users_data() # Carrega todos os usuários.
            user_found = False
            # Procura pelo usuário com o CPF fornecido.
            for user in users_data:
                if user.get("cpf") == cpf:
                    # Atualiza os campos do usuário, usando o valor existente se o novo estiver vazio.
                    user["username"] = username_input.text.strip() or user["username"]
                    user["email"] = email_input.text.strip() or user["email"]
                    user["telefone"] = telefone_input.text.strip() or user["telefone"]
                    # Só atualiza a senha se um novo valor foi digitado.
                    if senha_input.text.strip():
                        user["senha"] = senha_input.text.strip()
                    user["cep"] = cep_input.text.strip() or user["cep"]
                    user["bairro"] = bairro_input.text.strip() or user["bairro"]
                    user_found = True
                    break
            
            if user_found:
                self.save_users_data(users_data) # Salva os dados atualizados.
                self.show_popup('Sucesso', 'Dados do usuário atualizados.')
                popup.dismiss() # Fecha o popup.
                self.list_users_requests(None) # Atualiza a lista exibida na tela principal.
            else:
                self.show_popup('Erro', 'Usuário não encontrado.')
                
        save_btn.bind(on_press=save_user) # Associa a função save_user ao botão.
        popup_content.add_widget(save_btn)

        # Cria e abre o popup.
        popup = Popup(title='Editar Usuário', content=popup_content, size_hint=(None, None), size=(350, 500))
        popup.open()

    # Exibe um formulário em um popup para excluir uma solicitação de serviço.
    def show_delete_request_form(self, instance, prefill_service_id=None):
        popup_content = BoxLayout(orientation='vertical', padding=10, spacing=10, size_hint=(None, None), size=(300, 150))
        popup_content.add_widget(Label(text='Excluir Solicitação (Serviço)', size_hint_y=None, height=30))

        # Campo para inserir o ID da solicitação de serviço.
        service_id_input = TextInput(hint_text='ID da Solicitação (Serviço)', size_hint_y=None, height=40, readonly=bool(prefill_service_id))
        if prefill_service_id:
            service_id_input.text = prefill_service_id
        popup_content.add_widget(service_id_input)

        # Botão para excluir.
        delete_btn = Button(text='Excluir', size_hint_y=None, height=40)
        # Função chamada ao clicar em "Excluir".
        def delete_service(_):
            service_id = service_id_input.text.strip()
            if not service_id:
                self.show_popup('Erro', 'Informe o ID da solicitação (serviço).')
                return
            
            services_data = self.load_services_data() # Carrega todos os serviços.
            service_found = False
            service_title_to_delete = None # Armazena a chave do dicionário para exclusão.
            # Percorre os valores do dicionário para encontrar o serviço pelo ID.
            for title, service_info in services_data.items():
                if service_info.get("id") == service_id:
                    service_title_to_delete = title
                    service_found = True
                    break

            if service_found:
                del services_data[service_title_to_delete] # Remove o serviço do dicionário.
                self.save_services_data(services_data) # Salva os dados atualizados.
                self.show_popup('Sucesso', f'Solicitação (Serviço ID: {service_id}) excluída.')
                popup.dismiss() # Fecha o popup.
                self.list_users_requests(None) # Atualiza a lista na tela principal.
            else:
                self.show_popup('Erro', 'Solicitação (Serviço) não encontrada.')
        
        delete_btn.bind(on_press=delete_service) # Associa a função delete_service ao botão.
        popup_content.add_widget(delete_btn)

        # Cria e abre o popup.
        popup = Popup(title='Excluir Solicitação', content=popup_content, size_hint=(None, None), size=(350, 200))
        popup.open()

    # Lista todos os usuários e solicitações de serviço na área de informações.
    def list_users_requests(self, instance):
        self.info_layout.clear_widgets() # Limpa o conteúdo anterior da área de informações.
        self.info_layout.add_widget(Label(text='Usuários', size_hint_y=None, height=30, font_size=18, color=(0,0,0,1)))

        users_data = self.load_users_data() # Carrega os dados dos usuários.

        # Lista informações básicas dos usuários com botões de ação (Editar).
        if users_data:
            for user in users_data:
                user_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, spacing=5)
                user_info_label = Label(
                    text=f'Nome: {user.get("username", "")} | CPF: {user.get("cpf", "")}',
                    size_hint_x=0.7,
                    font_size=15,
                    color=(0, 0, 0, 1),
                    halign='left',
                    valign='middle'
                )
                user_info_label.bind(size=user_info_label.setter('text_size'))
                user_box.add_widget(user_info_label)

                # Botão "Editar" para abrir o formulário de edição do usuário.
                edit_btn = Button(text='Editar', size_hint_x=0.15, background_color=(0.1, 0.7, 0.3, 1), color=(1,1,1,1))
                # Usa uma lambda para passar o objeto 'user' como argumento.
                edit_btn.bind(on_press=lambda _, u=user: self.show_edit_user_form(None, prefill_user=u))
                user_box.add_widget(edit_btn)
                
                # Botão de exclusão de usuário (comentado, pode ser ativado se necessário).
                # delete_user_btn = Button(text='Excluir', size_hint_x=0.15, background_color=(0.9, 0.2, 0.2, 1), color=(1,1,1,1))
                # delete_user_btn.bind(on_press=lambda _, u=user: self.delete_user(u.get("cpf")))
                # user_box.add_widget(delete_user_btn)

                self.info_layout.add_widget(user_box)
        else:
            self.info_layout.add_widget(Label(text='Nenhum usuário cadastrado.', size_hint_y=None, height=30, color=(0,0,0,1)))

        # Adiciona um separador visual para a seção de serviços.
        self.info_layout.add_widget(Label(text='Serviços (Solicitações)', size_hint_y=None, height=30, font_size=18, color=(0,0,0,1)))

        services_data = self.load_services_data() # Carrega os dados dos serviços.

        # Lista serviços/solicitações com botões de ação (Atualizar, Excluir).
        if services_data:
            for service_title, service in services_data.items():
                service_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, spacing=5)
                service_info_label = Label(
                    text=f'ID: {service.get("id")} | Título: {service.get("title", service_title)} | Status: {service.get("status", "")}',
                    size_hint_x=0.7,
                    font_size=15,
                    color=(0, 0, 0, 1),
                    halign='left',
                    valign='middle'
                )
                service_info_label.bind(size=service_info_label.setter('text_size'))
                service_box.add_widget(service_info_label)

                # Botão "Atualizar" para ir para a tela de atualização do serviço.
                update_btn = Button(text='Atualizar', size_hint_x=0.15, background_color=(0.1, 0.5, 0.8, 1), color=(1,1,1,1))
                # Usa uma lambda para passar o ID do serviço como argumento.
                update_btn.bind(on_press=lambda _, s_id=service.get("id"): self.show_update_service_form(None, prefill_service_id=s_id))
                service_box.add_widget(update_btn)

                # Botão "Excluir" para remover a solicitação de serviço.
                delete_btn = Button(text='Excluir', size_hint_x=0.15, background_color=(0.9, 0.2, 0.2, 1), color=(1,1,1,1))
                # Usa uma lambda para passar o ID do serviço como argumento.
                delete_btn.bind(on_press=lambda _, s_id=service.get("id"): self.show_delete_request_form(None, prefill_service_id=s_id))
                service_box.add_widget(delete_btn)

                self.info_layout.add_widget(service_box)
        else:
            self.info_layout.add_widget(Label(text='Nenhum serviço (solicitação) cadastrado.', size_hint_y=None, height=30, color=(0,0,0,1)))

    # Exibe um formulário em um popup para obter o ID de um serviço e redirecionar para a tela de atualização.
    def show_update_service_form(self, instance, prefill_service_id=None):
        popup_content = BoxLayout(orientation='vertical', padding=10, spacing=10, size_hint=(None, None), size=(300, 150))
        popup_content.add_widget(Label(text='Atualizar Serviço', size_hint_y=None, height=30))

        # Campo para inserir o ID do serviço.
        service_id_input = TextInput(hint_text='ID do Serviço (ex: 897TKO)', size_hint_y=None, height=40)
        if prefill_service_id:
            service_id_input.text = prefill_service_id
        popup_content.add_widget(service_id_input)

        # Botão para iniciar o processo de atualização.
        go_btn = Button(text='Ir para Atualização', size_hint_y=None, height=40)
        # Função chamada ao clicar em "Ir para Atualização".
        def go_to_update(_):
            service_id = service_id_input.text.strip()
            # Valida o formato do ID do serviço (deve ter 6 caracteres).
            if not service_id or len(service_id) != 6:
                self.show_popup('Erro', 'ID deve ter 6 caracteres (ex: 897TKO).')
                return
            
            updates_data = self.load_services_data() # Carrega os dados dos serviços.

            service = None
            # Procura o serviço pelo ID.
            for value in updates_data.values():
                if value.get("id") == service_id:
                    service = value
                    break

            if service:
                # Se o serviço for encontrado, redireciona para a tela 'service_update'.
                if 'service_update' in self.manager.screen_names:
                    # Obtém a instância da tela 'service_update'.
                    service_update_screen = self.manager.get_screen('service_update')
                    # Se a tela tiver um método 'set_update_data', passa os dados do serviço.
                    if hasattr(service_update_screen, "set_update_data"):
                        service_update_screen.set_update_data(service)
                    self.manager.current = 'service_update' # Navega para a tela.
                    popup.dismiss() # Fecha o popup.
                else:
                    self.show_popup('Erro', 'Tela de atualização de serviço ("service_update") não encontrada. Verifique se ela está registrada no ScreenManager.')
            else:
                self.show_popup('Erro', 'Serviço não encontrado.')
        
        go_btn.bind(on_press=go_to_update) # Associa a função go_to_update ao botão.
        popup_content.add_widget(go_btn)

        # Cria e abre o popup.
        popup = Popup(title='Atualizar Serviço', content=popup_content, size_hint=(None, None), size=(350, 200))
        popup.open()

    # Método utilitário para exibir popups de mensagem simples.
    def show_popup(self, title, message):
        popup_content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        popup_content.add_widget(Label(text=message))
        close_btn = Button(text='Fechar', size_hint_y=None, height=40)
        popup_content.add_widget(close_btn)
        # Cria o popup.
        popup = Popup(title=title, content=popup_content, size_hint=(None, None), size=(300, 150))
        close_btn.bind(on_press=popup.dismiss) # Associa o botão de fechar ao fechamento do popup.
        popup.open()

    # ==================== Métodos de Navegação ====================
    # Navega de volta para a tela de login.
    def go_to_login(self, instance):
        if 'login' in self.manager.screen_names:
            self.manager.current = 'login'
        else:
            print("Erro: tela 'login' não encontrada")

    # Este método é chamado automaticamente pelo Kivy quando a tela está prestes a ser exibida.
    def on_pre_enter(self, *args):
        app = App.get_running_app() # Obtém a instância do aplicativo.
        # Verifica se há um usuário logado e se ele tem permissões de administrador.
        if not (hasattr(app, "usuario_logado") and app.usuario_logado and app.usuario_logado.get("is_admin", False)):
            # Se o usuário não for admin, redireciona para a tela de landing ou login.
            if self.manager and 'landing' in self.manager.screen_names:
                self.manager.current = 'landing'
            elif self.manager and 'login' in self.manager.screen_names: # Adicionado para caso 'landing' não exista
                self.manager.current = 'login'
            else:
                print("Acesso negado: apenas administradores podem acessar esta tela.")
            return # Impede o restante da lógica de inicialização do admin.

        # Se o usuário for admin, atualiza o rótulo com o nome do administrador.
        admin_nome = app.usuario_logado.get("username", "Administrador")
        self.admin_label.text = f'Admin: {admin_nome}'
        # Atualiza a lista de usuários e solicitações sempre que a tela é acessada.
        self.list_users_requests(None)