# FIATC Seguro de Salud — Wireframe Mobile

## Archivo único
`/Users/miquelmir/Fiatc/wireframe_mobile.html` (~4400 líneas)

Todo está en un solo archivo HTML autocontenido: CSS, HTML y JS. No hay build system, no hay dependencias externas. Se abre directamente en el navegador con `file://`.

---

## Encuadre del proyecto

Wireframe interactivo mobile-first para el funnel de cotización y contratación de FIATC Seguro de Salud. Simula un iPhone (frame de 375px con `box-shadow`). El objetivo es validar UX y copy con stakeholders — no es producción.

---

## CSS: paleta de colores (CSS custom properties)

```css
--wf-0:   #FFFFFF   /* blanco puro */
--wf-10:  #F7FAFC   /* fondo de página */
--wf-20:  #EBF0F4   /* bordes suaves, fondos de cards */
--wf-40:  #CED7E5   /* bordes más marcados, separadores */
--wf-60:  #8994A5   /* textos secundarios, placeholders */
--wf-90:  #424B5A   /* textos principales, iconos */
--wf-100: #272A30   /* negro casi puro, títulos */
```

Regla: usar solo estas variables. No usar colores hardcoded salvo para iconos SVG heredados.

---

## Navegación: flujo de cotización

```js
const stepFlow = [0, 'CP', 1, 2, 4, 5, 6, '6b'];
let stepFlowIdx = 0;
```

- `nextStep()` avanza por `stepFlow`
- `prevStep()` retrocede
- Al llegar al final de `stepFlow`, `showLoading()` lanza el spinner y luego activa `step7` (resultados)
- `currentStep` se mantiene por compatibilidad pero el índice real es `stepFlowIdx`

### Pasos del funnel de cotización

| ID | Contenido |
|---|---|
| `step0` | Portada / hero |
| `stepCP` | Código postal |
| `step1` | Número de asegurados |
| `step2` | Fecha de nacimiento del titular |
| `step4` | Fecha de inicio |
| `step5` | ¿Tienes seguro con FIATC? |
| `step6` | Email (CTA: "Aceptar") |
| `step6b` | WhatsApp opcional |
| `stepLoading` | Spinner de cálculo |
| `step7` | **Resultados** (página principal de producto) |

---

## Navegación: flujo de contratación

```js
let contractMode = false;
let contractStep = 0; // 1-based, mapea a step(7 + contractStep)
```

- `startContratacion()` activa `contractMode = true`, `contractStep = 1`, muestra `step8`
- `nextContractStep()` incrementa `contractStep` y muestra el siguiente step
- Los pasos de contratación son `step8` → `step20` (algunos pueden estar vacíos o ser placeholders)

---

## Spinners de loading

Hay dos spinners:
- `stepLoading` — spinner de cálculo de precio (entre cotización y resultados)
- `stepPayLoading` — spinner de procesamiento de pago

`showLoading()` arranca el spinner de cálculo con textos rotativos:

```js
const texts = [
  'Médico en 24h, sin desplazarte...',
  'Teleconsulta incluida en tu plan...',
  'Calculando el precio para ti...',
  'Casi listo...',
];
```

Estos textos están hardcodeados como placeholder del arquetipo "joven" — están pendientes de hacerse dinámicos por arquetipo.

### Clase de estado del frame durante loading

```js
document.querySelector('.phone-frame').classList.add('loading-active');
// Oculta el footer durante el spinner
```

---

## Personalización por arquetipo (pendiente de implementar)

Perfil completo tras `step2` (fecha de nacimiento del titular).

| Arquetipo | Condición |
|---|---|
| **Joven independiente** | titular < 35 años, `insuredCount === 1` |
| **Familia en expansión** | `insuredCount >= 2` con algún menor |
| **Pre-jubilado activo** | titular >= 50 años |

Función pendiente: `inferArchetype()` que lea el año del input del titular (generado por `dobFieldHTML(1)`) y el valor de `insuredCount`.

Elementos a personalizar cuando se implemente:
- Textos del spinner `showLoading()`
- Título y subtítulo en `step7` pestaña "Para ti" (`step7Title`, `step7Sub`)
- Social proof highlight encima de "Por qué elegir FIATC" en `step7`

---

## Página de resultados (step7)

### Estructura

```
filter-tabs (4 pestañas arriba)
  ↓
results-summary: h1#step7Title + p#step7Sub
  ↓
products-carousel (scroll horizontal de cards)
  ↓
stats de social proof (571.674 clientes · 8,8 valoración)
  ↓
why-section
  - why-title "¿Por qué elegir FIATC?"
  - reviews-scroll (carousel horizontal de testimonios)
  - why-list (accordion de razones)
  ↓
help-section (FAQs)
```

### Pestañas de filtro y sus copies

```js
selectFilter(filter, btn) // actualiza tab activa, título y subtítulo
```

| Pestaña | `data-title` | `data-sub` |
|---|---|---|
| Para ti | "Las opciones más populares en clientes como tú" | "Ideales para parejas jóvenes en Barcelona" *(placeholder, pendiente personalización)* |
| Con copago | "El equilibrio entre precio y cobertura" | "Si prefieres cuota mensual baja y pagar algo en cada visita" |
| Sin copago | "Cada visita incluida, sin sorpresas" | "Para quien usa mucho el seguro y prefiere precio fijo" |
| Reembolso | "Libertad total para elegir dónde te atienden" | "Para quien quiere seguir con su médico de confianza" |

---

## Bottom sheets

Patrón compartido: `.interes-sheet` + `.interes-content` + clase `.open`.

| Sheet | Función abrir | Función cerrar |
|---|---|---|
| Interés en producto | `openInteresSheet(btn)` | `closeInteresSheet()` |
| Portabilidad | `openPortabilidadSheet()` | `closePortabilidadSheet()` |
| Hablemos (help) | abre con JS | cierra con JS |
| Interés (cotización) | abre con JS | cierra con JS |

---

## Asegurados

```js
let insuredCount = 0;
function insuredBlockHTML(id, label, removable) { ... }
function dobFieldHTML(id) { ... } // genera campos DD / Mes / AAAA
```

- El input del año del titular se genera dentro de `dobFieldHTML(1)`
- Los inputs no tienen ID explícito en el año — el campo AAAA es el tercer input del bloque

---

## Hack de teclado (DEV only)

Permite navegar entre pasos con las teclas de flecha. Sincroniza `stepFlowIdx`, `contractMode` y `contractStep` tras cada navegación.

```js
document.addEventListener('keydown', function(e) { ... });
// ArrowRight / ArrowDown → avanzar
// ArrowLeft / ArrowUp → retroceder
// Ignora .step-loading para no quedarse colgado en spinners
```

---

## Componentes clave CSS

| Clase | Descripción |
|---|---|
| `.step` | Cada pantalla del funnel. Oculta por defecto, visible con `.active` |
| `.step-loading` | Pantalla de spinner. También necesita `.active` |
| `.btn-primary` | CTA principal, fondo oscuro |
| `.btn-skip` | Link secundario, negro sin subrayado |
| `.filter-tabs` | Pill-track con fondo blanco y borde `--wf-20` |
| `.filter-tab.active` | Fondo `--wf-20`, texto `--wf-100`, bold |
| `.product-card` | Card de producto en resultados |
| `.cp-info` | Bloque de información contextual con icono info |
| `.legal-mini` | Texto legal pequeño (12px, `--wf-60`) |
| `.legal-more` | Texto expandible, oculto por defecto |
| `.step-icon-badge` | Círculo con icono, 64px. Email y WA tienen fondo `--wf-20` |
| `.review-card` | Card de testimonio en carousel horizontal |
| `.reviews-scroll` | Contenedor scroll horizontal, sangra a los bordes con `margin: 0 -24px` |
| `.why-title` | Título de sección, alineado a la izquierda |

---

## Pendiente de implementar

1. **`inferArchetype()`** — leer edad titular e `insuredCount`, retornar `'joven' | 'familia' | 'prejubilado'`
2. **Textos dinámicos del spinner** por arquetipo
3. **Título/subtítulo de "Para ti"** dinámico por arquetipo
4. **Social proof highlight** en `step7` dinámico por arquetipo

---

## Convenciones de edición

- Editar siempre el archivo único `wireframe_mobile.html`
- No crear archivos adicionales
- No añadir dependencias externas (CDN, fonts, etc.)
- Usar solo las variables CSS `--wf-*` para colores
- Los SVGs de iconos van inline
- No añadir comentarios salvo que el WHY sea no obvio
