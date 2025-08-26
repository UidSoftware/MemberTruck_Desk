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

class MyApp(MDApp):
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
        
        # Adiciona APENAS a tela de login ao gerenciador.-----------------------------------------------------------------
        self.root.add_widget(LoginScreen(name='login'))
        
        
        # Define a tela inicial da aplicação como a de login.
        self.root.current = 'login'
        return self.root

if __name__ == '__main__':
    MyApp().run()
