# Las piezas de la casa y cómo diagnosticarlas

Cada personaje de la casa del Gran Harness representa una pieza. Los personajes son metáforas: lo que se diagnostica es la pieza real del flujo.

**Pisos:** en el altillo está el modelo; en el taller, el harness en acción (lo que pasa mientras se resuelve una tarea); en la planta baja, lo que se usa entre tareas (la memoria de largo plazo, que sí es parte del harness, y las evals, que lo ponen a prueba); afuera, la persona que hace el pedido.

## Quienes no se diagnostican

| id | Personaje | Qué es |
|---|---|---|
| `vos` | Vos | La persona que hace el pedido. No es parte del harness: está afuera de la casa. |
| `mente` | La Genia | El modelo. Recibe texto y devuelve texto; piensa y decide, pero no ejecuta nada ni recuerda nada entre llamadas. |

Si algo salió mal, no lo atribuyas al modelo sin antes descartar las piezas del harness. Cuando de verdad es del modelo (por ejemplo, razonó mal con todo el contexto correcto delante), decilo en el Narrador, y la acción suele ser cambiar de modelo o darle un ejemplo, no tocar la casa.

## Piezas centrales (incluilas siempre)

### `reglamento` · El Reglamento · instrucciones
Las instrucciones fijas que el modelo recibe en cada llamada, antes del pedido: su rol, qué tiene que resolver y qué reglas seguir. En la API de Claude van en el parámetro `system` (system prompt); en Claude Code, además, `CLAUDE.md` suma las reglas del proyecto. Guían, pero no obligan: lo que nunca se puede romper tiene que estar en permisos o hooks.
- Preguntas: ¿el agente sabe para quién trabaja y qué se espera? ¿Las reglas son claras y no se contradicen? ¿Hay reglas críticas escritas solo como texto que deberían ser un permiso o un hook?
- `incompleto`: no hay instrucciones del proyecto, o no dicen lo que este pedido necesita. `falla`: el agente rompió una regla escrita, o dos reglas se contradicen. `mejorar`: una regla importante está solo en el prompt y debería hacerse cumplir en el sistema.

### `caja` · La Caja · tools
Las herramientas que el harness le ofrece al modelo. El modelo pide una herramienta con sus datos (en la API de Claude, `tool_use`) y el harness la ejecuta y devuelve el resultado (`tool_result`).
- Preguntas: ¿estaban las herramientas que el pedido necesitaba? ¿Sus nombres y descripciones dejan claro cuándo usarlas? ¿Los errores dicen qué pasó y cómo seguir (es la primera mitad del manejo de errores)? ¿Devuelven lo justo o una montaña de texto?
- `falla`: una herramienta devolvió un error confuso o un resultado equivocado y eso desvió el flujo. `incompleto`: faltaba una herramienta y el agente tuvo que improvisar. `ausente`: el pedido requería actuar y no había ninguna.

### `mensajero` · El Mensajero · loop
El ciclo que llama al modelo una y otra vez con el resultado de la vuelta anterior, hasta terminar. Claude Code lo describe en tres fases: juntar contexto, actuar y verificar.
- Preguntas: ¿cuántas vueltas dio? ¿Cuándo paró: cuando el modelo dijo "terminé" o cuando una verificación pasó? Manejo de errores: cuando algo falló, ¿el error volvió al modelo como un dato para corregir y reintentar, o se frenó todo? ¿Hay un tope de vueltas, reintentos, tiempo o costo?
- `falla`: se quedó dando vueltas en lo mismo, reintentó sin cambiar nada, o cortó antes de terminar. `mejorar`: para solo cuando el modelo dice "terminé" (conectalo con la `inspectora`). `ausente`: fue un único pedido y respuesta, sin loop.

### `cuaderno` · El Cuaderno · memoria (de la tarea)
El estado de la tarea, guardado afuera del modelo y reenviado en cada llamada. La API de Claude no guarda estado: en cada pedido viaja la conversación completa. En tareas largas se suma un archivo de progreso o commits para que la sesión siguiente sepa por dónde seguir.
- Preguntas: ¿el agente sabía qué ya había hecho? ¿Repitió pasos o se contradijo? En tareas de varias sesiones, ¿quedó un registro de progreso?
- `falla`: repitió trabajo o perdió el hilo. `incompleto`: tarea larga sin archivo de progreso.

### `biblio` · La Bibliotecaria · contexto
Arma lo que ve el modelo en cada llamada: un mapa primero, y después lo que el modelo pide o hace falta. La ventana de contexto tiene un máximo (en tokens) y más texto no es mejor. Buenas prácticas: dar un mapa primero y traer lo puntual cuando hace falta (progressive disclosure), resumir cuando se llena (compaction) y dejar lo que tiene que durar en un archivo persistente como `CLAUDE.md`.
- Preguntas: ¿el modelo tuvo la información que necesitaba? ¿Recibió de más (ruido) o de menos? ¿Hubo compaction y se perdió algo importante? ¿El pedido daba el contexto necesario (para qué, para quién, restricciones)?
- `falla`: le faltó un archivo o dato clave, o se saturó y se perdió información. `incompleto`: el pedido o el `CLAUDE.md` no dan el contexto del proyecto. `mejorar`: se carga mucho más de lo necesario.

### `arenero` · El Patio cercado · sandbox
El entorno donde se ejecutan las herramientas y sus límites: dónde se puede escribir y a qué redes se puede conectar. Reduce el daño de un error o de instrucciones escondidas en un archivo (prompt injection), pero no es una garantía total: es una capa más.
- Preguntas: ¿dónde corrió el agente: en la máquina de la persona, en un contenedor, en la nube? ¿Puede escribir fuera del proyecto? ¿Puede salir a internet sin control? ¿Las conexiones externas tienen más permisos de los que la tarea necesita?
- `revisar`: hay acceso de escritura o de red que la tarea no necesita y la persona tiene que decidir. `ausente`: corre sin límites sobre recursos importantes. `ok` solo si viste la configuración del sandbox.

### `inspectora` · La Inspectora · verificación
Compara el resultado con criterios de aceptación y busca evidencia afuera del modelo (tests, una captura, un conteo, revisar la app). Conviene separar a quien construye de quien revisa, porque los agentes tienden a aprobar su propio trabajo.
- Preguntas: ¿había criterios de aceptación, en el pedido o en `CLAUDE.md`? ¿Se corrió algo para comprobarlos? ¿El "listo" del agente vino con evidencia?
- `ausente`: nadie verificó. `incompleto`: se verificó algo, pero no lo que el pedido pedía (por ejemplo, los tests pasan pero nunca se probó la función nueva). `revisar`: los criterios de calidad los tiene que definir la persona.

### `portero` · El Portero · permisos y guardrails
Decide qué herramientas existen, cuáles corren solas y cuáles piden aprobación, y pone topes a los reintentos. Criterio: cuanto más difícil de deshacer es una acción, más conviene que la apruebe una persona; borrar o publicar, siempre. También valida la entrada (los datos de cada pedido, como rutas o parámetros) y la salida (lo que vuelve antes de llegar al modelo o a alguien, como claves secretas). En Claude Code, los permisos se evalúan en orden deny, ask, allow, y la validación se puede hacer con hooks. Los límites que importan viven en el sistema, no solo en las instrucciones.
- Preguntas: ¿qué acciones irreversibles o visibles para otros (borrar, publicar, mandar mails, pagar, tocar producción) pueden pasar sin aprobación? ¿Se validan los datos de cada pedido y lo que vuelve antes de mostrarlo o enviarlo? ¿Hay topes de reintentos, tiempo o costo? ¿Algún límite está solo escrito en el prompt?
- `revisar` es el estado típico: el agente puede hacer algo delicado sin preguntar y la persona tiene que decidir si está bien. `falla`: se hizo algo que no debía. `ok`: viste las reglas y cubren lo delicado de este flujo.

### `camara` · La Cámara · observabilidad
El registro de cada paso: qué vio el modelo, qué pidió y qué volvió (traza o transcript). Sin trazas, todo parece "el modelo falló".
- Preguntas: ¿hay forma de reconstruir la ejecución paso a paso? ¿Se guardan los resultados de las herramientas?
- `ok` en modo traza si la traza existe. `ausente`: solo se ve el resultado final. En modo plan, marcala `revisar` y explicá que sin traza no se puede saber qué pasó.

### `examinador` · La Examinadora · evals
No es parte del harness del agente: Anthropic la llama harness de evaluación, la infraestructura que corre las evals y pone a prueba al modelo junto con su harness. Se diagnostica igual porque, sin evals, no hay forma de saber si un cambio mejoró el flujo.
Un conjunto fijo de tareas que se corre antes y después de cada cambio, con varios intentos por tarea porque el resultado varía. Las evals de regresión detectan que algo que andaba dejó de andar.
- Preguntas: ¿hay casos de prueba con el resultado esperado? ¿Se comparan versiones del prompt o del harness?
- Casi siempre `ausente` en flujos personales. Si el flujo se repite (un resumen semanal, un reporte), recomendá armar 3 a 5 casos de prueba; si es una tarea única, puede quedar `ausente` con una nota que diga que no hace falta todavía.

## Piezas extra (solo si aparecen o si su falta explica un problema)

### `skills` · El Recetario · skills
Instrucciones, criterios y recursos empaquetados para un tipo de tarea. Al empezar, el modelo solo ve el nombre y la descripción; el contenido completo se carga cuando hace falta.
- Diagnóstico típico: `mejorar` si la persona repite las mismas instrucciones en cada pedido (convertirlas en skill); `falla` si existía una skill pero no se usó porque su descripción no decía cuándo usarla.

### `mcp` · El Enchufe · MCP
Model Context Protocol: un estándar abierto para conectar el agente con herramientas y datos externos (GitHub, una base de datos, una app de tickets).
- Diagnóstico típico: `mejorar` si trae datos de más; `revisar` si tiene permisos de escritura que la tarea no necesita.

### `sub` · Las otras genias · subagentes
Otras ejecuciones con su propio contexto y objetivo, que hacen una parte y devuelven un resumen. Se puede usar un modelo más barato para lo simple (model routing).
- Diagnóstico típico: `mejorar` cuando una tarea grande se podría repartir para no saturar el contexto principal; `falla` si un subagente devolvió un resumen que perdió algo importante.

### `grafo` · El Plano · grafo
Un mapa explícito de pasos (nodos) y conexiones (aristas) que define qué va después de qué, como en LangGraph. No aparece en el artículo que inspira la casa.
- Diagnóstico típico: `mejorar` cuando el flujo siempre sigue los mismos pasos y conviene fijarlos en vez de dejar que el modelo improvise el orden.

### `memlarga` · El Archivo · memoria de largo plazo
Información que se reutiliza entre tareas: decisiones, preferencias, errores recurrentes.
- Diagnóstico típico: `incompleto` cuando el agente comete el mismo error que en tareas anteriores o la persona tiene que repetir sus preferencias cada vez.

## Fuentes

- Claude Code: glosario, cómo funciona, permisos, sandboxing y skills — https://code.claude.com/docs/en/glossary
- Tool use con Claude — https://platform.claude.com/docs/en/build-with-claude/tool-use/overview
- Context engineering para agentes — https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- Harnesses para agentes de larga duración — https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
- Diseño de harness para apps largas — https://www.anthropic.com/engineering/harness-design-long-running-apps
- Evals para agentes — https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
- Model Context Protocol — https://modelcontextprotocol.io/docs/getting-started/intro
- Agent Skills — https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
