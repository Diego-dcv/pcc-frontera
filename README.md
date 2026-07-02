# La frontera entre Prometeo y Maxwell

**El Principio de Coste de Concentración (PCC) como cartografía de la
viabilidad energética.**

*Prometeo custodia el territorio de la energía que la naturaleza entrega
ya concentrada — coger y llevar. Maxwell habita el de la energía dispersa por
cuya reunión su demonio cobra un peaje que ninguna técnica elude. La
frontera entre ambos territorios es el objeto de este trabajo: dónde pasa,
por qué pasa por ahí, y en qué dirección puede empujarla la tecnología.*

Repositorio de trabajo: `pcc-frontera`

## Tesis

El coste de aprovechar una fuente de energía se descompone en dos
componentes independientes que históricamente se han confundido:

```
PCC(fuente) = ( W_termo , C_infra )
```

- **W_termo** — trabajo mínimo termodinámico de concentración [J/J útil].
  Acotado por el segundo principio. Puede ser cero.
- **C_infra** — coste infraestructural de captación [m²/W útil].
  Función de la dilución exergética de la fuente. Nunca es cero.

Una fuente es explotable cuando ambas componentes son bajas; la frontera
tecnológica avanza reduciendo C_infra (mejores captadores) porque W_termo
es ley física y no se negocia.

## Estructura

```
BITACORA.md      ← cuaderno de bitácora: leer SIEMPRE antes de trabajar
src/pcc_core.py     funcional PCC y modelos por familia
src/caso_salino.py  banco de pruebas 01: gradiente salino
resultados/         figuras y datos generados
docs/               notas conceptuales
```

## Origen

Deriva del atlas facetado de fuentes de energía (origen × portador,
exergía por evento fundamental) y reformula el PCC v1
*([PCC_la disipación es gratuíta](https://github.com/Diego-dcv/turbulence-is-free))*.

Método de trabajo: colaboración humano-IA documentada por bitácora.

## Licencia

*CC-BY-4.0 para docs, MIT para código*
