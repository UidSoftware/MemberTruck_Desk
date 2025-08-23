from protocols import MensageriaService
from datetime import datetime
import pywhatkit as kit


# whatsapp_service.py
class Whatsap(MensageriaService):
    # Lembrar e enviar mensagem de Pagamento
    def remember_payment(self, date_pagamento, phone_no, message, hour, minute):

        today_date = datetime.now()
        data_aviso = MensageriaService.calcular_data_aviso(date_pagamento)

        if(data_aviso == today_date.date()):
           print(f"Enviando mensagem pelo WhatsApp.")
           kit.sendwhatmsg(phone_no, message, hour, minute, tab_close=True)
           print(f"Mensagem enviada pelo WhatsApp.")
        else:
            print("Não é a data.") # Arrumar para nao finalizar o sistema...................................

    # Enviar mensagens instantaneas.
    def sendWhatmsg_Instantly(phone_no, message):
        try:
            kit.sendwhatmsg_instantly(phone_no, message)
            print("Mensagem enviada pelo WhatsApp.")
            return True
        except Exception as e:
            print(f"Erro ao enviar mensagem pelo WhatsApp: {e}")
            return False
    