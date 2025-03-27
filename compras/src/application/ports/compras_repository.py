from abc import ABC, abstractmethod
from typing import List
from src.domain.models.compra import Compra

class CompraRepository(ABC):
    @abstractmethod
    def guardar(self, compra: Compra) -> Compra:
        pass

    @abstractmethod
    def listar_todas(self) -> List[Compra]:
        pass