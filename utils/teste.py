
from whatsapService import Whatsap
from datetime import date



data_pagamento = date(2025, 6, 19) 
phone_no = "+5534992990237"
message = "E o pix?? nada ainda?? Desculpe num é hoje não, é daqui 3 dias. Isto é um teste Uid Software."
hour = 21
minute = 35

# Crio instaciacao por conter self, que é um metodo de instancia.
# 1. Criar uma instância de Whatsap
whatsapp_sender = Whatsap()

# 2. Chamar o método lembrarPagamento na instância
whatsapp_sender.remember_payment(data_pagamento, phone_no, message, hour, minute)