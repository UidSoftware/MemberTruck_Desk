# Arquivo: controllers/cargoControl.py
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.snackbar import MDSnackbar
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivy.core.window import Window
from requests_futures.sessions import FuturesSession
from concurrent.futures import as_completed

from utils.protocols import CRUDController

class CargoControl(CRUDController):
    """
    Controller para a tela de Cargo.
    Lida com a lógica de negócio para interagir com o backend Django.
    """
    
    # URL base da sua API Django.
    URL_BASE_API = "http://31.97.240.156:8888/api/Cargo/"
    
    def __init__(self, view):
        """
        Construtor do controller. Recebe a instância da view.
        
        Args:
            view (CargoScreen): A instância da view (tela) CargoScreen.
        """
        self.view = view
        self.session = FuturesSession() # Sessão de requisições assíncronas

    def criar(self, *args, **kwargs):
        """
        Coleta os dados do formulário e cria um novo cargo no backend.
        """
        cargo_data = {
            "nomeCarg": self.view.ids.nome_cargo_field.text,
            "descricaoCarg": self.view.ids.descricao_cargo_field.text,
        }
        
        if not cargo_data["nomeCarg"]:
            self.show_snackbar("Erro: O nome do cargo é obrigatório.")
            return

        print("Enviando dados para criação de cargo...")
        try:
            future = self.session.post(f"{self.URL_BASE_API}Cargo/", json=cargo_data)
            future.add_done_callback(lambda f: self._handle_response_criar(f))
        except Exception as e:
            print(f"Erro ao tentar conectar com a API: {e}")
            self.show_snackbar(f"Erro de conexão com a API: {e}")

    def _handle_response_criar(self, future):
        """
        Callback para processar a resposta da requisição POST de criação.
        """
        try:
            response = future.result()
            if response.status_code == 201:
                self.show_snackbar("Cargo criado com sucesso!")
                self.clear_form()
            else:
                print(f"Erro na criação: {response.text}")
                self.show_snackbar(f"Erro na criação: {response.status_code}")
        except Exception as e:
            print(f"Erro ao processar a resposta da API: {e}")
            self.show_snackbar(f"Erro ao processar a resposta: {e}")

    def ler_todos(self):
        """
        Lógica para ler todos os cargos do backend.
        """
        pass

    def ler(self, id):
        """
        Lógica para ler dados de um cargo a partir do seu ID.
        """
        if not id:
            self.show_snackbar("Erro: ID é obrigatório para a leitura.")
            return

        print(f"Buscando cargo com ID: {id}...")
        try:
            future = self.session.get(f"{self.URL_BASE_API}Cargo/{id}/")
            future.add_done_callback(lambda f: self._handle_response_ler(f, id))
        except Exception as e:
            print(f"Erro ao tentar conectar com a API: {e}")
            self.show_snackbar(f"Erro de conexão com a API: {e}")

    def _handle_response_ler(self, future, id):
        """
        Callback para processar a resposta da requisição GET de leitura.
        """
        try:
            response = future.result()
            if response.status_code == 200:
                data = response.json()
                self.view.ids.id_cargo_field.text = str(data.get("idCarg", ""))
                self.view.ids.nome_cargo_field.text = data.get("nomeCarg", "")
                self.view.ids.descricao_cargo_field.text = data.get("descricaoCarg", "")

                self.show_snackbar(f"Cargo com ID {id} carregado.")
            else:
                print(f"Erro na leitura: {response.text}")
                self.show_snackbar(f"Erro na leitura: {response.status_code}")
        except Exception as e:
            print(f"Erro ao processar a resposta da API: {e}")
            self.show_snackbar(f"Erro ao processar a resposta: {e}")

    def atualizar(self, id):
        """
        Lógica para atualizar um cargo existente no backend.
        """
        if not id:
            self.show_snackbar("Erro: ID é obrigatório para a atualização.")
            return

        print(f"Atualizando cargo com ID: {id}...")
        
        cargo_data = {
            "nomeCarg": self.view.ids.nome_cargo_field.text,
            "descricaoCarg": self.view.ids.descricao_cargo_field.text,
        }
        
        try:
            future = self.session.put(f"{self.URL_BASE_API}Cargo/{id}/", json=cargo_data)
            future.add_done_callback(lambda f: self._handle_response_atualizar(f))
        except Exception as e:
            print(f"Erro ao tentar conectar com a API: {e}")
            self.show_snackbar(f"Erro de conexão com a API: {e}")

    def _handle_response_atualizar(self, future):
        """
        Callback para processar a resposta da requisição PUT de atualização.
        """
        try:
            response = future.result()
            if response.status_code == 200:
                self.show_snackbar("Cargo atualizado com sucesso!")
                self.clear_form()
            else:
                print(f"Erro na atualização: {response.text}")
                self.show_snackbar(f"Erro na atualização: {response.status_code}")
        except Exception as e:
            print(f"Erro ao processar a resposta da API: {e}")
            self.show_snackbar(f"Erro ao processar a resposta: {e}")
    
    def deletar(self, id):
        """
        Lógica para excluir um cargo do backend.
        """
        if not id:
            self.show_snackbar("Erro: ID é obrigatório para a exclusão.")
            return

        print(f"Deletando cargo com ID: {id}...")
        try:
            future = self.session.delete(f"{self.URL_BASE_API}Cargo/{id}/")
            future.add_done_callback(lambda f: self._handle_response_deletar(f))
        except Exception as e:
            print(f"Erro ao tentar conectar com a API: {e}")
            self.show_snackbar(f"Erro de conexão com a API: {e}")

    def _handle_response_deletar(self, future):
        """
        Callback para processar a resposta da requisição DELETE de exclusão.
        """
        try:
            response = future.result()
            if response.status_code == 204: # 204 No Content é o esperado para DELETE
                self.show_snackbar("Cargo excluído com sucesso!")
                self.clear_form()
            else:
                print(f"Erro na exclusão: {response.text}")
                self.show_snackbar(f"Erro na exclusão: {response.status_code}")
        except Exception as e:
            print(f"Erro ao processar a resposta da API: {e}")
            self.show_snackbar(f"Erro ao processar a resposta: {e}")
    
    def clear_form(self):
        """
        Limpa todos os campos do formulário.
        """
        self.view.ids.id_cargo_field.text = ""
        self.view.ids.nome_cargo_field.text = ""
        self.view.ids.descricao_cargo_field.text = ""

    def show_snackbar(self, text):
        """
        Exibe um SnackBar para mensagens de feedback ao usuário.
        """
        window_width = Window.width
        MDSnackbar(
            MDBoxLayout(
                MDLabel(
                    text=text,
                    halign="center",
                    adaptive_width=True,
                    font_style="Body1",
                    theme_text_color="Custom",
                    text_color="black"
                ),
                padding="8dp",
                spacing="8dp",
            ),
            y="24dp",
            pos_hint={'center_x': 0.5},
            size_hint_x=0.8,
            md_bg_color="#AFEEEE",
            duration=2.5
        ).open()
