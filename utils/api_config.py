# utils/api_config.py
class APIConfig:
    BASE_URL = "http://31.97.240.156:8888" # Usar nginx proxy
    ENDPOINTS = {
        'login': '/api/login/',
        'associados': '/api/associados/',
        'funcionarios': '/api/funcionarios/',
    }
    @classmethod
    def get_url(cls, endpoint):
        return f"{cls.BASE_URL}{cls.ENDPOINTS[endpoint]}"
    @classmethod
    def format_login_payload(cls, username, password):
        return {
            'usuarioPess': username,
            'password': password
        }