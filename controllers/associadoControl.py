# Arquivo: controllers/associadoControl.py
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.snackbar import MDSnackbar
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.list import MDListItem, MDListItemHeadlineText
from kivy.core.window import Window
from kivy.clock import Clock

from requests_futures.sessions import FuturesSession
from concurrent.futures import as_completed
from functools import partial
import json

from utils.protocols import CRUDController 

class AssociadoControl(CRUDController):
    """
    Controller para a tela de Associados.
    Lida com a lógica de negócio para interagir com o backend Django, gerenciando 
    as operações de CRUD e os dropdowns.
    """
    
    # URL base da sua API Django.
    URL_BASE_API = "http://31.97.240.156:8888/api/"
    
    def __init__(self, view):
        """
        Construtor do controller. Recebe a instância da view para interagir com a interface.
        
        Args:
            view (AssociadoScreen): A instância da view (tela) AssociadoScreen.
        """
        self.view = view
        self.plano_menu = None
        self.veiculo_menu = None
        self.planos_data = []
        self.veiculos_data = []
        self.session = FuturesSession() # Cria uma sessão de requisições assíncronas
        
        

    # Lógica de login
    def on_login_success(self, token):
        """
        Este método é chamado após o login ser bem-sucedido.
        Ele configura a sessão com o token de autenticação.
        """
        # 1. Cria a sessão HTTP
        self.session = requests.Session()
        
        # 2. Adiciona o token de autenticação no cabeçalho
        # O formato do cabeçalho pode variar (Bearer, Token, etc.).
        # Verifique a documentação da sua API.
        headers = {'Authorization': f'Bearer {token}'}
        self.session.headers.update(headers)

        # 3. Agora que a sessão está configurada,
        # você pode agendar a busca dos dados
        Clock.schedule_once(self.fetch_and_setup_dropdowns)

    def fetch_and_setup_dropdowns(self, dt):
        """
        Busca os dados para os dropdowns de forma assíncrona e os configura.
        Este método é chamado via Clock.schedule_once para garantir que a view
        e seus widgets (com IDs) já existam.
        """
        print("Buscando dados para dropdowns...")
        futures = {
            self.session.get(f"{self.URL_BASE_API}Plano/"): "Plano",
            self.session.get(f"{self.URL_BASE_API}Veiculo/"): "Veiculo"
        }
        
        for future in as_completed(futures):
            key = futures[future]
            try:
                response = future.result()
                if response.status_code == 200:
                    data = response.json()
                    if key == "Plano":
                        self.planos_data = data
                        self.setup_plano_menu()
                    elif key == "Veiculo":
                        self.veiculos_data = data
                        self.setup_veiculo_menu()
                else:
                    self.show_snackbar(f"Erro ao buscar {key}: {response.status_code}")
                    print(f"Erro ao buscar {key}: {response.text}")
            except Exception as e:
                self.show_snackbar(f"Erro de conexão ao buscar {key}: {e}")
                print(f"Erro de conexão ao buscar {key}: {e}")
        
        print("Dados para dropdowns carregados e menus configurados.")

    def setup_plano_menu(self):
        """
        Prepara o MDDropdownMenu para o campo de plano com os dados da API.
        """
        menu_items = [
            {
                "text": plano['nomePlan'],
                "on_release": lambda x, p_id=plano['idPlan']: self.set_plano(x.text, p_id),
            } for plano in self.planos_data
        ]
        self.plano_menu = MDDropdownMenu(
            caller=self.view.ids.plano_field,
            items=menu_items,
            width_mult=4,
        )

    def setup_veiculo_menu(self):
        """
        Prepara o MDDropdownMenu para o campo de veículo com os dados da API.
        """
        menu_items = [
            {
                "text": veiculo['nomeVeic'],
                "on_release": lambda x, v_id=veiculo['idVeic']: self.set_veiculo(x.text, v_id),
            } for veiculo in self.veiculos_data
        ]
        self.veiculo_menu = MDDropdownMenu(
            caller=self.view.ids.veiculo_associado_field,
            items=menu_items,
            width_mult=4,
        )

    def open_plano_menu(self):
        """
        Abre o dropdown menu de planos.
        """
        if self.plano_menu:
            self.plano_menu.open()

    def open_veiculo_menu(self):
        """
        Abre o dropdown menu de veículos.
        """
        if self.veiculo_menu:
            self.veiculo_menu.open()

    def set_plano(self, text_item, plano_id):
        """
        Define o texto do campo de plano com o item selecionado do menu.
        """
        self.view.ids.plano_field.text = text_item
        self.view.selected_plano_id = plano_id
        self.plano_menu.dismiss()

    def set_veiculo(self, text_item, veiculo_id):
        """
        Define o texto do campo de veículo com o item selecionado do menu.
        """
        self.view.ids.veiculo_associado_field.text = text_item
        self.view.selected_veiculo_id = veiculo_id
        self.veiculo_menu.dismiss()
    
    def criar(self, *args, **kwargs):
        """
        Coleta os dados do formulário e cria um novo associado no backend.
        """
        # Verifique se o ID do plano e do veículo foram selecionados
        if not self.view.selected_plano_id or not self.view.selected_veiculo_id:
            self.show_snackbar("Erro: Selecione um Plano e um Veículo.")
            return

        # Coleta os dados do associado/pessoa
        associado_data = {
            "nomePess": self.view.ids.nome_associado_field.text,
            "telefonePess": self.view.ids.telefone_associado_field.text,
            "documentoPess": self.view.ids.documento_associado_field.text,
            "nascimentoPess": self.view.ids.nascimento_associado_field.text,
            "emailPess": self.view.ids.email_associado_field.text,
            "usuarioPess": self.view.ids.usuario_associado_field.text,
            "password": self.view.ids.senha_associado_field.text,
            "idPlanAsso": self.view.selected_plano_id,
            "consultor": self.view.selected_consultor_id,  # Se aplicável
}
        
        # Opcional: Adicionar o ID do endereço se já foi selecionado
        if self.view.selected_endereco_id:
            associado_data['endereco'] = self.view.selected_endereco_id
        
        if not associado_data["nomePess"] or not associado_data["documentoPess"] or not associado_data["usuarioPess"] or not associado_data["password"]:
            self.show_snackbar("Erro: Campos obrigatórios não preenchidos.")
            return

        print("Enviando dados para criação de associado...")
        try:
            future = self.session.post(f"{self.URL_BASE_API}associados/completo/", json=associado_data)
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
                self.show_snackbar("Associado criado com sucesso!")
                self.clear_form()
                # Opcional: Atualizar lista ou redirecionar
            else:
                print(f"Erro na criação: {response.text}")
                self.show_snackbar(f"Erro na criação: {response.status_code}")
        except Exception as e:
            print(f"Erro ao processar a resposta da API: {e}")
            self.show_snackbar(f"Erro ao processar a resposta: {e}")

    def ler_todos(self):
        """
        Lógica para ler todos os associados do backend e popular a lista.
        """
        print("Buscando todos os associados...")
        try:
            future = self.session.get(f"{self.URL_BASE_API}associados/")
            future.add_done_callback(lambda f: self._handle_response_ler_todos(f))
        except Exception as e:
            print(f"Erro ao tentar conectar com a API: {e}")
            self.show_snackbar(f"Erro de conexão com a API: {e}")
    
    def _handle_response_ler_todos(self, future):
        """
        Callback para processar a resposta da requisição GET de todos os associados.
        """
        try:
            response = future.result()
            if response.status_code == 200:
                data = response.json()
                self.view.populate_associado_list(data)
                self.show_snackbar("Lista de associados carregada.")
            else:
                print(f"Erro na leitura da lista: {response.text}")
                self.show_snackbar(f"Erro na leitura da lista: {response.status_code}")
        except Exception as e:
            print(f"Erro ao processar a resposta da API: {e}")
            self.show_snackbar(f"Erro ao processar a resposta: {e}")

    def ler(self, id):
        """
        Lógica para ler dados de um associado a partir do seu ID.
        """
        if not id:
            self.show_snackbar("Erro: ID é obrigatório para a leitura.")
            return

        print(f"Buscando associado com ID: {id}...")
        try:
            future = self.session.get(f"{self.URL_BASE_API}associados/{id}/")
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
                # Preencher o formulário com os dados do associado
                self.view.ids.id_associado_field.text = str(data.get("idAsso", ""))
                self.view.ids.nome_associado_field.text = data.get("nomePess", "")
                self.view.ids.telefone_associado_field.text = data.get("telefonePess", "")
                self.view.ids.documento_associado_field.text = data.get("documentoPess", "")
                self.view.ids.nascimento_associado_field.text = data.get("nascimentoPess", "")
                self.view.ids.email_associado_field.text = data.get("emailPess", "")
                self.view.ids.usuario_associado_field.text = data.get("usuarioPess", "")
                self.view.ids.plano_field.text = data.get("plano", {}).get("nomePlan", "")
                self.view.ids.veiculo_associado_field.text = data.get("idVeicAsso", {}).get("nomeVeic", "")
                
                # Armazenar os IDs para futuras operações
                self.view.selected_plano_id = data.get("plano", {}).get("idPlan", None)
                self.view.selected_veiculo_id = data.get("idVeicAsso", {}).get("idVeic", None)
                self.view.selected_endereco_id = data.get("endereco", {}).get("idEnde", None)
                
                # Atualizar o campo do endereço para exibir o ID
                if self.view.selected_endereco_id:
                    self.view.ids.endereco_associado_field.text = str(self.view.selected_endereco_id)

                self.show_snackbar(f"Associado com ID {id} carregado.")
            else:
                print(f"Erro na leitura: {response.text}")
                self.show_snackbar(f"Erro na leitura: {response.status_code}")
        except Exception as e:
            print(f"Erro ao processar a resposta da API: {e}")
            self.show_snackbar(f"Erro ao processar a resposta: {e}")

    def atualizar(self, id):
        """
        Lógica para atualizar um associado existente no backend.
        """
        if not id:
            self.show_snackbar("Erro: ID é obrigatório para a atualização.")
            return

        print(f"Atualizando associado com ID: {id}...")
        
        associado_data = {
            "nomePess": self.view.ids.nome_associado_field.text,
            "telefonePess": self.view.ids.telefone_associado_field.text,
            "documentoPess": self.view.ids.documento_associado_field.text,
            "nascimentoPess": self.view.ids.nascimento_associado_field.text,
            "emailPess": self.view.ids.email_associado_field.text,
            "usuarioPess": self.view.ids.usuario_associado_field.text,
            "password": self.view.ids.senha_associado_field.text,
            "idPlanAsso": self.view.selected_plano_id,
            "consultor": self.view.selected_consultor_id,  # Se aplicável
}

        # Adiciona o ID do endereço à requisição se ele existir
        if self.view.selected_endereco_id:
            associado_data['endereco'] = self.view.selected_endereco_id
        
        try:
            future = self.session.put(f"{self.URL_BASE_API}associados/{id}/", json=associado_data)
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
                self.show_snackbar("Associado atualizado com sucesso!")
                self.clear_form()
            else:
                print(f"Erro na atualização: {response.text}")
                self.show_snackbar(f"Erro na atualização: {response.status_code}")
        except Exception as e:
            print(f"Erro ao processar a resposta da API: {e}")
            self.show_snackbar(f"Erro ao processar a resposta: {e}")
    
    def deletar(self, id):
        """
        Lógica para excluir um associado do backend.
        """
        if not id:
            self.show_snackbar("Erro: ID é obrigatório para a exclusão.")
            return

        print(f"Deletando associado com ID: {id}...")
        try:
            future = self.session.delete(f"{self.URL_BASE_API}associados/{id}/")
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
                self.show_snackbar("Associado excluído com sucesso!")
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
        self.view.ids.id_associado_field.text = ""
        self.view.ids.nome_associado_field.text = ""
        self.view.ids.telefone_associado_field.text = ""
        self.view.ids.documento_associado_field.text = ""
        self.view.ids.nascimento_associado_field.text = ""
        self.view.ids.email_associado_field.text = ""
        self.view.ids.usuario_associado_field.text = ""
        self.view.ids.senha_associado_field.text = ""
        self.view.ids.plano_field.text = ""
        self.view.ids.veiculo_associado_field.text = ""
        self.view.ids.endereco_associado_field.text = ""
        self.view.selected_plano_id = None
        self.view.selected_veiculo_id = None
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
