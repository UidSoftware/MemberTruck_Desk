# Arquivo: controllers/enderecoControl.py
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.snackbar import MDSnackbar
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivy.core.window import Window
from requests_futures.sessions import FuturesSession
from concurrent.futures import as_completed

from utils.protocols import CRUDController 

class EnderecoControl(CRUDController):
    """
    Controller para a tela de Endereços.
    Lida com a lógica de negócio para interagir com o backend Django.
    """
    URL_BASE_API = "http://31.97.240.156:8000/api/enderecos/"

    def __init__(self, view):
        self.view = view
        self.session = FuturesSession()

    def criar(self, *args, **kwargs):
        data = {
            "cepEnde": self.view.ids.endereco_cepEnde.text,
            "nomeEnde": self.view.ids.endereco_nomeEnde.text,
            "numeroEnde": self.view.ids.endereco_numeroEnde.text,
            "complementoEnde": self.view.ids.endereco_complementoEnde.text,
            "bairroEnde": self.view.ids.endereco_bairroEnde.text,
            "cidadeEnde": self.view.ids.endereco_cidadeEnde.text,
        }
        if not data["cepEnde"] or not data["nomeEnde"]:
            self.show_snackbar("Erro: CEP e Nome são obrigatórios.")
            return

        try:
            future = self.session.post(self.URL_BASE_API, json=data)
            future.add_done_callback(lambda f: self._handle_response_criar(f))
        except Exception as e:
            self.show_snackbar(f"Erro de conexão com a API: {e}")

    def _handle_response_criar(self, future):
        try:
            response = future.result()
            if response.status_code == 201:
                self.show_snackbar("Endereço criado com sucesso!")
                self.clear_form()
            else:
                self.show_snackbar(f"Erro na criação: {response.status_code}")
        except Exception as e:
            self.show_snackbar(f"Erro ao processar a resposta: {e}")
    
    def ler(self, id):
        if not id:
            self.show_snackbar("Erro: ID é obrigatório para a leitura.")
            return
        try:
            future = self.session.get(f"{self.URL_BASE_API}{id}/")
            future.add_done_callback(lambda f: self._handle_response_ler(f))
        except Exception as e:
            self.show_snackbar(f"Erro de conexão com a API: {e}")

    def _handle_response_ler(self, future):
        try:
            response = future.result()
            if response.status_code == 200:
                data = response.json()
                self.view.ids.endereco_cepEnde.text = data.get("cepEnde", "")
                self.view.ids.endereco_nomeEnde.text = data.get("nomeEnde", "")
                self.view.ids.endereco_numeroEnde.text = data.get("numeroEnde", "")
                self.view.ids.endereco_complementoEnde.text = data.get("complementoEnde", "")
                self.view.ids.endereco_bairroEnde.text = data.get("bairroEnde", "")
                self.view.ids.endereco_cidadeEnde.text = data.get("cidadeEnde", "")
                self.show_snackbar("Endereço carregado.")
            else:
                self.show_snackbar(f"Erro na leitura: {response.status_code}")
        except Exception as e:
            self.show_snackbar(f"Erro ao processar a resposta: {e}")

    def atualizar(self, id):
        if not id:
            self.show_snackbar("Erro: ID é obrigatório para a atualização.")
            return
        data = {
            "cepEnde": self.view.ids.endereco_cepEnde.text,
            "nomeEnde": self.view.ids.endereco_nomeEnde.text,
            "numeroEnde": self.view.ids.endereco_numeroEnde.text,
            "complementoEnde": self.view.ids.endereco_complementoEnde.text,
            "bairroEnde": self.view.ids.endereco_bairroEnde.text,
            "cidadeEnde": self.view.ids.endereco_cidadeEnde.text,
        }
        try:
            future = self.session.put(f"{self.URL_BASE_API}{id}/", json=data)
            future.add_done_callback(lambda f: self._handle_response_atualizar(f))
        except Exception as e:
            self.show_snackbar(f"Erro de conexão com a API: {e}")

    def _handle_response_atualizar(self, future):
        try:
            response = future.result()
            if response.status_code == 200:
                self.show_snackbar("Endereço atualizado com sucesso!")
                self.clear_form()
            else:
                self.show_snackbar(f"Erro na atualização: {response.status_code}")
        except Exception as e:
            self.show_snackbar(f"Erro ao processar a resposta: {e}")

    def deletar(self, id):
        if not id:
            self.show_snackbar("Erro: ID é obrigatório para a exclusão.")
            return
        try:
            future = self.session.delete(f"{self.URL_BASE_API}{id}/")
            future.add_done_callback(lambda f: self._handle_response_deletar(f))
        except Exception as e:
            self.show_snackbar(f"Erro de conexão com a API: {e}")

    def _handle_response_deletar(self, future):
        try:
            response = future.result()
            if response.status_code == 204:
                self.show_snackbar("Endereço excluído com sucesso!")
                self.clear_form()
            else:
                self.show_snackbar(f"Erro na exclusão: {response.status_code}")
        except Exception as e:
            self.show_snackbar(f"Erro ao processar a resposta: {e}")

    def clear_form(self):
        self.view.ids.endereco_cepEnde.text = ""
        self.view.ids.endereco_nomeEnde.text = ""
        self.view.ids.endereco_numeroEnde.text = ""
        self.view.ids.endereco_complementoEnde.text = ""
        self.view.ids.endereco_bairroEnde.text = ""
        self.view.ids.endereco_cidadeEnde.text = ""
    
    def show_snackbar(self, text):
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
