from pessoa import Pessoa

class Associado(Pessoa):
    def __init__(self, id, nome, telefone, documento, nascimento, email, senha, dataAtivacao, dataPagamento):
        super().__init__(id, nome, telefone, documento, nascimento, email, senha)
        
        self.dataAtivacao = dataAtivacao
        self.dataPagamento = dataPagamento

    def __str__(self):
        return f"Ativo desde: {self.dataAtivacao}, com pagamento em: {self.dataPagamento}."

    def verificarDataPagamento(self):
        pass