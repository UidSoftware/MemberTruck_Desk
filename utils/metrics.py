# utils/metrics.py
import time
from functools import wraps
from .logger import KivyLogger

# Instancia o logger uma vez no módulo
logger = KivyLogger().logger 

class PerformanceMetrics:
    def __init__(self):
     self.metrics = {}

    def measure_time(self, operation_name):
        """Decorator para medir tempo de execução"""

        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time.time()
                result = func(*args, **kwargs)
                end_time = time.time()

                execution_time = end_time - start_time
                if operation_name not in self.metrics:
                    self.metrics[operation_name] = []

                self.metrics[operation_name].append(execution_time)

                # Log se a operação demorar mais que 2 segundos
                if execution_time > 2.0:
                    logger.warning(f"Operação lenta detectada: {operation_name} - {execution_time:.2f}s")
                return result
            return wrapper
        return decorator
    def get_average_time(self, operation_name):
        """Retorna tempo médio de uma operação"""
        if operation_name in self.metrics:
            times = self.metrics[operation_name]
            return sum(times) / len(times)
        return 0