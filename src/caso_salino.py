"""
Caso de prueba 01: gradiente salino
===================================
Primer contacto del PCC formalizado con datos reales.

Preguntas que este script responde con números:
  1. ¿Cuál es el techo termodinámico exacto (W_max) de los pares
     río/mar y salmuera/mar?
  2. ¿Qué densidad de potencia de membrana implica cada par, y dónde
     quedan el umbral comercial (~5 W/m²) y los resultados
     nanofluídicos publicados (10-34 W/m²) respecto al techo?
  3. ¿Qué componente del PCC domina aquí: W_termo o C_infra?
"""

import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pcc_core import (trabajo_mezcla_ideal, presion_osmotica_vant_hoff,
                      densidad_potencia_PRO_ideal)

KWH = 3.6e6  # J

# --- Concentraciones (NaCl equivalente, mol/L) -------------------------
c_rio      = 0.01   # ~0.6 g/L, agua dulce típica
c_mar      = 0.60   # ~35 g/L
c_salmuera = 1.20   # ~70 g/L, rechazo de desaladora (recuperación ~50%)

pares = {
    "río / mar":        (c_mar, c_rio),
    "mar / salmuera":   (c_salmuera, c_mar),
    "río / salmuera":   (c_salmuera, c_rio),
}

print("="*72)
print("1. TECHO TERMODINÁMICO POR PAR (van 't Hoff ideal, 25 °C)")
print("="*72)
resultados = {}
for nombre, (cc, cd) in pares.items():
    W = trabajo_mezcla_ideal(cc, cd)                    # J/m³ de diluida
    dpi = (presion_osmotica_vant_hoff(cc)
           - presion_osmotica_vant_hoff(cd))            # Pa
    resultados[nombre] = (W, dpi)
    print(f"  {nombre:16s}  W_max = {W/1e6:6.3f} MJ/m³ "
          f"= {W/KWH:6.3f} kWh/m³   |  Δπ = {dpi/1e5:6.1f} bar")

# --- Recurso global (orden de magnitud) --------------------------------
Q_rios = 37300e9 / (365.25*24*3600)   # m³/s, descarga fluvial global
W_riomar = resultados["río / mar"][0]
P_teorica = Q_rios * W_riomar
print(f"\n  Recurso teórico global río/mar: {P_teorica/1e12:.2f} TW "
      f"({P_teorica*8760/1e12/1e3:.0f} PWh/año)")
print("  [Contraste literatura: ~1.4-3 TW teórico, ~1 TW técnico]")

print()
print("="*72)
print("2. DENSIDAD DE POTENCIA DE MEMBRANA vs TECHO")
print("="*72)
# Permeabilidades A_w típicas [m/(s·Pa)]
membranas = {
    "PRO comercial (CTA, ~2015)":      1.0e-12,
    "TFC avanzada":                    5.0e-12,
    "nanofluídica (extrapolación)":    2.5e-11,
}
for nombre, (W, dpi) in resultados.items():
    print(f"\n  Par {nombre} (Δπ = {dpi/1e5:.0f} bar):")
    for mem, Aw in membranas.items():
        P = densidad_potencia_PRO_ideal(dpi, Aw)
        print(f"    {mem:34s} P_ideal = {P:7.1f} W/m²")
print("\n  Umbral comercial estimado: ~5 W/m²")
print("  Publicado nanofluídico (lab): 10-34 W/m²")

print()
print("="*72)
print("3. DESCOMPOSICIÓN PCC")
print("="*72)
print("""
  W_termo: ~0. La mezcla es espontánea; no hay que INVERTIR trabajo
           para concentrar — la fuente YA es un gradiente. Las pérdidas
           (polarización de concentración, resistencia interna) son
           irreversibilidades de conversión, no coste de concentración.

  C_infra: DOMINANTE. Con 0.8 kWh/m³ y caudales fluviales, el coste
           es área de membrana por vatio. A 5 W/m² se necesitan
           200 000 m² de membrana por MW. A 30 W/m², 33 000 m²/MW.
           => La variable única que gobierna la viabilidad es la
           densidad de potencia de membrana, tal y como concluimos
           cualitativamente en la sesión del atlas. Ahora con números.
""")

# --- Figura: densidad de potencia vs permeabilidad y par ---------------
fig, ax = plt.subplots(figsize=(9, 5.5))
Aw_range = np.logspace(-13, -10.3, 200)
colores = {"río / mar": "#1f77b4", "mar / salmuera": "#d62728",
           "río / salmuera": "#7f2fbf"}
for nombre, (W, dpi) in resultados.items():
    P = densidad_potencia_PRO_ideal(dpi, Aw_range)
    ax.plot(Aw_range*1e12, P, label=f"{nombre} (Δπ={dpi/1e5:.0f} bar)",
            color=colores[nombre], lw=2)
ax.axhline(5, color="gray", ls="--", lw=1)
ax.text(0.12, 5.6, "umbral comercial ~5 W/m²", fontsize=9, color="gray")
ax.axhspan(10, 34, color="gold", alpha=0.18)
ax.text(0.12, 22, "rango nanofluídico publicado", fontsize=9, color="#8a6d00")
ax.set_xscale("log"); ax.set_yscale("log")
ax.set_xlabel("Permeabilidad de membrana A$_w$  [10⁻¹² m/(s·Pa)]")
ax.set_ylabel("Densidad de potencia ideal  [W/m²]")
ax.set_title("PCC — caso salino: la viabilidad vive en la membrana")
ax.legend(); ax.grid(alpha=0.3, which="both")
fig.tight_layout()
out = os.path.join(os.path.dirname(__file__), "..", "resultados",
                   "caso_salino_densidad_potencia.png")
fig.savefig(out, dpi=150)
print(f"Figura guardada: {os.path.abspath(out)}")
