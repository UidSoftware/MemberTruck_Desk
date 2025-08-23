# Arquivo: controllers/funcionarioControl.py
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

class FuncionarioControl(CRUDController):
    """
    Controller para a tela de Funcionários.
    Lida com a lógica de negócio para interagir com o backend Django, gerenciando 
    as operações de CRUD e a relação com Endereço.
    """
    
    # URL base da sua API Django.
    URL_BASE_API = "http://31.97.240.156:8000/api/"
    
    def __init__(self, view):
        """
        Construtor do controller. Recebe a instância da view para interagir com a interface.
        
        Args:
            view (FuncionarioScreen): A instância da view (tela) FuncionarioScreen.
        """
        self.view = view
        self.session = FuturesSession() # Cria uma sessão de requisições assíncronas

    def criar(self, *args, **kwargs):
        """
        Coleta os dados do formulário e cria um novo funcionário no backend.
        """
        funcionario_data = {
            "nomePess": self.view.ids.nome_funcionario_field.text,
            "telefonePess": self.view.ids.telefone_funcionario_field.text,
            "matriculaFunc": self.view.ids.matricula_funcionario_field.text,
            "emailPess": self.view.ids.email_funcionario_field.text,
            "usuarioPess": self.view.ids.usuario_funcionario_field.text,
            "password": self.view.ids.senha_funcionario_field.text,
        }
        
        # Adiciona o ID do endereço à requisição se ele existir
        if self.view.selected_endereco_id:
            funcionario_data['enderecoFunc'] = self.view.selected_endereco_id
        
        if not funcionario_data["nomePess"] or not funcionario_data["matriculaFunc"] or not funcionario_data["usuarioPess"] or not funcionario_data["password"]:
            self.show_snackbar("Erro: Campos obrigatórios não preenchidos.")
            return

        print("Enviando dados para criação de funcionário...")
        try:
            future = self.session.post(f"{self.URL_BASE_API}funcionarios/", json=funcionario_data)
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
                self.show_snackbar("Funcionário criado com sucesso!")
                self.clear_form()
            else:
                print(f"Erro na criação: {response.text}")
                self.show_snackbar(f"Erro na criação: {response.status_code}")
        except Exception as e:
            print(f"Erro ao processar a resposta da API: {e}")
            self.show_snackbar(f"Erro ao processar a resposta: {e}")

    def ler_todos(self):
        """
        Lógica para ler todos os funcionários do backend.
        """
        # Implementação para carregar uma lista de funcionários, se necessário.
        pass

    def ler(self, id):
        """
        Lógica para ler dados de um funcionário a partir do seu ID.
        """
        if not id:
            self.show_snackbar("Erro: ID é obrigatório para a leitura.")
            return

        print(f"Buscando funcionário com ID: {id}...")
        try:
            future = self.session.get(f"{self.URL_BASE_API}funcionarios/{id}/")
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
                # Preencher o formulário com os dados do funcionário
                self.view.ids.id_funcionario_field.text = str(data.get("idFunc", ""))
                self.view.ids.nome_funcionario_field.text = data.get("nomePess", "")
                self.view.ids.telefone_funcionario_field.text = data.get("telefonePess", "")
                self.view.ids.matricula_funcionario_field.text = data.get("matriculaFunc", "")
                self.view.ids.email_funcionario_field.text = data.get("emailPess", "")
                self.view.ids.usuario_funcionario_field.text = data.get("usuarioPess", "")
                
                # Armazenar o ID do endereço e preencher o campo
                self.view.selected_endereco_id = data.get("enderecoFunc", {}).get("idEnde", None)
                if self.view.selected_endereco_id:
                    self.view.ids.endereco_funcionario_field.text = str(self.view.selected_endereco_id)

                self.show_snackbar(f"Funcionário com ID {id} carregado.")
            else:
                print(f"Erro na leitura: {response.text}")
                self.show_snackbar(f"Erro na leitura: {response.status_code}")
        except Exception as e:
            print(f"Erro ao processar a resposta da API: {e}")
            self.show_snackbar(f"Erro ao processar a resposta: {e}")

    def atualizar(self, id):
        """
        Lógica para atualizar um funcionário existente no backend.
        """
        if not id:
            self.show_snackbar("Erro: ID é obrigatório para a atualização.")
            return

        print(f"Atualizando funcionário com ID: {id}...")
        
        funcionario_data = {
            "nomePess": self.view.ids.nome_funcionario_field.text,
            "telefonePess": self.view.ids.telefone_funcionario_field.text,
            "matriculaFunc": self.view.ids.matricula_funcionario_field.text,
            "emailPess": self.view.ids.email_funcionario_field.text,
            "usuarioPess": self.view.ids.usuario_funcionario_field.text,
            "password": self.view.ids.senha_funcionario_field.text,
        }

        # Adiciona o ID do endereço à requisição se ele existir
        if self.view.selected_endereco_id:
            funcionario_data['enderecoFunc'] = self.view.selected_endereco_id
        
        try:
            future = self.session.put(f"{self.URL_BASE_API}funcionarios/{id}/", json=funcionario_data)
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
                self.show_snackbar("Funcionário atualizado com sucesso!")
                self.clear_form()
            else:
                print(f"Erro na atualização: {response.text}")
                self.show_snackbar(f"Erro na atualização: {response.status_code}")
        except Exception as e:
            print(f"Erro ao processar a resposta da API: {e}")
            self.show_snackbar(f"Erro ao processar a resposta: {e}")
    
    def deletar(self, id):
        """
        Lógica para excluir um funcionário do backend.
        """
        if not id:
            self.show_snackbar("Erro: ID é obrigatório para a exclusão.")
            return

        print(f"Deletando funcionário com ID: {id}...")
        try:
            future = self.session.delete(f"{self.URL_BASE_API}funcionarios/{id}/")
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
                self.show_snackbar("Funcionário excluído com sucesso!")
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
        self.view.ids.id_funcionario_field.text = ""
        self.view.ids.nome_funcionario_field.text = ""
        self.view.ids.telefone_funcionario_field.text = ""
        self.view.ids.matricula_funcionario_field.text = ""
        self.view.ids.email_funcionario_field.text = ""
        self.view.ids.usuario_funcionario_field.text = ""
        self.view.ids.senha_funcionario_field.text = ""
        self.view.ids.endereco_funcionario_field.text = ""
        self.view.selected_endereco_id = None

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
