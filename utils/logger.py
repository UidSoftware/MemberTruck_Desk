# utils/logger.py
import logging
import json
from datetime import datetime

class KivyLogger:
    def __init__(self, name="MemberTruck"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)

        # Handler para arquivo
        file_handler = logging.FileHandler('logs/app.log')
        file_handler.setLevel(logging.INFO)

        # Handler para console
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)

        # Formatter estruturado
        formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def log_api_request(self, method, url, payload=None, response=None):

        """Log estruturado para requisições API"""
        log_data = {
            'type': 'api_request',
            'method': method,
            'url': url,
            'timestamp': datetime.now().isoformat(),
            'payload_size': len(str(payload)) if payload else 0,
            'response_status': response.status_code if response else None,
            'response_size': len(response.text) if response else 0
        }
        self.logger.info(json.dumps(log_data))

    def log_error(self, error_type, message, context=None):
        
        """Log estruturado para erros"""
        log_data = {
            'type': 'error',
            'error_type': error_type,
            'message': message,
            'context': context or {},
            'timestamp': datetime.now().isoformat()
        }
        self.logger.error(json.dumps(log_data))