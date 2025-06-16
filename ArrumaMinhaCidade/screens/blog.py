from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
import os

class BlogScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Layout principal
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Layout para filtro
        filter_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, spacing=10)

        # Spinner para categoria de filtro
        self.filter_spinner = Spinner(
            text='Filtrar por',
            values=('Região', 'Endereço', 'Bairro', 'Todos'),
            size_hint_x=None,
            width=150
        )
        self.filter_spinner.bind(text=self.on_search_text)
        filter_layout.add_widget(self.filter_spinner)

        # Campo de pesquisa
        self.search_input = TextInput(
            hint_text='Pesquisar...',
            size_hint_y=None,
            height=40,
            multiline=False
        )
        self.search_input.bind(text=self.on_search_text)
        filter_layout.add_widget(self.search_input)

        main_layout.add_widget(filter_layout)

        # Título da tela
        title = Label(
            text='Atualizações de Serviços',
            font_size=24,
            size_hint_y=None,
            height=50,
            color=(0, 0, 0, 1),
            font_name='Roboto',
            halign='center',
            text_size=(None, None)
        )
        main_layout.add_widget(title)

        # ScrollView para a lista de atualizações
        self.scroll = ScrollView(size_hint=(1, 1))
        self.posts_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            spacing=15,
            padding=[10, 10, 10, 10]
        )
        self.posts_layout.bind(minimum_height=self.posts_layout.setter('height'))

        # Fundo para o posts_layout
        with self.posts_layout.canvas.before:
            Color(0.95, 0.95, 0.95, 1)  # Cor de fundo cinza claro
            self.posts_rect = Rectangle(size=self.posts_layout.size, pos=self.posts_layout.pos)
        self.posts_layout.bind(size=self._update_posts_rect, pos=self._update_posts_rect)

        # Dados de exemplo para atualizações de serviços
        self.service_updates = [
            {
                'title': 'Buraco do Jackson',
                'description': 'Buraco gigante no Joquei CLube.',
                'date': '15/06/2025',
                'address': 'Rua Clara Nudes, 123, Jóquei, Fortaleza - CE',
                'image': os.path.join('images', 'limpeza_urbana.png')
            },
            {
                'title': 'Manutenção de Iluminação Pública',
                'description': 'Serviço de manutenção de iluminação pública agora disponível.',
                'date': '14/06/2025',
                'address': 'Av. da Liberdade, 456, Liberdade, São Paulo - SP',
                'image': os.path.join('images', 'iluminacao_publica.png')
            },
            {
                'title': 'Recapeamento de Asfalto',
                'description': 'Iniciado o recapeamento de ruas na zona norte.',
                'date': '13/06/2025',
                'address': 'Rua do Norte, 789, Santana, São Paulo - SP',
                'image': os.path.join('images', 'recapeamento_asfalto.png')
            },
            {
                'title': 'Coleta Seletiva Ampliada',
                'description': 'Ampliamos a coleta seletiva para mais bairros.',
                'date': '12/06/2025',
                'address': 'Rua Verde, 101, Vila Mariana, São Paulo - SP',
                'image': os.path.join('images', 'coleta_seletiva.png')
            }
        ]

        self.scroll.add_widget(self.posts_layout)
        main_layout.add_widget(self.scroll)

        # Botão para voltar à tela inicial
        back_button = Button(
            text='Voltar para Landing',
            size_hint=(1, None),
            height=50,
            background_color=(0.1, 0.7, 0.3, 1),
            color=(1, 1, 1, 1)
        )
        back_button.bind(on_press=self.go_to_landing)
        main_layout.add_widget(back_button)

        self.add_widget(main_layout)

        # Inicializa a lista de posts
        self.update_posts(self.service_updates)

    def update_posts(self, updates):
        self.posts_layout.clear_widgets()
        for update in updates:
            post = BoxLayout(
                orientation='horizontal',
                size_hint_y=None,
                height=220,
                padding=[10, 5, 10, 5],
                spacing=10
            )
            with post.canvas.before:
                Color(1, 1, 1, 1)
                post.post_rect = Rectangle(size=post.size, pos=post.pos)
            post.bind(size=self._update_post_rect, pos=self._update_post_rect)

            service_image = Image(
                source=update['image'],
                size_hint_x=0.3,
                size_hint_y=None,
                height=200,
                fit_mode='contain'
            )
            post.add_widget(service_image)

            text_layout = BoxLayout(
                orientation='vertical',
                size_hint_x=0.7,
                spacing=5
            )

            title_label = Label(
                text=update['title'],
                font_size=18,
                color=(0, 0, 0, 1),
                size_hint_y=None,
                height=40,
                halign='left',
                valign='middle',
                text_size=(None, None)
            )
            title_label.bind(size=title_label.setter('text_size'))
            text_layout.add_widget(title_label)

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

            post.add_widget(text_layout)
            self.posts_layout.add_widget(post)

    def on_search_text(self, instance, value):
        filtro = self.search_input.text.lower()
        categoria = self.filter_spinner.text

        if categoria == 'Todos' or categoria == 'Filtrar por':
            filtrados = [
                s for s in self.service_updates
                if filtro in s['title'].lower() or filtro in s['description'].lower() or filtro in s['address'].lower()
            ]
        elif categoria == 'Região':
            filtrados = [
                s for s in self.service_updates
                if filtro in s['address'].lower()  # Supondo que a região está no endereço
            ]
        elif categoria == 'Endereço':
            filtrados = [
                s for s in self.service_updates
                if filtro in s['address'].lower()
            ]
        elif categoria == 'Bairro':
            filtrados = [
                s for s in self.service_updates
                if filtro in s['address'].lower()  # Supondo que o bairro está no endereço
            ]
        else:
            filtrados = self.service_updates

        self.update_posts(filtrados)

    def _update_posts_rect(self, instance, value):
        self.posts_rect.pos = instance.pos
        self.posts_rect.size = instance.size

    def _update_post_rect(self, instance, value):
        instance.post_rect.pos = instance.pos
        instance.post_rect.size = instance.size

    def go_to_landing(self, instance):
        if 'landing' in self.manager.screen_names:
            self.manager.current = 'landing'
        else:
            print("Erro: tela 'landing' não encontrada")
