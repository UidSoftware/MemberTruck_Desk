from pessoa import Pessoa

class Funcionario(Pessoa):

    def __init__(self, id, nome, telefone, documento, nascimento, email, senha, usuario, salario, comicao, dataAdmissao):
        super().__init__(id ,nome, telefone, documento, nascimento, email, senha, usuario)
        
        self.salario = salario
        self.comicao = comicao
        self.dataAdmissao = dataAdmissao
    
    def __str__(self):

        return f"O salario: {self.salario}, recebe: {self.comicao} de comição, e foi contratado desde: {self.dataAdmissao}."
