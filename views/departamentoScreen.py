# Arquivo: views/departamentoScreen.py
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from controllers.departamentoControl import DepartamentoControl

Builder.load_file('views/departamentoScreen.kv')

class DepartamentoScreen(MDScreen):
    """
    Tela de cadastro de Departamento.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.controller = DepartamentoControl(view=self)
