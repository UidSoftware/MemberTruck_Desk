# Arquivo: views/enderecoScreen.py
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from controllers.enderecoControl import EnderecoControl

Builder.load_file('views/enderecoScreen.kv')

class EnderecoScreen(MDScreen):
    """
    Tela de cadastro de endereços.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.controller = EnderecoControl(view=self)
