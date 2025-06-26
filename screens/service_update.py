from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image
from kivy.uix.spinner import Spinner
from kivy.graphics import Color, Rectangle
import os
from datetime import datetime
import json

class ServiceUpdateScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.update_data = None
        self.current_user = "Administrador"  # Nome do usuário fixo para demonstração
        self.is_admin = True  # Verificação de administrador (fixa para demonstração)
        self.json_file = "admin_updates.json"  # Arquivo para armazenar atualizações e status

        # Layout principal
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Título
        self.title_label = Label(
            text='Detalhes da Atualização',
            font_size=24,
            size_hint_y=None,
            height=50,
            color=(0, 0, 0, 1),
            font_name='Roboto',
            halign='center',
            text_size=(None, None)
        )
        self.title_label.bind(width=lambda instance, value: setattr(instance, 'text_size', (instance.width, None)))
        main_layout.add_widget(self.title_label)

        # Layout para imagem e detalhes
        content_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=200, spacing=10)
        with content_layout.canvas.before:
            Color(0.98, 0.98, 0.98, 1)  # Fundo cinza claro
            self.content_rect = Rectangle(size=content_layout.size, pos=content_layout.pos)
        content_layout.bind(size=self._update_content_rect, pos=self._update_content_rect)

        # Imagem
        self.service_image = Image(
            source='',
            size_hint_x=0.3,
            size_hint_y=None,
            height=180,
            fit_mode='contain'
        )
        content_layout.add_widget(self.service_image)

        # Detalhes
        details_layout = BoxLayout(orientation='vertical', size_hint_x=0.7, padding=[5, 5, 5, 5], spacing=5)
        self.desc_label = Label(
            text='',
            font_size=14,
            color=(0, 0, 0, 1),
            size_hint_y=None,
            height=80,
            halign='left',
            valign='top',
            text_size=(None, None)
        )
        self.desc_label.bind(width=lambda instance, value: setattr(instance, 'text_size', (instance.width, None)))
        details_layout.add_widget(self.desc_label)

        self.address_label = Label(
            text='',
            font_size=12,
            color=(0.5, 0.5, 0.5, 1),
            size_hint_y=None,
            height=30,
            halign='left',
            valign='middle',
            text_size=(None, None)
        )
        self.address_label.bind(width=lambda instance, value: setattr(instance, 'text_size', (instance.width, None)))
        details_layout.add_widget(self.address_label)

        self.status_label = Label(
            text='Status: ',
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

        self.date_label = Label(
            text='',
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

        content_layout.add_widget(details_layout)
        main_layout.add_widget(content_layout)

        # Área para status
        status_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, spacing=10)
        status_label = Label(
            text='Andamento da Obra:',
            font_size=14,
            color=(0, 0, 0, 1),
            size_hint_x=0.3,
            halign='left',
            valign='middle',
            text_size=(None, None)
        )
        status_label.bind(width=lambda instance, value: setattr(instance, 'text_size', (instance.width, None)))
        status_layout.add_widget(status_label)

        self.status_spinner = Spinner(
            text='Em análise',
            values=('Em análise', 'Em andamento', 'Concluída'),
            size_hint_x=0.7,
            font_size=14,
            disabled=not self.is_admin
        )
        self.status_spinner.bind(text=self.update_status)
        status_layout.add_widget(self.status_spinner)
        main_layout.add_widget(status_layout)

        # Área para atualizações do administrador
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

        # ScrollView para exibir atualizações do administrador
        self.admin_scroll = ScrollView(size_hint=(1, 0.3))
        self.admin_updates_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            spacing=10,
            padding=[10, 10, 10, 10]
        )
        self.admin_updates_layout.bind(minimum_height=self.admin_updates_layout.setter('height'))
        with self.admin_updates_layout.canvas.before:
            Color(0.95, 0.95, 0.95, 1)  # Fundo cinza claro
            self.admin_updates_rect = Rectangle(size=self.admin_updates_layout.size, pos=self.admin_updates_layout.pos)
        self.admin_updates_layout.bind(size=self._update_admin_updates_rect, pos=self._update_admin_updates_rect)
        self.admin_scroll.add_widget(self.admin_updates_layout)
        main_layout.add_widget(self.admin_scroll)

        # Campo para nova atualização do administrador
        self.admin_input = TextInput(
            hint_text='Digite uma nova atualização...',
            size_hint=(1, None),
            height=60,
            multiline=True,
            font_size=14
        )
        main_layout.add_widget(self.admin_input)

        # Botão para enviar atualização
        submit_button = Button(
            text='Enviar Atualização',
            size_hint=(0.8, None),
            height=50,
            background_color=(0.1, 0.7, 0.3, 1),
            color=(1, 1, 1, 1),
            pos_hint={'center_x': 0.5}
        )
        submit_button.bind(on_press=self.submit_admin_update)
        main_layout.add_widget(submit_button)

        # Botão para voltar ao admin
        back_button = Button(
            text='Voltar para tela de admin',
            size_hint=(0.8, None),
            height=50,
            background_color=(0.1, 0.7, 0.3, 1),
            color=(1, 1, 1, 1),
            pos_hint={'center_x': 0.5}
        )
        back_button.bind(on_press=self.go_to_admin)
        main_layout.add_widget(back_button)

        self.add_widget(main_layout)

    def set_update_data(self, update):
        """Define os dados da atualização de serviço e carrega atualizações do JSON."""
        self.update_data = update
        self.title_label.text = update['title']
        self.service_image.source = update['image']
        self.desc_label.text = update['description']
        self.address_label.text = f'Endereço: {update["address"]}'
        self.status_label.text = f'Status: {update["status"]}'
        self.date_label.text = f'Data: {update["date"]}'
        self.status_spinner.text = update['status']
        
        # Limpa o layout de atualizações
        self.admin_updates_layout.clear_widgets()
        
        # Carrega atualizações do JSON
        try:
            with open(self.json_file, 'r') as f:
                all_updates = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            all_updates = {}
        
        # Verifica se all_updates é um dicionário
        if not isinstance(all_updates, dict):
            print(f"Erro: Formato inválido em {self.json_file}. Esperado dicionário, encontrado {type(all_updates)}.")
            all_updates = {}
        
        # Obtém dados do serviço atual
        service_data = all_updates.get(self.update_data['title'], {})
        
        # Verifica se service_data é uma lista (formato antigo)
        if isinstance(service_data, list):
            print(f"Convertendo formato antigo para {self.update_data['title']}.")
            service_data = {
                'id': self.update_data.get('id', '000AAA'),
                'title': self.update_data['title'],
                'description': self.update_data.get('description', 'Descrição não disponível'),
                'date': self.update_data.get('date', '01/01/2023'),
                'address': self.update_data.get('address', 'Endereço não disponível'),
                'image': self.update_data.get('image', os.path.join('images', 'default.png')),
                'status': self.update_data.get('status', 'Em análise'),
                'type': self.update_data.get('type', 'Serviço Geral'),
                'last_update': self.update_data.get('last_update', '01/01/2023 00:00'),
                'updates': service_data
            }
            all_updates[self.update_data['title']] = service_data
            # Salva a nova estrutura no JSON
            with open(self.json_file, 'w') as f:
                json.dump(all_updates, f, indent=4)
        
        # Obtém atualizações do serviço
        service_updates = service_data.get('updates', [])
        
        # Ordena atualizações por data (mais recentes primeiro)
        try:
            service_updates.sort(
                key=lambda x: datetime.strptime(x['date'], '%d/%m/%Y %H:%M'),
                reverse=True
            )
        except (KeyError, ValueError) as e:
            print(f"Erro ao ordenar atualizações: {e}")
        
        # Exibe atualizações ordenadas
        for update in service_updates:
            update_layout = BoxLayout(
                orientation='vertical',
                size_hint_y=None,
                height=80,
                padding=[5, 5, 5, 5],
                spacing=5
            )
            with update_layout.canvas.before:
                Color(1, 1, 1, 1)  # Fundo branco
                update_layout.rect = Rectangle(size=update_layout.size, pos=update_layout.pos)
            update_layout.bind(size=self._update_update_rect, pos=self._update_update_rect)

            update_label = Label(
                text=update['text'],
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
                text=f'Por: {update["user"]} em {update["date"]}',
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

            self.admin_updates_layout.add_widget(update_layout)

    def update_status(self, instance, value):
        """Atualiza o status do serviço e salva no JSON."""
        if not self.is_admin:
            return  # Impede alterações se não for administrador
        
        self.update_data['status'] = value
        self.status_label.text = f'Status: {value}'
        
        # Salva o status no JSON
        try:
            with open(self.json_file, 'r') as f:
                all_updates = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            all_updates = {}
        
        # Verifica se all_updates é um dicionário
        if not isinstance(all_updates, dict):
            print(f"Erro: Formato inválido em {self.json_file}. Reinicializando.")
            all_updates = {}
        
        service_title = self.update_data['title']
        service_data = all_updates.get(service_title, {'updates': [], 'status': 'Em análise'})
        
        # Verifica se service_data é uma lista (formato antigo)
        if isinstance(service_data, list):
            print(f"Convertendo formato antigo para {service_title}.")
            service_data = {
                'id': self.update_data.get('id', '000AAA'),
                'title': service_title,
                'description': self.update_data.get('description', 'Descrição não disponível'),
                'date': self.update_data.get('date', '01/01/2023'),
                'address': self.update_data.get('address', 'Endereço não disponível'),
                'image': self.update_data.get('image', os.path.join('images', 'default.png')),
                'status': value,
                'type': self.update_data.get('type', 'Serviço Geral'),
                'last_update': self.update_data.get('last_update', '01/01/2023 00:00'),
                'updates': service_data
            }
        
        service_data['status'] = value
        all_updates[service_title] = service_data
        
        with open(self.json_file, 'w') as f:
            json.dump(all_updates, f, indent=4)
        
        # Atualiza o status na lista service_updates da BlogScreen
        if 'blog' in self.manager.screen_names:
            blog_screen = self.manager.get_screen('blog')
            for service in blog_screen.service_updates:
                if service['title'] == service_title:
                    service['status'] = value
                    break
            blog_screen.update_posts(blog_screen.service_updates)

    def submit_admin_update(self, instance):
        """Adiciona uma nova atualização do administrador e salva no JSON."""
        update_text = self.admin_input.text.strip()
        if update_text:
            # Obtém a data atual no formato DD/MM/AAAA HH:MM
            current_time = datetime.now().strftime('%d/%m/%Y %H:%M')
            
            # Cria um layout para a atualização com usuário e data
            update_layout = BoxLayout(
                orientation='vertical',
                size_hint_y=None,
                height=80,
                padding=[5, 5, 5, 5],
                spacing=5
            )
            with update_layout.canvas.before:
                Color(1, 1, 1, 1)  # Fundo branco
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

            self.admin_updates_layout.add_widget(update_layout, index=0)  # Adiciona no topo
            
            # Salva a atualização no JSON
            try:
                with open(self.json_file, 'r') as f:
                    all_updates = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                all_updates = {}
            
            # Verifica se all_updates é um dicionário
            if not isinstance(all_updates, dict):
                print(f"Erro: Formato inválido em {self.json_file}. Reinicializando.")
                all_updates = {}
            
            service_title = self.update_data['title']
            service_data = all_updates.get(service_title, {'updates': [], 'status': 'Em análise'})
            
            # Verifica e corrige se service_data é uma lista (formato antigo)
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
            
            # Garante que 'updates' exista em service_data
            if 'updates' not in service_data:
                service_data['updates'] = []
            
            # Adiciona a nova atualização
            service_data['updates'].append({
                'text': update_text,
                'user': self.current_user,
                'date': current_time
            })
            
            # Atualiza a última data de atualização
            service_data['last_update'] = current_time
            
            # Ordena as atualizações do serviço por data (mais recentes primeiro)
            try:
                service_data['updates'].sort(
                    key=lambda x: datetime.strptime(x['date'], '%d/%m/%Y %H:%M'),
                    reverse=True
                )
            except (KeyError, ValueError) as e:
                print(f"Erro ao ordenar atualizações: {e}")
            
            all_updates[service_title] = service_data
            
            with open(self.json_file, 'w') as f:
                json.dump(all_updates, f, indent=4)
            
            # Atualiza a BlogScreen com o novo last_update
            if 'blog' in self.manager.screen_names:
                blog_screen = self.manager.get_screen('blog')
                for service in blog_screen.service_updates:
                    if service['title'] == service_title:
                        service['last_update'] = current_time
                        break
                blog_screen.update_posts(blog_screen.service_updates)
            
            self.admin_input.text = ''  # Limpa o campo após enviar

    def go_to_blog(self, instance):
        if 'blog' in self.manager.screen_names:
            self.manager.current = 'blog'
        else:
            print("Erro: tela 'blog' não encontrada")

    def go_to_admin(self, instance):
        if 'admin' in self.manager.screen_names:
            self.manager.current = 'admin'
        else:
            print("Erro: tela 'admin' não encontrada")

    def _update_content_rect(self, instance, value):
        self.content_rect.pos = instance.pos
        self.content_rect.size = instance.size

    def _update_admin_updates_rect(self, instance, value):
        self.admin_updates_rect.pos = instance.pos
        self.admin_updates_rect.size = instance.size

    def _update_update_rect(self, instance, value):
        instance.rect.pos = instance.pos
        instance.rect.size = instance.size
