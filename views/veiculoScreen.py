# Arquivo: views/veiculoScreen.py
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from controllers.veiculoControl import VeiculoControl

Builder.load_file('views/veiculoScreen.kv')

class VeiculoScreen(MDScreen):
    """
    Tela de cadastro de veículos.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.controller = VeiculoControl(view=self)
