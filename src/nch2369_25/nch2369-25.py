# Librerías necesarias

import numpy as np

def coeficiente_importancia(categoria:str):
        """
        Calcula el coeficiente de importancia basado en la categoría de ocupación.

        Parámetros:
        categoria (str): Categoría de ocupación ('I', 'II', 'III', 'IV')

        Retorna:
        float: Coeficiente de importancia correspondiente a la categoría
        """

        importancia = {
        'I': 0.8,
        'II': 1.0,
        'III': 1.2,
        'IV': 1.2
        }
        
        return importancia[categoria]

def parametros_suelo(tipo_suelo:str):
        """
        Calcula los parámetros del suelo basado en el tipo de suelo.

        Parámetros:
        tipo_suelo (str): Tipo de suelo ('A', 'B', 'C', 'D', 'E')

        Retorna:
        dict: Diccionario con los parámetros S, r, T_0, p, q, T1 correspondientes al tipo
        """
        
        parametros = {
        "A": {"S": 0.90, "r": 4.50, "T_0": 0.15, "p": 1.85, "q": 3.00, "T1": 0.15},
        "B": {"S": 1.00, "r": 4.50, "T_0": 0.30, "p": 1.60, "q": 3.00, "T1": 0.27},
        "C": {"S": 1.05, "r": 4.50, "T_0": 0.40, "p": 1.50, "q": 3.00, "T1": 0.35},
        "D": {"S": 1.00, "r": 3.50, "T_0": 0.60, "p": 1.00, "q": 2.50, "T1": 0.41},
        "E": {"S": 1.00, "r": 3.00, "T_0": 1.20, "p": 1.00, "q": 2.70, "T1": 0.79},
        }
        
        return parametros[tipo_suelo]

def coeficiente_aceleración(zona:int):
        """
        Calcula la aceleración efectiva máxima, y de referencia, del suelo según la zona sísmica.

        Parámetros:
        zona (int): Zona sísmica (1, 2, o 3)

        Retorna:
        float: Aceleración efectiva máxima (A_0) y de referencia (A_r) correspondiente a la zona sísmica
        """
        
        A0 = {
        1: 0.2,
        2: 0.3,
        3: 0.4
        }
        
        A_0 = A0[zona]
        A_r = 1.4 * A_0
        
        return A_0, A_r

def espectro_referencia(tipo_suelo:str, zona:int):
        """
        Calcula el espectro de respuesta de referencia según NCh2369-25.

        Parámetros:
        T (float): Período de vibración estructural (segundos)
        tipo_suelo (str): Tipo de suelo ('A', 'B', 'C', 'D', 'E')
        zona (int): Zona sísmica (1, 2, o 3)

        Retorna:
        float: Valor del espectro de respuesta de diseño de referencia S_d(T)
        """
        
        # Obtener parámetros del suelo
        params = parametros_suelo(tipo_suelo)
        S = params['S']
        r = params['r']
        T_0 = params['T_0']
        p = params['p']
        q = params['q']
        T1 = params['T1']
        
        # Obtener aceleraciones
        A_0, A_r = coeficiente_aceleración(zona)
        
        # Generación de rango de períodos
        T = np.linspace(0, 3, 301)
        
        # Calcular S_aH_TH(T)
        S_aH_TH = np.zeros(len(T))
        for i in range(len(T)):
                S_aH_TH[i] = A_r * S * ((1 + r * (T[i] / T_0) ** p) / (1 + (T[i] / T_0) ** q))
        return S_aH_TH

def espectro_diseno(R:int, xi:float, tipo_suelo:str, zona:int, categoria:str, T_star:float=1.0):
        """
        Calcula el espectro de respuesta de diseño según NCh2369-25.

        Parámetros:
        R (int): Factor de reducción de fuerzas sísmicas
        xi (float): Factor de amortiguamiento
        tipo_suelo (str): Tipo de suelo ('A', 'B', 'C', 'D', 'E')
        zona (int): Zona sísmica (1, 2, o 3)
        categoria (str): Categoría de ocupación ('I', 'II', 'III', 'IV')
        T_star (float): Período de vibración estructural (segundos)

        Retorna:
        float: Valor del espectro de respuesta de diseño S_d(T)
        """
        
        # Obtener coeficiente de importancia
        I = coeficiente_importancia(categoria)
        
        # Obtener espectro de referencia
        S_aH_TH = espectro_referencia(tipo_suelo, zona)
        
        params = parametros_suelo(tipo_suelo)
        T1 = params['T1']
        
        C_r = 0.16 * R
        if R ==1:
                R_star = 1
        elif R !=1 and T_star >= C_r *T1:
                R_star = R
        elif R !=1 and T_star < C_r *T1:
                R_star = 1.5 + (R + 1.5) * T_star / (C_r * T1)
        # Calcular espectro de diseño
        S_a_TH = S_aH_TH / I
        
        return S_a_TH