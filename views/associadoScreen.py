# Arquivo: views/associadoScreen.py
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from controllers.associadoControl import AssociadoControl

Builder.load_file('views/associadoScreen.kv')

class AssociadoScreen(MDScreen):
    """
    Tela de cadastro de Associado.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.controller = AssociadoControl(view=self)
        self.selected_plano_id = None
        self.selected_veiculo_id = None
