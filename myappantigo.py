from kivymd.app import MDApp
from kivymd.uix.textfield import MDTextField
from kivymd.uix.screen import MDScreen
# Importe as classes de botão corretas
from kivymd.uix.button import MDButton, MDButtonText
# Importe as classes de diálogo corretas
from kivymd.uix.dialog import (
    MDDialog,
    MDDialogHeadlineText,
    MDDialogSupportingText,
    MDDialogButtonContainer,
)
from kivymd.uix.widget import Widget # Necessário para o espaçamento no MDDialogButtonContainer
from kivymd.uix.label import MDLabel # Já havíamos adicionado
from kivy.uix.screenmanager import ScreenManager, Screen
# from kivymd.uix.boxlayout import MDBoxLayout # Pode ser útil, mas MDDialogButtonContainer já é um BoxLayout

import requests
import json
from kivy.lang import Builder
from kivy.metrics import dp # Para usar dp() em medidas

from kivymd.uix.menu import MDDropdownMenu

class FuncionarioScreen(Screen): pass

class MyScreenManager(ScreenManager):
    # Você pode adicionar métodos aqui para serem chamados de dentro do KV
    # Por exemplo, para lidar com o login
    def login_user(self, username, password):
        print(f"Tentando logar com {username}:{password}")
        # Aqui você faria a chamada para sua API Django
        # Se sucesso: self.current = 'funcionario'
        # Se falha: exibir mensagem de erro


class MyApp(MDApp):

    

    def build(self):
        self.theme_cls.theme_style = "Dark" # Estilo do tema (claro ou escuro)
        self.theme_cls.primary_palette = "Lightseagreen" # <<== NOVA COR AQUI

        # Carrega o arquivo KV explicitamente.
        # Certifique-se de que myapp.kv está na mesma pasta do myapp.py
        return Builder.load_file('myapp.kv')

    def do_login(self):
        email = self.root.ids.my_user_tf.text
        password = self.root.ids.my_pass_tf.text

        print(f"Email digitado: {email}")
        print(f"Senha digitada: {password}")

        if not email or not password:
            self.show_dialog("Erro de Login", "Por favor, preencha todos os campos.")
            return

        # SUBSTITUA PELA URL REAL DA SUA API DJANGO
        api_url = "http://127.0.0.1:8000/api/login/"
        headers = {"Content-Type": "application/json"}
        payload = {
            "email": email,
            "password": password
        }

        try:
            response = requests.post(api_url, headers=headers, data=json.dumps(payload))
            response.raise_for_status() # Lança um erro para status de erro (4xx, 5xx)

            data = response.json()

            if response.status_code == 200:
                token = data.get("token") # Ajuste para o nome da chave do token na sua API
                self.show_dialog("Sucesso!", f"Login realizado! Token: {token}")
                # A partir daqui, você implementaria a navegação para a próxima tela.
            else:
                self.show_dialog("Erro de Login", "Resposta inesperada da API.")

        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
            try:
                error_data = http_err.response.json()
                error_message = error_data.get("detail", "Erro desconhecido da API.")
                self.show_dialog("Erro de Login", f"Erro da API: {error_message}")
            except (json.JSONDecodeError, AttributeError):
                self.show_dialog("Erro de Login", f"Erro HTTP: {http_err}")
        except requests.exceptions.ConnectionError as conn_err:
            print(f"Connection error occurred: {conn_err}")
            self.show_dialog("Erro de Conexão", "Não foi possível conectar ao servidor. Verifique sua conexão ou a URL da API.")
        except requests.exceptions.Timeout as timeout_err:
            print(f"Timeout error occurred: {timeout_err}")
            self.show_dialog("Tempo Esgotado", "A requisição demorou muito para responder.")
        except requests.exceptions.RequestException as req_err:
            print(f"An unexpected error occurred: {req_err}")
            self.show_dialog("Erro Inesperado", "Ocorreu um erro ao processar sua requisição.")

    def show_dialog(self, title_text, message_text):
        if hasattr(self, 'dialog') and self.dialog.is_open:
            self.dialog.dismiss()

        # Criar o botão "OK"
        # O MDDialogButtonContainer espera widgets de botão.
        ok_button = MDButton(
            style="text", # Botão de texto simples
            on_release=lambda *args: self.dialog.dismiss()
        )
        ok_button.add_widget(MDButtonText(text="OK")) # Texto do botão como widget filho

        # Criar o MDDialog, passando os componentes como argumentos diretos no construtor
        # Conforme o primeiro exemplo da documentação para a versão 2.x
        self.dialog = MDDialog(
            # Título do diálogo
            MDDialogHeadlineText(
                text=title_text,
                halign="center", # Alinhe o título ao centro
            ),
            # Texto de suporte/mensagem
            MDDialogSupportingText(
                text=message_text,
                halign="center", # Alinhe a mensagem ao centro
            ),
            # Contêiner de botões
            MDDialogButtonContainer(
                Widget(), # Isso adiciona um espaço flexível para empurrar o botão para a direita
                ok_button,
                spacing="8dp", # Espaçamento entre os botões (se houvesse mais de um)
            ),
            # Outras propriedades do diálogo (opcionais, mas boas de ter)
            auto_dismiss=True, # Permite fechar o diálogo clicando fora
            radius=[dp(28), dp(28), dp(28), dp(28)], # Arredondamento dos cantos
        )

        self.dialog.open()

    # Cria e retorna o ScreenManager
        sm = MyScreenManager()
        sm.add_widget(Screen(name='login')) # Adiciona a tela de login (o Kivy carrega login.kv)
        sm.add_widget(Screen(name='funcionario')) # Adiciona a tela de funcionario (o Kivy carrega funcionario.kv)
        sm.add_widget(Screen(name='produto')) # Adiciona a tela de produto (o Kivy carrega produto.kv)
        return sm


if __name__ == '__main__':
    MyApp().run()
