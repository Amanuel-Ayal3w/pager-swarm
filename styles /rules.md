# farmjs.dev: design rules

A dark interface on a near-black neutral background where a green accent marks the next step. Type is Geist Pixel Square, corners are 3px, and depth comes from soft neutral shadows.

## Principles

### Soft, neutral depth

Lift raised elements with the measured shadow (rgba(255, 255, 255, 0.68) 2px 0px 0px 0px inset).

_Why:_ Shadows appear on about 7% of elements; they mark what floats above the page and are never tinted.

### Even, compact hierarchy

Keep type sizes close together, anchored on 16px body text.

_Why:_ The largest measured size is only 2.3× the body size; hierarchy comes from weight and spacing instead.

### A steady rhythm

Space everything on the 4px grid: 3, 4, 8, 12, 16, 20, 24, 32px.

_Why:_ 80% of measured spacing values fall on this grid, which is what makes the layout feel ordered.

### Crisp corners

Use 3px corners as the default radius.

_Why:_ It is the most common measured radius; one radius family is what makes separate components feel like one product.

## Never

- **Never tint shadows with colour.** Every measured shadow is neutral; a coloured glow would read as a different product.
- **Never introduce a second accent colour.** Only one saturated colour (#4ade80) carries weight in the measured palette.
- **Never animate longer than 260ms.** Every measured transition finishes within 260ms; slower motion would feel heavy here.
- **Never use spacing off the 4px grid.** 80% of measured spacing sits on it.

## Colour

- Dark theme: near-black neutral background (#000000) with #070707 surfaces.
- Body text #ffffff on the background reads at 21.0:1; secondary text uses #7a7a7a.
- Accent #4ade80 (green) with #000000 text on top of it.

## Typography

- Geist Pixel Square for headings, Geist Sans for body, Geist Mono for code.
- Scale: h1 36px, h2 30px, h3 24px, h4 20px, body 16px, small 14px, caption 11px.
- Weights in use: 300, 350, 400, 500.

## Shape and depth

- Radii: 2px (4%), 3px (48%), 4px (4%), 5px (13%), 6px (10%), pill (20%).
- Borders: 1px in #1f1f1f.
- Shadows: rgba(255, 255, 255, 0.68) 2px 0px 0px 0px inset | rgba(0, 0, 0, 0.18) 0px 18px 50px 0px | rgba(255, 255, 255, 0.85) 0px -1px 0px 0px inset.
