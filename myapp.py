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
        
        # Carrega APENAS o arquivo KV da tela de login.
        # Isso nos ajudará a isolar o problema.
        kv_dir = os.path.join(os.path.dirname(__file__), 'views')
        Builder.load_file(os.path.join(kv_dir, 'loginScreen.kv'))
        
        # Cria o gerenciador de telas.
        self.root = MDScreenManager()
        
        # Adiciona APENAS a tela de login ao gerenciador.
        self.root.add_widget(LoginScreen(name='login'))
        
        # Define a tela inicial da aplicação como a de login.
        self.root.current = 'login'
        return self.root

if __name__ == '__main__':
    MyApp().run()
