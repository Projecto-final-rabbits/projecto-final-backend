#Test unitario de prueba para validar configuracion de pytest dentro del proyecto
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.application.services.logic import suma_for_test

def test_suma_for_test():
    assert suma_for_test(1, 2) == 3