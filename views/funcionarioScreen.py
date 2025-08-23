# Arquivo: views/funcionarioScreen.py
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from controllers.funcionarioControl import FuncionarioControl

Builder.load_file('views/funcionarioScreen.kv')

class FuncionarioScreen(MDScreen):
    """
    Tela de cadastro de Funcionário.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.controller = FuncionarioControl(view=self)
        self.selected_endereco_id = None # Atributo para armazenar o ID do endereço selecionado

    def show_endereco_screen(self):
        """
        Método para navegar para a tela de endereço para seleção.
        """
        # Supondo que você tenha um Gerenciador de Telas na sua aplicação principal
        # e que a tela de Endereco se chame 'endereco'.
        self.manager.current = 'endereco'
