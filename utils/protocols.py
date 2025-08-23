from typing import Protocol
from datetime import timedelta

class CRUDController(Protocol):
    def criar(self, *args, **kwargs): ...
    def ler(self, id): ...
    def atualizar(self, id, *args, **kwargs): ...
    def deletar(self, id): ...


class MensageriaService(Protocol):
    def sendWhatmsg(self, destinatario: str, mensagem: str) -> bool: ...

    # Verificar data para mensagem de lembrete.
    def calcular_data_aviso(data_vencimento):
        
        dias_antecedencia = timedelta(days=3)
        data_aviso = data_vencimento - dias_antecedencia
        return data_aviso

        