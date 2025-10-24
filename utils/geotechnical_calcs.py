"""
Funciones auxiliares para cálculos geotécnicos
"""
import numpy as np


def calcular_factores_capacidad_portante(angulo_friccion):
    """
    Calcula los factores de capacidad portante Nc, Nq, Ng
    
    Args:
        angulo_friccion (float): Ángulo de fricción en grados
        
    Returns:
        tuple: (Nc, Nq, Ng)
    """
    phi_rad = np.radians(angulo_friccion)
    
    if angulo_friccion == 0:
        Nc = 5.14
        Nq = 1.0
        Ng = 0.0
    else:
        Nq = np.exp(np.pi * np.tan(phi_rad)) * (np.tan(np.radians(45 + angulo_friccion/2)))**2
        Nc = (Nq - 1) / np.tan(phi_rad)
        Ng = 2 * (Nq - 1) * np.tan(phi_rad)
    
    return Nc, Nq, Ng


def calcular_factores_forma(ancho, largo, angulo_friccion, Nc=None, Nq=None):
    """
    Calcula los factores de forma para capacidad portante
    
    Args:
        ancho (float): Ancho de la cimentación (B)
        largo (float): Largo de la cimentación (L)
        angulo_friccion (float): Ángulo de fricción en grados
        Nc (float, optional): Factor de capacidad portante Nc
        Nq (float, optional): Factor de capacidad portante Nq
        
    Returns:
        tuple: (sc, sq, sg)
    """
    if angulo_friccion == 0:
        sc = 1 + 0.2 * (ancho / largo)
        sq = 1.0
        sg = 1.0
    else:
        if Nc is None or Nq is None:
            Nc, Nq, _ = calcular_factores_capacidad_portante(angulo_friccion)
        
        sc = 1 + (ancho / largo) * (Nq / Nc)
        sq = 1 + (ancho / largo) * np.tan(np.radians(angulo_friccion))
        sg = 1 - 0.4 * (ancho / largo)
    
    return sc, sq, sg


def calcular_asentamiento_consolidacion(Cc, Cr, e0, H, sigma_0, sigma_p, delta_sigma):
    """
    Calcula el asentamiento por consolidación en arcillas
    
    Args:
        Cc (float): Índice de compresión
        Cr (float): Índice de recompresión
        e0 (float): Relación de vacíos inicial
        H (float): Espesor de capa compresible [m]
        sigma_0 (float): Esfuerzo efectivo inicial [kN/m²]
        sigma_p (float): Presión de preconsolidación [kN/m²]
        delta_sigma (float): Incremento de esfuerzo [kN/m²]
        
    Returns:
        tuple: (asentamiento [m], tipo_consolidacion)
    """
    sigma_f = sigma_0 + delta_sigma
    
    if sigma_f <= sigma_p:
        # Recompresión
        Sc = (Cr * H / (1 + e0)) * np.log10(sigma_f / sigma_0)
        tipo = "Recompresión"
    else:
        if sigma_0 < sigma_p:
            # Sobreconsolidado
            Sc1 = (Cr * H / (1 + e0)) * np.log10(sigma_p / sigma_0)
            Sc2 = (Cc * H / (1 + e0)) * np.log10(sigma_f / sigma_p)
            Sc = Sc1 + Sc2
            tipo = "Sobreconsolidado + Virgen"
        else:
            # Compresión virgen
            Sc = (Cc * H / (1 + e0)) * np.log10(sigma_f / sigma_0)
            tipo = "Compresión Virgen"
    
    return Sc, tipo


def calcular_asentamiento_elastico(carga, ancho, modulo_elasticidad, poisson, factor_forma=1.0):
    """
    Calcula el asentamiento elástico inmediato
    
    Args:
        carga (float): Carga aplicada [kN/m²]
        ancho (float): Ancho de cimentación [m]
        modulo_elasticidad (float): Módulo de elasticidad del suelo [kN/m²]
        poisson (float): Relación de Poisson
        factor_forma (float): Factor de forma (default 1.0)
        
    Returns:
        float: Asentamiento inmediato [m]
    """
    Si = (carga * ancho * (1 - poisson**2) * factor_forma) / modulo_elasticidad
    return Si


def clasificar_sucs(grava, arena, finos, Cu, Cc, LL, IP):
    """
    Clasifica un suelo según el sistema SUCS
    
    Args:
        grava (float): Porcentaje de grava
        arena (float): Porcentaje de arena
        finos (float): Porcentaje de finos
        Cu (float): Coeficiente de uniformidad
        Cc (float): Coeficiente de curvatura
        LL (float): Límite líquido
        IP (float): Índice de plasticidad
        
    Returns:
        tuple: (símbolo, descripción)
    """
    if finos < 50:
        # Suelo de grano grueso
        if grava > arena:
            # Grava
            if finos < 5:
                if Cu >= 4 and 1 <= Cc <= 3:
                    return "GW", "Grava bien gradada"
                else:
                    return "GP", "Grava pobremente gradada"
            elif finos <= 12:
                return "GW-GC/GM", "Grava bien gradada con finos"
            else:
                if IP > 7 and LL < 50:
                    return "GC", "Grava arcillosa"
                else:
                    return "GM", "Grava limosa"
        else:
            # Arena
            if finos < 5:
                if Cu >= 6 and 1 <= Cc <= 3:
                    return "SW", "Arena bien gradada"
                else:
                    return "SP", "Arena pobremente gradada"
            elif finos <= 12:
                return "SW-SC/SM", "Arena bien gradada con finos"
            else:
                if IP > 7 and LL < 50:
                    return "SC", "Arena arcillosa"
                else:
                    return "SM", "Arena limosa"
    else:
        # Suelo de grano fino
        if LL < 50:
            if IP > 7:
                return "CL", "Arcilla de baja plasticidad"
            elif IP < 4:
                return "ML", "Limo de baja plasticidad"
            else:
                return "CL-ML", "Limo arcilloso"
        else:
            if IP > 0.73 * (LL - 20):
                return "CH", "Arcilla de alta plasticidad"
            else:
                return "MH", "Limo de alta plasticidad"
