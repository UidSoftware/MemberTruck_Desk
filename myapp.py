# -*- coding: utf-8 -*-
"""
Este é o arquivo principal (myapp.py) da sua aplicação.
Esta versão foi adaptada para depuração, focando apenas na tela de login.
"""
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivy.lang import Builder
import os

# Importa apenas a classe da tela de login por enquanto.
from views.loginScreen import LoginScreen
from views.homeScreen import HomeScreen
from views.inicioScreen import InicioScreen
from views.enderecoScreen import EnderecoScreen
from views.associadoScreen import AssociadoScreen
from views.funcionarioScreen import FuncionarioScreen
from views.planoScreen import PlanoScreen
from views.veiculoScreen import VeiculoScreen
from views.cargoScreen import CargoScreen
from views.departamentoScreen import DepartamentoScreen


class MyApp(MDApp):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Declaração da variável com valor inicial
        self.is_logged_in = False
        self.logged_in_user_data = None

    def build(self):
        """
        Método que constrói a interface do usuário e gerencia as telas.
        """
        # Configuração do tema
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Lightseagreen"
        
        def load_kv_files(self):
            """Carrega todos os arquivos KV necessários"""
            kv_dir = os.path.join(os.path.dirname(__file__), 'views')
            kv_files = [
                'loginScreen.kv',
                'homeScreen.kv',
                'inicioScreen.kv',
                'enderecoScreen.kv',
                'associadoScreen.kv',
                'planoScreen.kv',
                'veiculoScreen.kv',
                'funcionarioScreen.kv',
                'cargoScreen.kv',
                'departamento.kv',
                
            ]
            for kv_file in kv_files:
                kv_path = os.path.join(kv_dir, kv_file)
                if os.path.exists(kv_path):
                    Builder.load_file(kv_path)
                else:
                    print(f"Aviso: Arquivo KV não encontrado: {kv_path}")
                    
        # Cria o gerenciador de telas.
        self.root = MDScreenManager()
        
        # Telas ao gerenciador.-----------------------------------------------------------------
        self.root.add_widget(LoginScreen(name='login'))
        self.root.add_widget(HomeScreen(name='home'))
        self.root.add_widget(InicioScreen(name='inicio'))
        self.root.add_widget(EnderecoScreen(name='endereco'))
        self.root.add_widget(AssociadoScreen(name='associado'))
        self.root.add_widget(FuncionarioScreen(name='funcionario'))
        self.root.add_widget(PlanoScreen(name='plano'))
        self.root.add_widget(VeiculoScreen(name='veiculo'))
        self.root.add_widget(CargoScreen(name='cargo'))
        self.root.add_widget(DepartamentoScreen(name='departamento'))

        # Define a tela inicial da aplicação como a de login.
        self.root.current = 'login'

        return self.root

if __name__ == '__main__':
    MyApp().run()
