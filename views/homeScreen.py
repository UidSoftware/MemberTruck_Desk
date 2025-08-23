# Arquivo: views/homeScreen.py

from kivymd.uix.screen import MDScreen
from kivy.properties import ObjectProperty, StringProperty
from kivy.animation import Animation
from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.label import MDLabel
from kivy.metrics import dp

# Importe aqui as telas de conteúdo que você vai usar
# Corrigido para usar a sua convenção de nome de arquivo: inicioScreen
from views.inicioScreen import InicioScreen

# CORRIGIDO: As telas estão diretamente na pasta views, não em um subdiretório 'cadastro'
from views.funcionarioScreen import FuncionarioScreen
from views.associadoScreen import AssociadoScreen

class HomeScreen(MDScreen):
    """
    Tela principal da aplicação que contém o menu de navegação.
    """
    # Propriedades para referenciar os widgets no .kv
    nav_drawer = ObjectProperty(None)
    content_manager = ObjectProperty(None)
    user_name_label = ObjectProperty(None)
    user_avatar = ObjectProperty(None)
    cadastro_submenu = ObjectProperty(None)

    # Dicionário para armazenar as telas de conteúdo já criadas
    # Isso evita recriar as telas toda vez que o usuário navega.
    content_screens = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Carrega as telas de conteúdo padrão na inicialização
        # As telas são criadas apenas uma vez.
        # Corrigido para usar a sua classe real: InicioScreen
        self.content_screens['inicio'] = InicioScreen(name='inicio')
        
        # Adicione aqui as outras telas de cadastro
        self.content_screens['cadastro_funcionario'] = FuncionarioScreen(name='cadastro_funcionario')
        self.content_screens['cadastro_associado'] = AssociadoScreen(name='cadastro_associado')
        
        # Adiciona a tela de início ao gerenciador de conteúdo
        self.add_widget_to_content_manager(self.content_screens['inicio'])
        
        # Acessa o ID do content_manager após a inicialização do construtor
        # e define a tela de início como a tela atual.
        self.ids.content_manager.current = 'inicio'

    def on_enter(self, *args):
        """
        Método chamado quando a tela HomeScreen se torna a tela atual.
        É o lugar ideal para carregar os dados do usuário.
        """
        app = MDApp.get_running_app()
        if app.is_logged_in and app.logged_in_user_data:
            user_data = app.logged_in_user_data
            self.ids.user_name_label.text = user_data.get('nomePess', 'Usuário')
            self.ids.user_avatar.source = user_data.get('foto_perfil', 'image/luiz.png')

    def add_widget_to_content_manager(self, widget_instance):
        """
        Adiciona uma tela de conteúdo ao ScreenManager interno se ela ainda não existir.
        """
        if widget_instance not in self.ids.content_manager.children:
            self.ids.content_manager.add_widget(widget_instance)

    def switch_content_screen(self, screen_name):
        """
        Muda a tela de conteúdo exibida no ScreenManager interno.
        """
        # Verifica se a tela já existe no dicionário e muda para ela.
        if screen_name in self.content_screens:
            self.add_widget_to_content_manager(self.content_screens[screen_name])
            self.ids.content_manager.current = screen_name
            print(f"Mudando para a tela de conteúdo: {screen_name}")
        else:
            print(f"Tela '{screen_name}' não encontrada no dicionário de telas.")

    def toggle_cadastro_menu(self):
        """
        Anima a exibição e o recolhimento do submenu de cadastro.
        """
        submenu_widget = self.ids.cadastro_submenu
        # Define a nova altura e opacidade com base no estado atual
        # A altura é calculada com base no número de itens (48dp cada)
        # Mais 5dp de espaçamento entre eles.
        num_items = 4 # Funcionarios, Associados, Departamentos, Cargos
        spacing = 5
        new_height = dp(48) * num_items + dp(spacing) * (num_items-1) if submenu_widget.height == 0 else 0
        new_opacity = 1 if submenu_widget.opacity == 0 else 0

        # Cria e inicia a animação
        animation = Animation(height=new_height, opacity=new_opacity, duration=0.2)
        animation.start(submenu_widget)
