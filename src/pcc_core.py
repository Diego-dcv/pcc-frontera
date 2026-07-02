"""
PCC — Principio de Coste de Concentración
Formalización v0.1

Tesis formalizada:
El coste de aprovechar una fuente de energía tiene DOS componentes
separables, y la confusión histórica del PCC venía de mezclarlas:

  1. W_termo : trabajo mínimo termodinámico de concentración.
     Exergía que hay que destruir/invertir para llevar el portador
     desde su estado difuso ambiente hasta un estado útil.
     Tiene límite inferior exacto (2º principio). A veces es CERO
     (concentración óptica pasiva de radiación hasta el límite de
     étendue) y a veces domina (bombeo de calor de baja T).

  2. C_infra : coste infraestructural de captación.
     Área/volumen/masa de captador que hay que desplegar por vatio
     útil, función de la densidad exergética de la fuente.
     No es termodinámico: es geométrico-económico. Escala como
     ~ 1/phi_ex (flujo exergético por unidad de área).

Definición del funcional:

  PCC(fuente) = ( W_termo / E_util ,  A_captacion / P_util )

Es deliberadamente un PAR, no un escalar: colapsarlo en un solo
número fue el error de la versión anterior. Una fuente puede ser
termodinámicamente barata e infraestructuralmente carísima
(fotovoltaica difusa) o al revés.

Índice de realización (conecta con el atlas):

  chi = P_real / P_techo   con techo = límite termodinámico puro
"""

import numpy as np

R = 8.314          # J/(mol·K)
T0 = 298.15        # K, ambiente de referencia


# ----------------------------------------------------------------------
# Familia química: gradientes de concentración (caso salino y afines)
# ----------------------------------------------------------------------

def presion_osmotica_vant_hoff(c_molar, i=2, T=T0):
    """Presión osmótica [Pa]. c_molar en mol/L, i = factor de van 't Hoff."""
    return i * c_molar * 1000.0 * R * T


def trabajo_mezcla_ideal(c_conc, c_dil, T=T0, i=2):
    """
    Trabajo máximo extraíble [J/m³ de disolución diluida] al mezclar
    reversiblemente 1 m³ de disolución diluida en un reservorio infinito
    de disolución concentrada. Modelo ideal (van 't Hoff integrado):

      W = i·R·T·1000·[ c_c - c_d - c_d·ln(c_c/c_d) ]   (c en mol/L)

    Para c_d -> 0 se recupera W ≈ pi(c_c)·V.
    """
    c_c, c_d = float(c_conc), float(c_dil)
    if c_d <= 0:
        return presion_osmotica_vant_hoff(c_c, i, T)
    return i * R * T * 1000.0 * (c_c - c_d - c_d * np.log(c_c / c_d))


def densidad_potencia_PRO_ideal(delta_pi, A_w):
    """
    Densidad de potencia máxima idealizada en ósmosis por presión
    retardada (PRO):  P_max = A_w · (Δπ)² / 4   [W/m²]
    A_w : permeabilidad al agua de la membrana [m/(s·Pa)]
    Se opera a ΔP = Δπ/2 (punto de máxima potencia).
    """
    return A_w * delta_pi**2 / 4.0


# ----------------------------------------------------------------------
# Familia radiativa: coste de concentración de radiación diluida
# ----------------------------------------------------------------------

def factor_dilucion_solar(irradiancia_local=1000.0, T_sol=5778.0):
    """Factor de dilución f de la radiación solar en superficie."""
    sigma = 5.670e-8
    return irradiancia_local / (sigma * T_sol**4)


def eficiencia_landsberg(T_sol=5778.0, T_amb=T0):
    """Techo exergético de la radiación solar no diluida."""
    x = T_amb / T_sol
    return 1.0 - (4.0/3.0)*x + (1.0/3.0)*x**4


def eficiencia_petela_diluida(f, T_sol=5778.0, T_amb=T0):
    """
    Fracción exergética de radiación diluida (aprox. de Landsberg-Tonge).
    Muestra el coste TERMODINÁMICO de no concentrar: la exergía específica
    de la radiación cae con la dilución. La concentración óptica pasiva
    (hasta C_max = 1/f ≈ 46200) recupera exergía SIN trabajo: W_termo = 0,
    todo el coste es C_infra (óptica, seguimiento).
    """
    # temperatura efectiva de la radiación diluida (aprox. gris)
    T_ef = T_sol * f**0.25
    x = T_amb / T_ef
    return max(0.0, 1.0 - (4.0/3.0)*x + (1.0/3.0)*x**4)


# ----------------------------------------------------------------------
# Familia térmica: coste de concentrar calor de baja temperatura
# ----------------------------------------------------------------------

def cop_carnot_bomba(T_util, T_fuente):
    """COP máximo de una bomba de calor que 'concentra' calor difuso."""
    if T_util <= T_fuente:
        return np.inf
    return T_util / (T_util - T_fuente)


def w_termo_concentracion_calor(T_util, T_fuente, T_amb=T0):
    """
    Trabajo mínimo [J por J de calor útil] para elevar calor desde
    T_fuente hasta T_util. Este es el caso donde W_termo DOMINA el PCC.
    """
    return 1.0 / cop_carnot_bomba(T_util, T_fuente)


# ----------------------------------------------------------------------
# Índices agregados del atlas
# ----------------------------------------------------------------------

def indice_realizacion(P_real, P_techo):
    """chi = realizado / techo termodinámico."""
    return P_real / P_techo


def coste_infraestructural(phi_exergetico):
    """
    C_infra [m²/W]: área de captación por vatio útil.
    phi_exergetico: flujo exergético por unidad de área [W/m²].
    """
    return 1.0 / phi_exergetico
