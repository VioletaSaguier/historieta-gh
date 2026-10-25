# La casa del Gran Harness

Una historieta interactiva para entender qué es un **harness** y cómo un modelo se convierte en un agente.

Bienvenidos a la casa de GH. En una lámpara del altillo vive la Genia, que representa al modelo: piensa muy bien, pero no tiene cuerpo: no puede tocar nada. Solo puede leer las notitas que le acercan y dictar su respuesta, que aparece escrita en una notita nueva. Los demás habitantes de la casa (la Caja, el Mensajero, el Cuaderno, la Bibliotecaria, el Patio cercado, la Inspectora, el Portero, la Cámara y la Examinadora) representan las piezas del harness. La Genia junto con la casa forman el agente. Mientras avanza la historia, se construye un botón de me gusta en una app de ejemplo.

Los pisos de la casa también tienen significado: en el **altillo** está el modelo; en el **taller**, el harness en acción (lo que pasa mientras se resuelve una tarea); en la **planta baja**, el harness entre tareas (las evals y la memoria de largo plazo). **Afuera** de la casa está la usuaria que hace el pedido: no es parte del agente.

**¿Por qué importa?** Porque el mismo modelo rinde muy distinto según el harness que lo rodea: LangChain llevó su agente del puesto 30 al top 5 de Terminal Bench 2.0 [cambiando solo el harness](https://www.langchain.com/blog/improving-deep-agents-with-harness-engineering).

## Secciones

- **Historieta:** 10 capítulos más un capítulo bonus, viñeta por viñeta. Podés saltar a cualquier capítulo.
- **Personajes:** quién es quién y qué pieza del harness representa.
- **Sacá una pieza:** una prueba de ablación. Quitá un personaje y mirá qué deja de funcionar.
- **Test de conocimiento:** 16 preguntas con explicación y fuente oficial.
- **Tu flujo en la casa:** cómo usar la skill para ver tu propio pedido en historieta.
- **Fuentes:** documentación oficial de Claude Code, la API de Claude, Anthropic Engineering, Codex, MCP, LangChain y LangGraph.

## Skill: tu flujo en la casa

La carpeta [`skill/casa-del-gran-harness`](skill/casa-del-gran-harness) es una [Agent Skill](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) que convierte tu pedido (y, si la tenés, la traza de lo que hizo tu agente) en una historieta de la casa. Cada personaje lleva una marca con el estado de su pieza del harness:

| Estado | Qué significa |
|---|---|
| ✓ Funciona | Hay evidencia de que cumple su función en este flujo. |
| ↑ Conviene mejorar | Funciona, pero hay un ajuste concreto que lo haría más confiable, rápido o barato. |
| ! Incompleta | La pieza existe, pero le falta algo para este pedido. |
| ✗ Falla | Esta pieza causó o dejó pasar un error. |
| ? Revisión humana | Hace falta una decisión tuya: un permiso, un riesgo o un criterio. |
| ○ No está | La pieza no existe en este flujo y su falta importa. |

Al final hay un diagnóstico por pieza y una lista priorizada de qué arreglar, con un botón para copiar los pasos como pedido para tu agente. Mirá [un ejemplo](ejemplo-skill.html).

La skill nunca marca una pieza como «Funciona» sin evidencia observada, y separa lo observado de lo inferido. Si solo le das el pedido, arma una simulación y lo aclara.

**En Claude Code:** copiá la carpeta a `~/.claude/skills/` (todos tus proyectos) o a `.claude/skills/` (solo ese proyecto) y pedí `/casa-del-gran-harness`.

```bash
git clone https://github.com/VioletaSaguier/historieta-gh
cp -r historieta-gh/skill/casa-del-gran-harness ~/.claude/skills/
```

**En Claude (web y app):** descargá [`casa-del-gran-harness.zip`](skill/casa-del-gran-harness.zip) y subilo en **Customize → Skills → + → Create skill → Upload a skill**. Necesitás tener activada la ejecución de código ([cómo usar skills en Claude](https://support.claude.com/en/articles/12512180-use-skills-in-claude)).

El script que arma la página (`scripts/build.py`) usa solo la biblioteca estándar de Python.

## Inspiración

Basada en el artículo [«Harness Engineering: explicado desde cero»](https://x.com/santtiagom_/article/2098782814837543075) de santi ([@santtiagom_](https://x.com/santtiagom_)). El ejemplo del botón de me gusta sale de ahí.

Los personajes son metáforas, no componentes literales. La app, los nombres de archivo y los números de las evals son ejemplos ilustrativos. Los grafos no aparecen en el artículo y se suman como contexto extra.

## Validación

Cada concepto está chequeado contra el artículo original y contra documentación oficial. La lista completa de fuentes está en la sección **Fuentes** de la página.

## Licencia

Esta obra está bajo licencia [Creative Commons Atribución 4.0 Internacional (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/deed.es): podés copiarla, adaptarla y compartirla, también con fines comerciales, siempre que des crédito a [@purpleerainnnn](https://x.com/purpleerainnnn) e indiques si hiciste cambios. El artículo que la inspira es obra de santi (@santtiagom_) y no está cubierto por esta licencia.

## Cómo correrlo

Es un solo archivo HTML, sin dependencias ni build. Abrí `index.html` en el navegador o publicalo en cualquier hosting estático (por ejemplo, Vercel o GitHub Pages).

---

Creado con 💜 por [@purpleerainnnn](https://x.com/purpleerainnnn)
