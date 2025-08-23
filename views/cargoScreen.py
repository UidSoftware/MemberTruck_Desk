# Arquivo: views/cargoScreen.py
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from controllers.cargoControl import CargoControl

Builder.load_file('views/cargoScreen.kv')

class CargoScreen(MDScreen):
    """
    Tela de cadastro de Cargo.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.controller = CargoControl(view=self)
