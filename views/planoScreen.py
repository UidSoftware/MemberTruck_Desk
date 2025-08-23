# Arquivo: views/planoScreen.py
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from controllers.planoControl import PlanoControl

Builder.load_file('views/planoScreen.kv')

class PlanoScreen(MDScreen):
    """
    Tela de cadastro de planos.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.controller = PlanoControl(view=self)
