# Arquivo: views/loginScreen.py

import requests
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField

Builder.load_file('views/loginScreen.kv')


class LoginScreen(MDScreen):
    """
    Tela de login da aplicação.
    
    Gerencia a autenticação do usuário com o backend Django.
    """
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)

    def on_login_button_press(self):
        """
        Método chamado quando o botão de login é pressionado.
        
        Coleta as credenciais e envia para o backend.
        """
        # Limpa qualquer mensagem de erro anterior.
        self.ids.error_label.text = ""
        
        username = self.ids.user_field.text
        password = self.ids.password_field.text
        
        # URL do endpoint de login no seu backend Django.
        # IMPORTANTE: Altere esta URL para a URL correta do seu projeto.
        login_url = "http://31.97.240.156:8888/api/login/"
        
        # Dados a serem enviados no corpo da requisição POST.
        payload = {
            'usuarioPess': username, # Corrigido para o campo esperado
            'password': password
        }
        
        try:
            # Faz a requisição HTTP POST para o backend.
            response = requests.post(login_url, json=payload)
            
            # Verifica o status da resposta.
            if response.status_code == 200:
                # Login bem-sucedido.
                # Você pode lidar com o token de autenticação aqui, se houver.
                print("Login bem-sucedido!")

                self.is_logged_in = True
                
                
                # Navega para a tela 'home'.
                # A propriedade `manager` é o ScreenManager que gerencia a tela.
                self.manager.current = 'home'
                
                
            else:
                # Login falhou.
                error_data = response.json()
                error_message = error_data.get('error', 'Credenciais inválidas.')
                self.ids.error_label.text = error_message
                print(f"Erro de login: {error_message}")
                
        except requests.exceptions.RequestException as e:
            # Trata erros de conexão ou de rede.
            self.ids.error_label.text = "Erro de conexão. Verifique o servidor."
            print(f"Erro de conexão: {e}")
