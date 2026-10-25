---
name: casa-del-gran-harness
description: Convierte el pedido o prompt de alguien, y lo que su agente hizo (o haría) con él, en una historieta interactiva de La casa del Gran Harness, con un diagnóstico visual de cada pieza del harness (herramientas, loop, memoria, contexto, sandbox, verificación, permisos, observabilidad, evals, skills, MCP, subagentes) marcada como funciona, conviene mejorar, incompleta, falla, revisión humana o no está, y los próximos pasos para arreglarla. Usala cuando alguien quiera ver su flujo de agente en historieta, entender qué parte de su prompt, agente o harness falla o está incompleta, revisar una ejecución o traza, o pida "pasá esto a la casa de GH".
license: CC-BY-4.0
---

# La casa del Gran Harness: tu flujo en historieta

Esta skill toma un pedido real (un prompt, una tarea, una sesión de agente) y lo cuenta como una historieta en la casa del Gran Harness. En la casa, la Genia es el modelo y cada habitante es una pieza del harness. Cada personaje lleva una marca con su estado, así la persona ve de un vistazo qué pieza funciona, cuál falla, cuál está incompleta y cuál necesita una decisión humana. Al final hay un diagnóstico por pieza y una lista priorizada de qué arreglar.

El resultado es un único archivo HTML, sin dependencias, que se abre en cualquier navegador.

## Antes de empezar

Leé `references/piezas.md`: tiene qué representa cada personaje, qué preguntar para diagnosticarlo y cuándo corresponde cada estado. Leé `references/formato.md` cuando vayas a escribir el JSON.

## Paso 1. Juntar el material

Necesitás, como mínimo, el **pedido literal** de la persona. Con eso solo ya se puede armar una simulación. Todo lo demás mejora el diagnóstico; juntá lo que esté a mano:

- El prompt completo o el system prompt, si es un agente propio.
- Instrucciones persistentes: `CLAUDE.md`, `AGENTS.md` o equivalentes.
- Herramientas y conexiones disponibles (incluidos los servidores MCP).
- Permisos y límites: qué corre solo, qué pide aprobación, qué está prohibido. En Claude Code están en `.claude/settings.json` y `~/.claude/settings.json`; los servidores MCP del proyecto, en `.mcp.json`; las skills, en `.claude/skills/`.
- Lo que pasó: la traza o transcript de la ejecución, los logs, los resultados de los tests, el resultado final.
- Si la persona pide "pasá a historieta lo que acabás de hacer", la traza es esta misma conversación: usá los pasos que realmente diste.

Si no hay pedido, pedíselo a la persona en una sola pregunta. Si hay pedido pero falta el resto, no frenes: seguí en modo simulación y anotá qué faltó en `fuentes`.

## Paso 2. Elegir el modo

- `"traza"`: hay evidencia de una ejecución real. Cada viñeta cuenta un paso que pasó de verdad.
- `"plan"`: solo hay pedido y configuración. Cada viñeta cuenta lo que el agente probablemente haría. Decilo en el Narrador ("lo más probable es que…") y nunca inventes resultados como si hubieran pasado.

## Paso 3. Diagnosticar cada pieza

Para cada pieza del harness, decidí un estado siguiendo `references/piezas.md`:

| Estado | Cuándo |
|---|---|
| `ok` (Funciona) | Hay evidencia **observada** de que cumple su función en este flujo. |
| `mejorar` (Conviene mejorar) | Funciona, pero hay un ajuste concreto que haría el flujo más confiable, rápido o barato. |
| `incompleto` (Incompleta) | La pieza existe pero le falta algo para este pedido (por ejemplo, hay tests pero no cubren lo que se cambió). |
| `falla` (Falla) | Hay evidencia de que esta pieza causó o dejó pasar un error. |
| `revisar` (Revisión humana) | Hace falta una decisión o confirmación de la persona: un permiso, un riesgo, un criterio, o no hay forma de saberlo con lo que se revisó. |
| `ausente` (No está) | La pieza no existe en este flujo y su falta importa. |

Reglas que no se negocian:

1. **Nunca marques `ok` sin evidencia observada** (`"tipo": "observado"`). El script rechaza un `ok` sin ella. Si no podés comprobarlo, usá `revisar`.
2. Separá lo **observado** (está en la traza, en la configuración o en un resultado) de lo **inferido** (tu lectura). Ponelo en `tipo`.
3. Incluí siempre las nueve piezas centrales: `caja`, `mensajero`, `cuaderno`, `biblio`, `arenero`, `inspectora`, `portero`, `camara`, `examinador`. Sumá `skills`, `mcp`, `sub`, `grafo` o `memlarga` solo si aparecen en el flujo o si su falta explica un problema.
4. Si el problema es del pedido mismo (ambiguo, sin criterios de éxito), no culpes al modelo: casi siempre es `inspectora` (faltan criterios de aceptación) o `biblio` (falta contexto). Decilo en la nota.
5. Cada pieza en `falla`, `incompleto` o `mejorar` lleva una `accion` concreta: qué cambiar, dónde y cómo se nota que funcionó.
6. No inventes datos. Si un número, un archivo o un resultado no está en el material, no lo pongas. En el ejemplo del repo los datos son inventados y lo dice en `fuentes`; en un diagnóstico real, no.

## Paso 4. Escribir las viñetas

Entre 6 y 14 viñetas, en orden:

1. **Primera viñeta:** Vos (`vos`) le pasa el pedido a la Genia (`mente`). El pedido va en `nota`, literal (si es muy largo, recortalo y aclará "…").
2. **Una viñeta por paso que importe**: cada llamada a una herramienta relevante, cada decisión, cada error, cada aprobación. Agrupá pasos repetitivos en una sola viñeta.
3. **Cuando un paso muestra un problema**, marcá la viñeta con `pieza` y `estado`, y explicá en `alerta` qué pasó y por qué importa. Así la persona ve el problema justo donde ocurre.
4. **Última viñeta:** el cierre, con lo más importante para arreglar. El Narrador separa qué es del modelo y qué es del harness.

Cómo se escriben:

- `dice` es lo que dice el personaje, en primera persona, corto y claro (hasta ~200 caracteres).
- `nota` es la notita literal que viaja (el pedido, la llamada a una herramienta, un resultado). Usá `"mono": true` para código o llamadas.
- `narrador` explica qué pasa y qué concepto ilustra, en una o dos oraciones (hasta ~200 caracteres).
- Hablan los personajes que tienen sentido: la Genia pide herramientas; la Caja las ejecuta; el Portero aprueba o frena; la Inspectora verifica; la Cámara muestra la traza. La Genia nunca ejecuta nada: dicta.
- Una pieza `ausente` no puede hablar ni actuar. Mostrala con `pieza` en una viñeta donde se nota su falta.
- La página está en castellano: escribí los textos en castellano, con el tono de la casa (cercano, con "vos"), claro y sin jerga sin explicar. Si usás un término técnico, el Narrador lo explica. Las notitas literales (el pedido, código, nombres de herramientas) van tal cual, en su idioma original.

## Paso 5. Próximos pasos

En `proximos_pasos`, de 3 a 7 acciones ordenadas por impacto. Cada una con `pieza`, `accion`, `prioridad` (`alta`, `media`, `baja`) y `quien`:

- `agente`: se le puede pedir directamente al agente (reescribir una instrucción, agregar un test, procesar por tandas).
- `humano`: necesita una decisión de la persona (un permiso, un criterio de calidad, un riesgo que aceptar).

## Paso 6. Generar el HTML

Guardá el JSON y corré el script desde la carpeta de esta skill:

```bash
python3 scripts/build.py historia.json historieta.html
```

El script valida el JSON. Si hay errores, los lista en castellano: corregilos y volvé a correrlo. Los avisos no frenan la generación, pero leelos.

Para ver un ejemplo completo: `examples/resumen-de-tickets.json`.

## Paso 7. Entregar

Entregá el HTML a la persona (como archivo o como página publicada, según el entorno). En la respuesta, en pocas líneas:

- Las dos o tres piezas más importantes para arreglar y por qué.
- Lo que necesita decidir ella (los pasos de `humano`).
- Qué no pudiste revisar, si faltó material.

No repitas toda la historieta en el chat: la persona la va a leer en la página. Si después cambia algo de su flujo, ofrecé volver a correr la skill para comparar.
