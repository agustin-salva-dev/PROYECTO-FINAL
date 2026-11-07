import sys
import os

# Asegura que la raíz del proyecto esté en el path de búsqueda
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.repositories.lote_repository import LoteRepository


class InventarioController:
    """
    Controlador para consultas y estado del inventario.
    Desacopla la Vista de la persistencia y expone métricas y listas para la UI.
    """

    def __init__(self):
        self.lote_repo = LoteRepository()

    def obtener_alertas_stock_critico(self) -> list:
        """Retorna medicamentos que requieren reposición urgente."""
        return self.lote_repo.obtener_alertas_stock_critico()

    def obtener_lotes_proximos_a_vencer(self, dias: int = 180) -> list:
        """Retorna lotes en riesgo de vencimiento bajo política FEFO."""
        return self.lote_repo.obtener_proximos_a_vencer(dias)

    def obtener_lotes_disponibles_para_venta(self) -> list:
        """Retorna los lotes activos y no vencidos aptos para venta en la UI."""
        return self.lote_repo.obtener_disponibles_venta()
