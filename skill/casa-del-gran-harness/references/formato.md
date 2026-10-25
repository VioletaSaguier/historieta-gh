# Formato del JSON de la historia

`scripts/build.py` lee este JSON, lo valida y genera el HTML. Ejemplo completo: `examples/resumen-de-tickets.json`.

```json
{
  "titulo": "Nombre corto del flujo",
  "modo": "traza",
  "pedido": "El pedido literal de la persona",
  "prompt": "Opcional: system prompt, CLAUDE.md o configuración relevante (texto plano)",
  "fuentes": ["Qué se revisó para el diagnóstico", "y qué faltó"],
  "fecha": "Opcional, por ejemplo 24 de octubre de 2026",
  "usuario": "Opcional: cómo llamar a la persona en vez de «Vos»",
  "piezas": {
    "<id>": {
      "estado": "ok | mejorar | incompleto | falla | revisar | ausente",
      "tipo": "observado | inferido | sin_evidencia",
      "nota": "Qué pasa con esta pieza en este flujo (1 o 2 oraciones)",
      "evidencia": "Dónde se ve: archivo, línea de la traza, resultado",
      "accion": "Qué cambiar, concreto"
    }
  },
  "vinietas": [
    {
      "a": "<id>", "b": "<id opcional>", "habla": "a | b",
      "dice": "Lo que dice quien habla",
      "reaccion": "Opcional: lo que contesta el otro",
      "nota": "Opcional: la notita literal que viaja de quien habla al otro",
      "mono": true,
      "narrador": "Qué pasa y qué concepto ilustra",
      "animo_a": "happy | neutral | think | worried | surprised | confused",
      "animo_b": "…",
      "pieza": "Opcional: <id> de la pieza que esta viñeta pone en foco",
      "estado": "Opcional: estado que se muestra en la alerta",
      "alerta": "Opcional: qué pasó y por qué importa"
    }
  ],
  "proximos_pasos": [
    {"pieza": "<id>", "accion": "…", "prioridad": "alta | media | baja", "quien": "agente | humano"}
  ]
}
```

## Ids de personajes

Podés usar el id o cualquiera de sus alias.

| id | Alias | Personaje | Pieza |
|---|---|---|---|
| `vos` | usuario, usuaria | Vos | quien pide (no se diagnostica) |
| `mente` | genia, modelo | La Genia | modelo (no se diagnostica) |
| `caja` | tools, herramientas | La Caja | tools |
| `mensajero` | loop | El Mensajero | loop |
| `cuaderno` | memoria | El Cuaderno | memoria de la tarea |
| `biblio` | bibliotecaria, contexto | La Bibliotecaria | contexto |
| `arenero` | patio, sandbox | El Patio cercado | sandbox |
| `inspectora` | verificacion | La Inspectora | verificación |
| `portero` | permisos | El Portero | permisos |
| `camara` | observabilidad | La Cámara | observabilidad |
| `examinador` | examinadora, evals | La Examinadora | evals |
| `skills` | recetario | El Recetario | skills |
| `mcp` | enchufe | El Enchufe | MCP |
| `sub` | otras_genias, subagentes | Las otras genias | subagentes |
| `grafo` | plano | El Plano | grafo |
| `memlarga` | archivo, memoria_largo_plazo | El Archivo | memoria de largo plazo |

## Reglas que valida el script

- `titulo`, `pedido`, `piezas` y `vinietas` son obligatorios.
- Una pieza en `ok` tiene que tener `"tipo": "observado"`.
- Todo personaje que aparece en una viñeta (salvo `vos` y `mente`) tiene que estar en `piezas`.
- Una pieza `ausente` no puede ser `a` ni `b` de una viñeta; se la muestra con `pieza`.
- Cada viñeta tiene `a` y `dice`; si `habla` es `b`, tiene que haber `b`.

## Cómo se ve

- En la casa aparecen solo las piezas listadas en `piezas`, cada una con una marca de color con su estado. Las `ausente` se ven como fantasmas grises.
- Los dos personajes de la viñeta se destacan; los demás quedan atenuados.
- Si hay `nota` y otro personaje, la notita viaja por la casa (por la escalera si el Mensajero está presente y cambian de piso).
- `pieza` dibuja un recuadro de color alrededor de ese personaje; `estado` y `alerta` muestran un aviso debajo del diálogo.
- Arriba hay un resumen por estado que filtra el diagnóstico; abajo, las tarjetas por pieza y los próximos pasos, con un botón para copiarlos como pedido para el agente.
