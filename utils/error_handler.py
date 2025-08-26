# utils/error_handler.py
import requests
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
class ErrorHandler:
    @staticmethod
    def handle_api_error(response, error_label=None):
        """Trata erros de API de forma padronizada"""
        error_messages = {
            400: "Dados inválidos. Verifique as informações inseridas.",
            401: "Credenciais inválidas. Verifique usuário e senha.",
            403: "Acesso negado. Você não tem permissão para esta ação.",
            404: "Recurso não encontrado. Verifique a URL da API.",
            500: "Erro interno do servidor. Tente novamente mais tarde.",
            502: "Servidor indisponível. Verifique a conexão.",
            503: "Serviço temporariamente indisponível."
        }
        status_code = response.status_code
        message = error_messages.get(status_code, f"Erro desconhecido:{status_code}")

        if error_label:
            error_label.text = message
        return message
    
    @staticmethod
    def handle_connection_error(exception, error_label=None):
        """Trata erros de conexão"""
        if isinstance(exception, requests.exceptions.ConnectionError):
            message = "Não foi possível conectar ao servidor. Verifique sua conexão."
        elif isinstance(exception, requests.exceptions.Timeout):
            message = "Tempo limite de conexão excedido. Tente novamente."
        elif isinstance(exception, requests.exceptions.SSLError):
            message = "Erro de certificado SSL. Verifique a configuração do servidor."
        else:
            message = f"Erro de conexão: {str(exception)}"
        if error_label:
            error_label.text = message
        return message