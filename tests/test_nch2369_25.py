import sys
from pathlib import Path

import pytest

# Agregar la carpeta src al path para permitir las importaciones
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# Importar usando la notación de módulo con guión
import importlib
nch = importlib.import_module("nch2369-25.nch2369-25")
parametros_suelo = nch.parametros_suelo
coeficiente_importancia = nch.coeficiente_importancia
coeficiente_aceleración = nch.coeficiente_aceleración


class TestParametrosSuelo:
    """Tests para verificar los parámetros del suelo según NCh2369-25"""
    
    def test_parametros_suelo_tipo_a(self):
        """Verifica que los parámetros del suelo tipo A correspondan con la norma"""
        params = parametros_suelo('A')
        assert params['S'] == 0.90
        assert params['r'] == 4.50
        assert params['T_0'] == 0.15
        assert params['p'] == 1.85
        assert params['q'] == 3.00
        assert params['T1'] == 0.15
    
    def test_parametros_suelo_tipo_b(self):
        """Verifica que los parámetros del suelo tipo B correspondan con la norma"""
        params = parametros_suelo('B')
        assert params['S'] == 1.00
        assert params['r'] == 4.50
        assert params['T_0'] == 0.30
        assert params['p'] == 1.60
        assert params['q'] == 3.00
        assert params['T1'] == 0.27
    
    def test_parametros_suelo_tipo_c(self):
        """Verifica que los parámetros del suelo tipo C correspondan con la norma"""
        params = parametros_suelo('C')
        assert params['S'] == 1.05
        assert params['r'] == 4.50
        assert params['T_0'] == 0.40
        assert params['p'] == 1.50
        assert params['q'] == 3.00
        assert params['T1'] == 0.35
    
    def test_parametros_suelo_tipo_d(self):
        """Verifica que los parámetros del suelo tipo D correspondan con la norma"""
        params = parametros_suelo('D')
        assert params['S'] == 1.00
        assert params['r'] == 3.50
        assert params['T_0'] == 0.60
        assert params['p'] == 1.00
        assert params['q'] == 2.50
        assert params['T1'] == 0.41
    
    def test_parametros_suelo_tipo_e(self):
        """Verifica que los parámetros del suelo tipo E correspondan con la norma"""
        params = parametros_suelo('E')
        assert params['S'] == 1.00
        assert params['r'] == 3.00
        assert params['T_0'] == 1.20
        assert params['p'] == 1.00
        assert params['q'] == 2.70
        assert params['T1'] == 0.79
    
    def test_parametros_suelo_tipo_invalido(self):
        """Verifica que levanta excepción con tipo de suelo inválido"""
        with pytest.raises(KeyError):
            parametros_suelo('Z')


class TestCoeficienteImportancia:
    """Tests para el coeficiente de importancia"""
    
    def test_coeficiente_importancia_i(self):
        assert coeficiente_importancia('I') == 1.0
    
    def test_coeficiente_importancia_ii(self):
        assert coeficiente_importancia('II') == 1.0
    
    def test_coeficiente_importancia_iii(self):
        assert coeficiente_importancia('III') == 1.2
    
    def test_coeficiente_importancia_iv(self):
        assert coeficiente_importancia('IV') == 1.4


class TestCoeficienteAceleración:
    """Tests para el coeficiente de aceleración sísmica"""
    
    def test_coeficiente_aceleración_zona_1(self):
        a_0, a_r = coeficiente_aceleración(1)
        assert a_0 == 0.2
        assert a_r == 0.28  # 1.4 * 0.2
    
    def test_coeficiente_aceleración_zona_2(self):
        a_0, a_r = coeficiente_aceleración(2)
        assert a_0 == 0.3
        assert a_r == 0.42  # 1.4 * 0.3
    
    def test_coeficiente_aceleración_zona_3(self):
        a_0, a_r = coeficiente_aceleración(3)
        assert a_0 == 0.4
        assert a_r == 0.56  # 1.4 * 0.4
