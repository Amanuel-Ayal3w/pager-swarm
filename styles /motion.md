# Motion and Interactions

Quick, quiet transitions (150ms), with signature motion that carries the personality: typing text, line drawing, rotating list, endless rail.

- Default to 150ms transitions (43% of measured ones).
- Ease with cubic-bezier(0.4, 0, 0.2, 1).
- Animate stroke, background-color, color, border-color; avoid animating layout.
- Stagger repeated items: line drawing starts each one 70ms after the last.
- Looping motion is slow and steady (several seconds per cycle), never frantic.
- Turn every loop and decorative animation off under prefers-reduced-motion, as the site does.

## Signature motion

The animations that make this site feel like itself. Recreate the behaviour with your own elements and content; the keyframes are the measured reference.

### Typing text

Text types itself in character by character (steps()), holds, then clears, looping every 9.6s, choreographed with 2 other animations on the same clock. It runs on its own, on list items.

```css
@keyframes farm-terminal-command-type { 0% { opacity: 1; width: 0px; } 2% { opacity: 1; width: 0px; animation-timing-function: steps(8); } 7%, 88% { opacity: 1; width: 8ch; } 94%, 99.99% { opacity: 0; width: 8ch; } 100% { opacity: 1; width: 0px; } }
.farm-terminal-command-type { animation: farm-terminal-command-type 9600ms ease infinite; }
```

### Line drawing

SVG lines draw themselves in over 520ms with cubic-bezier(0.22, 1, 0.36, 1), staggered 70ms apart. It runs on its own, on SVG paths.

```css
@keyframes farm-route-draw { 100% { stroke-dashoffset: 0; } }
.farm-route-draw { animation: farm-route-draw 520ms cubic-bezier(0.22, 1, 0.36, 1) both; /* + 70ms delay per item */ }
```

### Rotating list

32 items take turns: each fades and rises in, holds, then leaves, looping every 12s, staggered 3s apart. It runs on its own, on list items.

```css
@keyframes benchmark-comparison-cycle { 0% { opacity: 0; transform: translateY(46%); } 4%, 22% { opacity: 1; transform: translate(0px, 0px); } 25%, 100% { opacity: 0; transform: translateY(-42%); } }
.benchmark-comparison-cycle { animation: benchmark-comparison-cycle 12000ms cubic-bezier(0.22, 1, 0.36, 1) infinite; /* + 3000ms delay per item */ }
```

### Endless rail

A strip scrolls sideways forever, one pass every 96s, linear. It runs on its own, on blocks.

```css
@keyframes farm-logo-rail { 0% { transform: translate(0px, 0px); } 100% { transform: translate(-50%); } }
.farm-logo-rail { animation: farm-logo-rail 96000ms linear infinite; }
```

### Wipe reveal

Content is wiped into view with clip-path, on a 9.6s loop. It runs on its own, on blocks.

```css
@keyframes farm-terminal-output { 0%, 12% { clip-path: inset(0px 0px 100%); opacity: 1; animation-timing-function: steps(6, start); } 68%, 88% { clip-path: inset(0px); opacity: 1; animation-timing-function: linear; } 94%, 99.99% { clip-path: inset(0px); opacity: 0; } 100% { clip-path: inset(0px 0px 100%); opacity: 1; } }
.farm-terminal-output { animation: farm-terminal-output 9600ms ease infinite; }
```

### Refusal shake

Shakes side to side over 450ms to say no. It starts when its state changes (opened, selected, shown).

```css
@keyframes iso-refuse { 20%, 60% { transform: translate(-1.5px); } 40%, 80% { transform: translate(1.5px); } }
.iso-refuse { animation: iso-refuse 450ms ease-in-out both; }
```

### Hard blink

Switches hard on and off every 800ms, no fade (cursors and carets). It runs on its own, on list items, blocks, SVG text.

```css
@keyframes farm-terminal-cursor-blink { 0%, 48% { opacity: 1; } 49%, 100% { opacity: 0; } }
.farm-terminal-cursor-blink { animation: farm-terminal-cursor-blink 800ms linear infinite; }
```

### Pulse

Breathes in opacity or scale every 6s with ease-in-out. It starts when its state changes (opened, selected, shown).

```css
@keyframes blog-ascii-wave { 0%, 100% { opacity: 0.65; transform: translate(-8px); } 50% { opacity: 1; transform: translate(8px); } }
.blog-ascii-wave { animation: blog-ascii-wave 6000ms ease-in-out infinite; }
```

## Interactions

- **Hover** changes text colour (59% of hover rules), background colour (46% of hover rules), background (40% of hover rules), border (16% of hover rules), underline (12% of hover rules), position or scale (10% of hover rules). Things rarely move on hover; they change colour.
- **Illustrations** are line art: thin strokes that stay thin at any size (vector-effect: non-scaling-stroke) on flat fills. Highlight a part by brightening its stroke, not by adding colour.

Animations started by people or state:

- `blog-digit-roll`: enter, 1400ms cubic-bezier(0.16, 1, 0.3, 1), starts when its state changes (opened, selected, shown).
- `blog-ascii-wave`: pulse, 6000ms ease-in-out, starts when its state changes (opened, selected, shown).
- `blog-cursor-blink`: blink, 1200ms step-end, starts when its state changes (opened, selected, shown).
- `agent-waitlist-pixel-on`: pulse, 650ms ease-in-out, starts when its state changes (opened, selected, shown).
- `iso-refuse`: shake, 450ms ease-in-out, starts when its state changes (opened, selected, shown).
- `fd-ai-fade-in`: enter, 150ms ease-out, starts when its state changes (opened, selected, shown).

## Measurements

- Durations: 150ms (43%), 180ms (27%), 200ms (9%), 260ms (9%), 160ms (7%)
- Easings: `cubic-bezier(0.4, 0, 0.2, 1)`, `linear`, `ease`, `cubic-bezier(0.22, 1, 0.36, 1)`
- Animated properties: stroke, background-color, color, border-color, opacity, transform, text-decoration-color, outline-color

The site turns its motion off under `prefers-reduced-motion: reduce`. Do the same: every looping or decorative animation stops, and state changes happen instantly.
