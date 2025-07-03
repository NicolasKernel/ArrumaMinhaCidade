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

class AdminScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.users_json = "usuarios.json"

        # Layout principal horizontal
        main_layout = BoxLayout(orientation='horizontal', spacing=10)

        # Layouts verticais para a esquerda e direita
        left_layout = BoxLayout(orientation='vertical', size_hint_x=0.25, padding=10, spacing=10)
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
            text='Painel do Administrador',
            font_size=24,
            size_hint=(1, 0.2),
            color=(0, 0, 0, 1),
            font_name='Roboto'
        )
        left_layout.add_widget(title)

        logo = Image(
            source=os.path.join('resources', 'logo.png'),
            size_hint=(1, None),
            height=300,
            fit_mode='contain'
        )
        left_layout.add_widget(logo)

        buttons = [
            ('Voltar à Login', self.go_to_login),
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

        # ==================== Layout da Direita: Barra Superior ====================

        top_bar = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=80,
            padding=10,
            spacing=10
        )

        top_bar.add_widget(Widget(size_hint_x=1))

        admin_nome = "Administrador"
        app = App.get_running_app()
        if hasattr(app, "usuario_logado") and app.usuario_logado:
            admin_nome = app.usuario_logado.get("username", "Administrador")
        self.admin_label = Label(
            text=f'Admin: {admin_nome}',
            font_size=20,
            color=(0, 0, 0, 1),
            size_hint=(None, None),
            size=(200, 60),
            halign='right',
            valign='middle'
        )
        self.admin_label.bind(size=self.admin_label.setter('text_size'))
        top_bar.add_widget(self.admin_label)

        profile_pic = Image(
            source=os.path.join('resources', 'logo.png'),
            size_hint=(None, None),
            size=(60, 60),
            fit_mode='contain'
        )
        top_bar.add_widget(profile_pic)

        right_layout.add_widget(top_bar)

        # ==================== Layout da Direita: Conteúdo ====================

        right_content = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # Três botões de administração
        admin_buttons = [
            ('Alterar Dados do Usuário', self.show_edit_user_form),
            ('Excluir Solicitação', self.show_delete_request_form),
            ('Listar Usuários/Solicitações', self.list_users_requests),
            ('Atualizar Serviço', self.show_update_service_form)  # Novo botão
        ]
        for text, callback in admin_buttons:
            btn = Button(
                text=text,
                size_hint=(1, None),
                height=50,
                background_color=(1, 0.4, 0.4, 1),
                color=(1, 1, 1, 1)
            )
            btn.bind(on_press=callback)
            right_content.add_widget(btn)

        # Área rolável para exibir informações
        self.scroll = ScrollView(size_hint=(1, 1))
        self.info_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10)
        self.info_layout.bind(minimum_height=self.info_layout.setter('height'))
        self.scroll.add_widget(self.info_layout)
        right_content.add_widget(self.scroll)

        right_layout.add_widget(right_content)

        # DADOS SIMULADOS EDITAR PARA TOMAR DOS JSON
        self.users = [
            {"id": 1, "username": "joao", "cidade": "São Paulo"},
            {"id": 2, "username": "maria", "cidade": "Rio de Janeiro"}
        ]
        self.requests = [
            {"id": 1, "servico": "Limpeza", "data": "2025-06-20"},
            {"id": 2, "servico": "Pavimentação", "data": "2025-06-22"}
        ]

    # ==================== Métodos de Atualização ====================

    def _update_left_rect(self, instance, value):
        self.left_rect.pos = instance.pos
        self.left_rect.size = instance.size

    def _update_right_rect(self, instance, value):
        self.right_rect.pos = instance.pos
        self.right_rect.size = instance.size

    # ==================== Métodos de Administração ====================

    def show_edit_user_form(self, instance):
        popup_content = BoxLayout(orientation='vertical', padding=10, spacing=10, size_hint=(None, None), size=(300, 250))
        popup_content.add_widget(Label(text='Editar Usuário', size_hint_y=None, height=30))

        cpf_input = TextInput(hint_text='CPF do Usuário', size_hint_y=None, height=40)
        username_input = TextInput(hint_text='Nome', size_hint_y=None, height=40)
        bairro_input = TextInput(hint_text='Bairro', size_hint_y=None, height=40)

        popup_content.add_widget(cpf_input)
        popup_content.add_widget(username_input)
        popup_content.add_widget(bairro_input)

        save_btn = Button(text='Salvar', size_hint_y=None, height=40)
        def save_user(_):
            cpf = cpf_input.text.strip()
            if not cpf:
                self.show_popup('Erro', 'Informe o CPF do usuário.')
                return
            # Carrega usuários do JSON
            try:
                with open(self.users_json, "r", encoding="utf-8") as f:
                    users_data = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                users_data = []

            user = next((u for u in users_data if u.get("cpf") == cpf), None)
            if user:
                user["username"] = username_input.text.strip() or user["username"]
                user["bairro"] = bairro_input.text.strip() or user["bairro"]
                # Salva alterações
                with open(self.users_json, "w", encoding="utf-8") as f:
                    json.dump(users_data, f, ensure_ascii=False, indent=4)
                self.show_popup('Sucesso', 'Dados do usuário atualizados.')
            else:
                self.show_popup('Erro', 'Usuário não encontrado.')
        save_btn.bind(on_press=save_user)
        popup_content.add_widget(save_btn)

        popup = Popup(title='Editar Usuário', content=popup_content, size_hint=(None, None), size=(350, 300))
        popup.open()

    def show_delete_request_form(self, instance):
        popup_content = BoxLayout(orientation='vertical', padding=10, spacing=10, size_hint=(None, None), size=(300, 150))
        popup_content.add_widget(Label(text='Excluir Solicitação', size_hint_y=None, height=30))

        request_id_input = TextInput(hint_text='ID da Solicitação', size_hint_y=None, height=40)
        popup_content.add_widget(request_id_input)

        delete_btn = Button(text='Excluir', size_hint_y=None, height=40)
        def delete_request(_):
            request_id = request_id_input.text.strip()
            if not request_id.isdigit():
                self.show_popup('Erro', 'ID deve ser um número.')
                return
            request_id = int(request_id)
            request = next((r for r in self.requests if r["id"] == request_id), None)
            if request:
                self.requests.remove(request)
                self.show_popup('Sucesso', 'Solicitação excluída.')
            else:
                self.show_popup('Erro', 'Solicitação não encontrada.')
        delete_btn.bind(on_press=delete_request)
        popup_content.add_widget(delete_btn)

        popup = Popup(title='Excluir Solicitação', content=popup_content, size_hint=(None, None), size=(350, 200))
        popup.open()

    def list_users_requests(self, instance):
        self.info_layout.clear_widgets()
        self.info_layout.add_widget(Label(text='Usuários', size_hint_y=None, height=30, font_size=18))

        # Carrega usuários do JSON
        try:
            with open(self.users_json, "r", encoding="utf-8") as f:
                users_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            users_data = []

        # Lista apenas informações básicas dos usuários
        for user in users_data:
            user_info = Label(
                text=f'Nome: {user.get("username", "")} | Email: {user.get("email", "")} | Bairro: {user.get("bairro", "")}',
                size_hint_y=None,
                height=30,
                font_size=15,
                color=(0, 0, 0, 1)
            )
            self.info_layout.add_widget(user_info)

        self.info_layout.add_widget(Label(text='Serviços', size_hint_y=None, height=30, font_size=18))

        # Carrega serviços do JSON igual ao BlogScreen
        try:
            with open("services_updates.json", "r", encoding="utf-8") as f:
                services_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            services_data = {}

        for service_title, service in services_data.items():
            service_info = Label(
                text=f'Título: {service.get("title", service_title)} | Tipo: {service.get("type", "")} | Status: {service.get("status", "")}',
                size_hint_y=None,
                height=30,
                font_size=15,
                color=(0, 0, 0, 1)
            )
            self.info_layout.add_widget(service_info)

    def pre_fill_edit_form(self, user):
        popup_content = BoxLayout(orientation='vertical', padding=10, spacing=10, size_hint=(None, None), size=(300, 250))
        popup_content.add_widget(Label(text='Editar Usuário', size_hint_y=None, height=30))

        cpf_input = TextInput(text=user.get("cpf", ""), hint_text='CPF do Usuário', size_hint_y=None, height=40, readonly=True)
        username_input = TextInput(text=user.get("username", ""), hint_text='Nome', size_hint_y=None, height=40)
        bairro_input = TextInput(text=user.get("bairro", ""), hint_text='Bairro', size_hint_y=None, height=40)

        popup_content.add_widget(cpf_input)
        popup_content.add_widget(username_input)
        popup_content.add_widget(bairro_input)

        save_btn = Button(text='Salvar', size_hint_y=None, height=40)
        def save_user(_):
            # Carrega usuários do JSON
            try:
                with open(self.users_json, "r", encoding="utf-8") as f:
                    users_data = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                users_data = []

            for u in users_data:
                if u.get("cpf") == cpf_input.text:
                    u["username"] = username_input.text.strip() or u["username"]
                    u["bairro"] = bairro_input.text.strip() or u["bairro"]
                    break
            # Salva alterações
            with open(self.users_json, "w", encoding="utf-8") as f:
                json.dump(users_data, f, ensure_ascii=False, indent=4)
            self.show_popup('Sucesso', 'Dados do usuário atualizados.')
            self.list_users_requests(None)
        save_btn.bind(on_press=save_user)
        popup_content.add_widget(save_btn)

        popup = Popup(title='Editar Usuário', content=popup_content, size_hint=(None, None), size=(350, 300))
        popup.open()

    def pre_fill_delete_form(self, request):
        popup_content = BoxLayout(orientation='vertical', padding=10, spacing=10, size_hint=(None, None), size=(300, 150))
        popup_content.add_widget(Label(text='Excluir Solicitação', size_hint_y=None, height=30))

        request_id_input = TextInput(text=str(request["id"]), hint_text='ID da Solicitação', size_hint_y=None, height=40, readonly=True)
        popup_content.add_widget(request_id_input)

        delete_btn = Button(text='Excluir', size_hint_y=None, height=40)
        def delete_request(_):
            self.requests.remove(request)
            self.show_popup('Sucesso', 'Solicitação excluída.')
            self.list_users_requests(None)
        delete_btn.bind(on_press=delete_request)
        popup_content.add_widget(delete_btn)

        popup = Popup(title='Excluir Solicitação', content=popup_content, size_hint=(None, None), size=(350, 200))
        popup.open()

    def show_update_service_form(self, instance):
        popup_content = BoxLayout(orientation='vertical', padding=10, spacing=10, size_hint=(None, None), size=(300, 150))
        popup_content.add_widget(Label(text='Atualizar Serviço', size_hint_y=None, height=30))

        service_id_input = TextInput(hint_text='ID do Serviço (ex: 897TKO)', size_hint_y=None, height=40)
        popup_content.add_widget(service_id_input)

        go_btn = Button(text='Ir para Atualização', size_hint_y=None, height=40)
        def go_to_update(_):
            service_id = service_id_input.text.strip()
            if not service_id or len(service_id) != 6:
                self.show_popup('Erro', 'ID deve ter 6 caracteres (ex: 897TKO).')
                return
            # Carrega serviços do JSON
            try:
                with open("services_updates.json", "r", encoding="utf-8") as f:
                    updates_data = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                updates_data = {}

            # Procura pelo campo "id" dentro dos valores
            service = None
            for value in updates_data.values():
                if value.get("id") == service_id:
                    service = value
                    break

            if service:
                if 'service_update' in self.manager.screen_names:
                    service_update_screen = self.manager.get_screen('service_update')
                    if hasattr(service_update_screen, "set_update_data"):
                        service_update_screen.set_update_data(service)
                    self.manager.current = 'service_update'
            else:
                self.show_popup('Erro', 'Serviço não encontrado.')
        go_btn.bind(on_press=go_to_update)
        popup_content.add_widget(go_btn)

        popup = Popup(title='Atualizar Serviço', content=popup_content, size_hint=(None, None), size=(350, 200))
        popup.open()

    def show_popup(self, title, message):
        popup_content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        popup_content.add_widget(Label(text=message))
        close_btn = Button(text='Fechar', size_hint_y=None, height=40)
        popup_content.add_widget(close_btn)
        popup = Popup(title=title, content=popup_content, size_hint=(None, None), size=(300, 150))
        close_btn.bind(on_press=popup.dismiss)
        popup.open()

    # ==================== Métodos de Navegação ====================

    def go_to_login(self, instance):
        if 'login' in self.manager.screen_names:
            self.manager.current = 'login'
        else:
            print("Erro: tela 'login' não encontrada")

    def on_pre_enter(self, *args):
        app = App.get_running_app()
        if not (hasattr(app, "usuario_logado") and app.usuario_logado and app.usuario_logado.get("is_admin", False)):
            # Usuário não é admin, redireciona para landing ou login
            if self.manager and 'landing' in self.manager.screen_names:
                self.manager.current = 'landing'
            else:
                print("Acesso negado: apenas administradores podem acessar esta tela.")
            return

        admin_nome = app.usuario_logado.get("username", "Administrador")
        self.admin_label.text = f'Admin: {admin_nome}'