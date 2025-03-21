#Test unitario de prueba para validar configuracion de pytest dentro del proyecto
from app.logic import suma_for_test

def test_suma_for_test():
    assert suma_for_test(1, 2) == 4