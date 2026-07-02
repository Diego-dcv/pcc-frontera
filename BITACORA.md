# Cuaderno de bitácora — PCC: trabajo de concentración

Proyecto: formalización matemática del **Principio de Coste de Concentración**
y su contraste empírico, derivado del atlas facetado de fuentes de energía.

Colaboración: Diego Carreño de Vicente (dirección, criterio, catálisis) +
Claude/Anthropic (modelización, cálculo, crítica interna).

**Repositorio antecedente:** [PCC v1 — GOY, difusión en redes, caso apagón ibérico]
*(enlazar aquí al repo antiguo)*. Este repositorio reformula el principio;
no sustituye al anterior, lo depura.

---

## Protocolo de continuidad (leer antes de cada sesión)

Cada sesión de trabajo con una instancia de IA añade UNA entrada con este
formato. La instancia debe leer las tres últimas entradas antes de trabajar.

```
## Entrada NNN — AAAA-MM-DD
Objetivo:        (qué se quería hacer)
Decisiones:      (qué se decidió y POR QUÉ — esto es lo que se pierde entre sesiones)
Resultados:      (números, ficheros generados, validaciones)
Falsaciones:     (qué se intentó y NO funcionó — tan valioso como lo anterior)
Abierto:         (siguiente paso concreto)
```

Regla de oro: las decisiones conceptuales se registran con su justificación,
no solo con su conclusión. El "por qué" es la memoria que las instancias no tienen.

---

## Entrada 001 — 2026-07-02

**Objetivo:** Revisar el trabajo del atlas de energía, decidir qué merece
modelo matemático, y dar el primer golpe: formalizar el PCC y estrellarlo
contra un caso con datos reales (gradiente salino).

**Decisiones:**

1. **Repo nuevo, no ampliación del antiguo.** El repo PCC v1 lleva encuadre
   distinto (turbulencia GOY, difusión en redes) y DOI propio. Esta
   reformulación merece traza de versiones limpia. Se enlazan mutuamente.

2. **El PCC se formaliza como PAR, no como escalar.** Esta es la decisión
   conceptual central de la sesión y responde a la crítica que la propia IA
   hizo a la versión anterior (que el PCC era una intuición sin formulación
   y que se confundía con el techo termodinámico):

   `PCC(fuente) = (W_termo, C_infra)`

   - **W_termo**: trabajo mínimo termodinámico de concentración (J invertido
     por J útil). Límite exacto por 2º principio. Ejemplo dominante: bombear
     calor de baja temperatura (1/COP_Carnot).
   - **C_infra**: coste infraestructural de captación (m² de captador por W
     útil), función de la dilución de la fuente. No es termodinámico; es
     geométrico-económico. Ejemplo dominante: fotovoltaica, membranas.

   Justificación: hay fuentes termodinámicamente gratis pero
   infraestructuralmente carísimas (radiación diluida: la concentración
   óptica pasiva no cuesta trabajo hasta el límite de étendue C≈46 200,
   pero cuesta óptica y seguimiento) y viceversa. Colapsar ambas en un
   número era el error de origen del PCC v1.

3. **Banco de pruebas: gradiente salino**, por ser el caso identificado en
   el atlas como oportunidad más cercana y por tener datos publicados
   (umbral comercial ~5 W/m²; membranas nanofluídicas 10–34 W/m²;
   demostrador Sweetch Energy OPUS-1 en el Ródano).

4. Modelo v0.1 deliberadamente ideal (van 't Hoff, PRO idealizado
   P=A_w·Δπ²/4). Primero validar órdenes de magnitud; refinamientos
   (coeficientes de actividad, polarización de concentración) solo si el
   esqueleto aguanta.

**Resultados:**

| Par | W_max | Δπ | Validación |
|---|---|---|---|
| río / mar | 0.756 kWh/m³ | 29.3 bar | literatura: ~0.7–0.8 kWh/m³, ~29 bar ✓ |
| mar / salmuera | 0.254 kWh/m³ | 29.7 bar | — |
| río / salmuera | 1.573 kWh/m³ | 59.0 bar | duplica el gradiente ✓ |

- Recurso teórico global río/mar: **3.2 TW** (literatura: 1.4–3 TW teórico;
  ligeramente alto por idealidad del modelo — coherente).
- Densidades de potencia PRO ideales: membrana comercial 2015 → 2.1 W/m²
  (bajo umbral, explica el fracaso de Statkraft); TFC avanzada → 10.7 W/m²;
  nanofluídica → 53 W/m² ideal, que acota por arriba el rango publicado
  10–34 W/m² (las pérdidas reales se comen ~40–60%: razonable).
- **Confirmación cuantitativa de la conclusión cualitativa del atlas:** en
  el caso salino W_termo ≈ 0 y el PCC es puro C_infra. A 5 W/m² hacen falta
  200 000 m² de membrana por MW; a 30 W/m², 33 000 m²/MW. La viabilidad
  vive en un único parámetro: densidad de potencia de membrana.
- El par **río/salmuera** (59 bar) es el hallazgo operativo: cuadruplica la
  densidad de potencia respecto a río/mar con la misma membrana. Refuerza
  la tesis del acoplamiento con desaladoras.
- Ficheros: `src/pcc_core.py`, `src/caso_salino.py`,
  `resultados/caso_salino_densidad_potencia.png`.

**Falsaciones / errores de la sesión:**
- Bug inicial: bucle de la sección 2 iteraba sobre concentraciones en vez
  de sobre resultados (Δπ=0). Corregido. Se registra como recordatorio de
  que la validación contra literatura detectó el fallo al instante:
  mantener SIEMPRE contrastes de literatura en los scripts.

**Abierto (siguiente sesión):**
1. Aplicar la descomposición (W_termo, C_infra) a las otras cinco familias
   del atlas y construir el "mapa PCC": plano log-log W_termo vs C_infra
   con todas las fuentes posicionadas. Hipótesis a comprobar: las fuentes
   explotadas históricamente ocupan la esquina (bajo, bajo) y la frontera
   de expansión tecnológica avanza en diagonal.
2. Refinar el caso salino: polarización de concentración y modelo RED
   (resistencia de membrana) para acotar mejor el rango nanofluídico.
3. Decidir nombre definitivo del repo y crear en GitHub (Diego).

---

## Entrada 002 — 2026-07-02

**Objetivo:** Bautizo del proyecto.

**Decisiones:**

1. **Título del ensayo/documento con DOI:** *La frontera entre Prometeo
   y Maxwell*. **Subtítulo:** *El Principio de Coste de Concentración
   como cartografía de la viabilidad energética*.

   Justificación (registrada porque el porqué es la memoria del proyecto):
   el título no es decorativo sino estructural — describe el modelo.
   Prometeo = territorio de la energía que la naturaleza entrega
   concentrada (fuego, carbón, uranio: componente C_infra baja, coger y
   llevar). Maxwell = territorio de lo disperso, donde reunir tiene un
   peaje termodinámico mínimo (W_termo, vía demonio de Maxwell/Landauer)
   que ninguna técnica elude. La frontera entre ambos ES la diagonal del
   mapa PCC (hipótesis pendiente de la Entrada 001, punto 1 de "Abierto").

2. **Jerarquía invertida respecto a la propuesta inicial de Diego**
   ("PCC, la frontera..."): la imagen abre, la sigla baja al subtítulo.
   Primer golpe fachada, segundo golpe rigor.

3. **Asimetría asumida de las figuras** (mito vs físico histórico): es
   elección estética deliberada — un titán y un demonio victoriano
   custodiando cada lado — y debe declararse como tal en una frase de la
   introducción del ensayo para desarmar la crítica previsible.

4. **Nombre sobrio del repositorio:** `pcc-frontera` (buscable; la poesía
   vive en el documento, la infraestructura en el repo — patrón SimbIAsis).

**Resultados:** README actualizado con título, subtítulo y párrafo de
fachada.

**Falsaciones:** —

**Abierto:** sin cambios respecto a Entrada 001 — (1) mapa PCC de seis
familias en plano log-log W_termo vs C_infra y test de la hipótesis de la
diagonal; (2) refinado del caso salino (polarización, modelo RED);
(3) creación del repo `pcc-frontera` en GitHub con enlace cruzado a PCC v1
(tarea de Diego).
