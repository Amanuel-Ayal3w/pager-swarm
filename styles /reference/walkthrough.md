# Walkthrough: how the page is built and how it moves

One part per top-level section, top to bottom, as measured at 1440 px. Sizes are CSS pixels; colours are as computed. Every file named here is in this folder. How things move and behave (scrolling, page changes, the menu, hovers), step by step, is in `reference/motion/README.md`.

## 01 · div

- **Box:** 1440×8805 px, starting 29 px from the top. Background rgb(0, 0, 0), text rgb(255, 255, 255).
- **Layout:** stacked blocks.
- **Type:** Geist Mono 400 10px/15px (family weight size/line-height, most text first).
- **Inside:** 1 link.
- **Look:** `reference/sections/01-div.jpg` and its anatomy `reference/sections/01-div.anatomy.jpg`.
- **Markup:** `reference/sections/01-div.html`.
- **Pictures:** `reference/assets/images/038-canvas.png` (1240×384).
- **Hover:** `.hover\:text-white:hover` changes color; `.hover\:decoration-white:hover` changes text-decoration.

## 02 · header

- **Box:** 1440×44 px, starting 29 px from the top. Background rgba(0, 0, 0, 0.94), text rgb(255, 255, 255).
- **Layout:** flex row of 4, gap normal, normal/stretch.
- **Type:** Geist Mono 400 10px/15px · Geist Sans 400 16px/24px · Geist Mono 400 11px/16.5px (family weight size/line-height, most text first).
- **Inside:** 17 links, 2 pictures, 16 drawings.
- **Markup:** `reference/sections/02-header.html`.
- **Drawings:** `reference/assets/svg/001-icon-header.svg` (icon, 14×14), `reference/assets/svg/002-icon-header.svg` (icon, 14×14), `reference/assets/svg/003-icon-header.svg` (icon, 14×14), `reference/assets/svg/004-icon-header.svg` (icon, 14×14), `reference/assets/svg/005-icon-header.svg` (icon, 14×14), `reference/assets/svg/006-icon-header.svg` (icon, 14×14), `reference/assets/svg/007-icon-header.svg` (icon, 14×14).
- **Pictures:** `reference/assets/images/004-farming-labs-logo-dark-lwxtiiae.svg`, `reference/assets/images/005-github-qpyq9fjq.svg`, `reference/assets/images/038-canvas.png` (1240×384).
- **Hover:** `.hover\:bg-white\/88:hover` changes background; `.hover\:bg-white\/\[0\.035\]:hover` changes background; `.hover\:bg-white\/\[0\.04\]:hover` changes background; `.hover\:text-white:hover` changes color.
- **Control states:** `reference/components/01-nav-link.jpg` (nav-link a.shrink-0.font-mono:nth-of-type(2): rest, hover, focus).
- **Control states:** `reference/components/02-nav-link.jpg` (nav-link a.flex.h-full:nth-of-type(1): rest, hover, focus).
- **Control states:** `reference/components/03-button.jpg` (button a.inline-flex.h-11:nth-of-type(2): rest, hover, focus).

## 03 · hero

- **Box:** 1440×542 px, starting 73 px from the top. Background rgb(0, 0, 0), text rgb(255, 255, 255).
- **Layout:** flex row of 3, gap 6px, normal/center.
- **Type:** Geist Mono 350 10px/15px · Geist Sans 300 13px/21.45px · Geist Sans 400 64px/68.48px · Geist Mono 400 10px/15px · Geist Mono 400 9px/13.5px (family weight size/line-height, most text first).
- **Inside:** 1 heading, 1 paragraph, 6 buttons, 2 links, 4 pictures, 5 drawings.
- **Look:** `reference/sections/03-hero.jpg` and its anatomy `reference/sections/03-hero.anatomy.jpg`.
- **Markup:** `reference/sections/03-hero.html`.
- **Drawings:** `reference/assets/svg/008-illustration-hero.svg` (illustration, 508×165), `reference/assets/svg/009-icon-hero.svg` (icon, 18×18), `reference/assets/svg/010-icon-hero.svg` (icon, 10×10), `reference/assets/svg/011-icon-hero.svg` (icon, 10×10), `reference/assets/svg/012-icon-hero.svg` (icon, 10×10).
- **Pictures:** `reference/assets/images/006-npm-czs-0-kf.svg`, `reference/assets/images/007-yarn-dplun-jd.svg`, `reference/assets/images/008-pnpm-dfcrvzz2.svg`, `reference/assets/images/009-bun-bpknyn70.svg`, `reference/assets/images/038-canvas.png` (1240×384).
- **Motion:**
  - choreography: 5 elements (svg, a, span, div) animate `transform` starting 948–5816 ms after load, about 793 ms apart, each for about 19272 ms
  - choreography: 7 elements (svg, span, div, path) animate `opacity` starting 948–948 ms after load together, each for about 18231 ms
  - script writes `transform` on `section.farm-full-rule.farm-hero-rule:nth-of-type(1) > div.relative.z-10:nth-of-type(1) > div.farm-hero-title.relative:nth-of-type(2) > div.farm-sw-layer > svg:nth-of-type(2)` 335 times over 21368 ms (on load): from `translate3d(-27.2356px, 44.6321px, 0px) scale(1)` to `translate3d(435.952px, 173.336px, 0px) scale(1)`
  - script writes `width` on `div.relative.z-10:nth-of-type(1) > div.farm-hero-title.relative:nth-of-type(2) > h1.max-w-full.font-medium > span.block.whitespace-nowrap:nth-of-type(2) > span.farm-hero-swap` 217 times over 22165 ms (loops): from `auto` to `326.094px`
  - script writes `width` on `section.farm-full-rule.farm-hero-rule:nth-of-type(1) > div.relative.z-10:nth-of-type(1) > div.farm-hero-title.relative:nth-of-type(2) > div.farm-sw-layer > div.farm-sw-select` 190 times over 20757 ms (on load): from `0.0022034px` to `346.574px`
  - script writes `height` on `section.farm-full-rule.farm-hero-rule:nth-of-type(1) > div.relative.z-10:nth-of-type(1) > div.farm-hero-title.relative:nth-of-type(2) > div.farm-sw-layer > div.farm-sw-select` 122 times over 19975 ms (on load): from `0.0003251px` to `74.8688px`
  - script writes `opacity` on `section.farm-full-rule.farm-hero-rule:nth-of-type(1) > div.relative.z-10:nth-of-type(1) > div.farm-hero-title.relative:nth-of-type(2) > div.farm-sw-layer > svg:nth-of-type(2)` 91 times over 22161 ms (on load): from `0` to `0`
  - script writes `transform` on `main > section.farm-full-rule.farm-hero-rule:nth-of-type(1) > div.relative.z-10:nth-of-type(1) > div.farm-hero-title.relative:nth-of-type(2) > a.farm-hero-tag` 74 times over 22161 ms (on load): from `translate3d(555.562px, 152.938px, 0px) scale(1)` to `translate3d(394.734px, 152.938px, 0px) scale(1)`
  - and 13 more recorded tracks (motion.json `recorded`)
- **Hover:** `.farm-hero-tag[data-sw-state="on"]:hover` changes background, border-color; `.hover\:bg-white\/88:hover` changes background; `.hover\:bg-white\/\[0\.055\]:hover` changes background; `.hover\:bg-white\/\[0\.075\]:hover` changes background; `.hover\:text-white:hover` changes color; `.group:hover .group-hover\:opacity-90` changes opacity.
- **Control states:** `reference/components/04-button.jpg` (button a.inline-flex.min-w-0: rest, hover, focus).

## 04 · section

- **Box:** 1440×64 px, starting 615 px from the top. Background rgb(0, 0, 0), text rgb(255, 255, 255).
- **Layout:** grid, 2 columns (224px 1016px), gap normal.
- **Type:** Geist Mono 400 11px/16.5px · Geist Mono 400 10px/15px (family weight size/line-height, most text first).
- **Inside:** 48 links, 48 pictures, 1 drawing.
- **Look:** `reference/sections/04-section.jpg` and its anatomy `reference/sections/04-section.anatomy.jpg`.
- **Markup:** `reference/sections/04-section.html`.
- **Drawings:** `reference/assets/svg/013-icon-section.svg` (icon, 14×14).
- **Pictures:** `reference/assets/images/010-react-chwnrnxy.svg`, `reference/assets/images/011-stripe-c0dozjf.svg`, `reference/assets/images/012-cloudflare-dropbqrh.svg`, `reference/assets/images/013-betterauth-symz-vfv.svg`, `reference/assets/images/014-vercel-cibc0le.svg`, `reference/assets/images/015-inngest-drlwhelo.svg`, `reference/assets/images/016-vite-b-cd16dj.svg`, `reference/assets/images/017-supabase-d6vee-ys.svg`, `reference/assets/images/018-trigger-cg-qosvn.svg`, `reference/assets/images/019-docker-bdqjcm6t.svg`.
- **Motion:**
  - CSS `farm-logo-rail` 96s linear infinite on 1 element (e.g. `main > section.farm-full-rule.w-full:nth-of-type(2) > div.grid.h-16 > div.farm-logo-viewport.min-w-0:nth-of-type(2) > div.farm-logo-rail.flex`)
- **Hover:** `.farm-logo-viewport:hover .farm-logo-rail` changes animation; `.hover\:bg-white\/\[0\.07\]:hover` changes background; `.hover\:text-white\/82:hover` changes color.

## 05 · section

- **Box:** 1440×1679 px, starting 679 px from the top. Background rgb(0, 0, 0), text rgb(255, 255, 255).
- **Layout:** grid, 2 columns (620px 620px), gap normal.
- **Type:** ui-monospace 400 11px/24px · Geist Sans 300 16px/24px · ui-monospace 400 10.5px/20px · Geist Pixel Square 500 24px/32px · ui-monospace 400 11px/18px (family weight size/line-height, most text first).
- **Inside:** 6 headings, 6 paragraphs, 3 buttons, 1 link, 15 drawings.
- **Look:** `reference/sections/05-section.jpg` and its anatomy `reference/sections/05-section.anatomy.jpg`.
- **Markup:** `reference/sections/05-section.html`.
- **Drawings:** `reference/assets/svg/014-icon-section.svg` (icon, 14×14), `reference/assets/svg/015-icon-section.svg` (icon, 12×12), `reference/assets/svg/016-icon-section.svg` (icon, 14×14), `reference/assets/svg/017-icon-section.svg` (icon, 12×12, ×4), `reference/assets/svg/018-icon-section.svg` (icon, 14×14), `reference/assets/svg/019-icon-section.svg` (icon, 12×12, ×5), `reference/assets/svg/020-icon-section.svg` (icon, 14×14), `reference/assets/svg/021-icon-section.svg` (icon, 12×12), `reference/assets/svg/022-icon-section.svg` (icon, 14×14), `reference/assets/svg/023-icon-section.svg` (icon, 12×12), `reference/assets/svg/024-icon-section.svg` (icon, 14×14, ×2), `reference/assets/svg/025-icon-section.svg` (icon, 10×10), and 1 more.
- **Pictures:** `reference/assets/images/038-canvas.png` (1240×384).
- **Motion:**
  - CSS `farm-terminal-command-type` 9.6s ease infinite on 1 element (e.g. `pre.min-h-0.flex-1 > code.block.min-w-0 > span.block.min-w-max > span.block.h-5:nth-of-type(1) > span.farm-terminal-command-text.inline-block:nth-of-type(2)`)
  - CSS `farm-terminal-cursor-window` 9.6s linear infinite on 1 element (e.g. `pre.min-h-0.flex-1 > code.block.min-w-0 > span.block.min-w-max > span.block.h-5:nth-of-type(1) > span.farm-terminal-command-cursor.inline-block:nth-of-type(3)`)
  - CSS `farm-terminal-cursor-blink` 0.8s steps(1) infinite on 4 elements (e.g. `pre.min-h-0.flex-1 > code.block.min-w-0 > span.block.min-w-max > span.block.h-5:nth-of-type(1) > span.farm-terminal-command-cursor.inline-block:nth-of-type(3)::before`)
  - CSS `farm-terminal-output` 9.6s ease infinite on 1 element (e.g. `figure.relative.z-10 > pre.min-h-0.flex-1 > code.block.min-w-0 > span.block.min-w-max > span.farm-terminal-output.block:nth-of-type(2)`)
  - CSS `farm-build-command-type` 10.8s ease infinite on 1 element (e.g. `figure.relative.z-10 > pre.min-h-0.flex-1 > code.block.min-w-0 > span.block.h-5:nth-of-type(1) > span.farm-build-command-text.inline-block:nth-of-type(2)`)
  - CSS `farm-build-cursor-window` 10.8s linear infinite on 1 element (e.g. `figure.relative.z-10 > pre.min-h-0.flex-1 > code.block.min-w-0 > span.block.h-5:nth-of-type(1) > span.farm-build-command-cursor.inline-block:nth-of-type(3)`)
  - CSS `farm-build-output` 10.8s ease infinite on 1 element (e.g. `div.farm-feature-spotlight.relative:nth-of-type(2) > figure.relative.z-10 > pre.min-h-0.flex-1 > code.block.min-w-0 > span.farm-build-output.mt-2:nth-of-type(2)`)
  - script writes `data-typewriter-phase` on `pre.min-h-0.max-w-full > code.farm-highlighted-code.block > span.sh__line.sh__line--highlighted:nth-of-type(4) > span.farm-renderer-value:nth-of-type(3) > span.farm-inline-typewriter` 17 times over 18513 ms (loops): from `deleting` to `typing`
- **Hover:** `.hover\:bg-white\/\[0\.035\]:hover` changes background; `.hover\:bg-white\/\[0\.04\]:hover` changes background; `.hover\:text-white:hover` changes color; `.hover\:text-white\/68:hover` changes color; `.group:hover .group-hover\:-translate-y-0\.5` changes transform; `.group:hover .group-hover\:translate-x-0\.5` changes transform.

## 06 · benchmarks

- **Box:** 1440×1809 px, starting 2358 px from the top. Background rgb(0, 0, 0), text rgb(255, 255, 255).
- **Layout:** grid, 2 columns (620px 620px), gap normal.
- **Type:** Geist Sans 400 16px/24px · Geist Sans 500 30px/36px · Geist Mono 400 8px/12px · Geist Mono 400 9px/13.5px · Geist Sans 300 14px/20px (family weight size/line-height, most text first).
- **Inside:** 5 headings, 11 paragraphs, 10 drawings.
- **Look:** `reference/sections/06-benchmarks.jpg` and its anatomy `reference/sections/06-benchmarks.anatomy.jpg`.
- **Markup:** `reference/sections/06-benchmarks.html`.
- **Drawings:** `reference/assets/svg/027-icon-benchmarks.svg` (icon, 16×16), `reference/assets/svg/028-illustration-benchmarks.svg` (illustration, 540×265, animated), `reference/assets/svg/029-icon-benchmarks.svg` (icon, 16×16), `reference/assets/svg/030-illustration-benchmarks.svg` (illustration, 539×265), `reference/assets/svg/031-icon-benchmarks.svg` (icon, 16×16), `reference/assets/svg/032-illustration-benchmarks.svg` (illustration, 540×265), `reference/assets/svg/033-icon-benchmarks.svg` (icon, 16×16), `reference/assets/svg/034-illustration-benchmarks.svg` (illustration, 539×265), `reference/assets/svg/035-icon-benchmarks.svg` (icon, 16×16), `reference/assets/svg/036-illustration-benchmarks.svg` (illustration, 1240×640).
- **Pictures:** `reference/assets/images/038-canvas.png` (1240×384).
- **Motion:**
  - CSS `benchmark-comparison-cycle` 12s cubic-bezier(0.22, 1, 0.36, 1) infinite on 32 elements (e.g. `article.flex.flex-col > h3.mt-4.max-w-xl > span.mt-1.grid:nth-of-type(3) > span.benchmark-comparison-rotator.block:nth-of-type(1) > span.benchmark-comparison-item.block:nth-of-type(1)`, staggered: -0.48s, 2.52s, 5.52s, 8.52s)
  - choreography: 35 elements (polygon) animate `points` starting 1011–3502 ms after load, about 166 ms apart, each for about 21911 ms
  - choreography: 17 elements (path) animate `d` starting 1011–1844 ms after load, about 136 ms apart, each for about 22057 ms, and keep looping
  - choreography: 15 elements (circle) animate `cy` starting 1048–1844 ms after load, about 166 ms apart, each for about 22047 ms, and keep looping
  - choreography: 5 elements (circle) animate `cx` starting 1048–1048 ms after load together, each for about 22078 ms
  - choreography: 6 elements (g) animate `data-linked` starting 1011–1381 ms after load, about 141 ms apart, each for about 20962 ms, and keep looping
  - script writes `points` on `article.flex.flex-col > div.benchmark-illustration.benchmark-hairline > svg > g:nth-of-type(2) > polygon` 771 times over 22078 ms (on load): from `-48.26,-33.52 -47.71,-33.14 -47.42,-32.70 -47.42,-32.23 -47.71,-31.78 -48.26,-31.40 -57.28,-26.89 -58.03,-26.62 -58.93,-26.47 -59.87,-26.47 -60.76,-26.62 -61.52` to `-48.26,-88.24 -47.71,-87.86 -47.42,-87.42 -47.42,-86.95 -47.71,-86.50 -48.26,-86.12 -57.28,-81.61 -58.03,-81.34 -58.93,-81.19 -59.87,-81.19 -60.76,-81.34 -61.52`
  - script writes `d` on `div.benchmark-illustration.benchmark-hairline > svg > g:nth-of-type(7) > g > path` 771 times over 22078 ms (on load): from `M-59.40,-32.46L-59.40,-32.46` to `M-59.40,-87.18L-59.40,-87.18`
  - script writes `cy` on `div.benchmark-illustration.benchmark-hairline > svg > g:nth-of-type(7) > g > circle` 771 times over 22078 ms (on load): from `-32.46` to `-87.18`
  - script writes `d` on `div.benchmark-illustration.benchmark-hairline > svg > g:nth-of-type(11) > g > path` 771 times over 22078 ms (on load): from `M-46.43,-15.37L-46.43,-15.37` to `M2.80,9.24L2.80,9.24`
  - script writes `cx` on `div.benchmark-illustration.benchmark-hairline > svg > g:nth-of-type(11) > g > circle` 771 times over 22078 ms (on load): from `-46.43` to `2.80`
  - script writes `cy` on `div.benchmark-illustration.benchmark-hairline > svg > g:nth-of-type(11) > g > circle` 764 times over 22078 ms (on load): from `-15.37` to `9.24`
  - and 74 more recorded tracks (motion.json `recorded`)
  - scripts add `.hl-sign`, `.hl-led-on` to 91 elements as the page scrolls (first at scrollY 0)
- **Film:** `reference/motion/films/04-drawing-benchmarks.jpg` (Looping drawing: 62 moving parts (d, cy, points, cx); it is `section#benchmarks:nth-of-type(4) > div.grid.bg-black:nth-of-type(1) > article.flex.flex-col > div.benchmark-illustration.benchmark-hairline > svg` in the markup; frames captioned with ms).
- **Film:** `reference/motion/films/05-drawing-benchmarks.jpg` (Looping drawing: 17 moving parts (points, d, cx, cy); it is `div.grid.bg-black:nth-of-type(1) > div.border-t:nth-of-type(1) > article.flex.flex-col > div.benchmark-illustration.benchmark-hairline > svg` in the markup; frames captioned with ms).
- **Hover:** `.hover\:bg-white\/\[0\.045\]:hover` changes background; `.hover\:text-white:hover` changes color; `.benchmark-series:hover .benchmark-series-line` changes filter, stroke-opacity, stroke-width; `.benchmark-point:hover .benchmark-point-ring` changes fill-opacity, opacity, stroke-opacity, transform; `.benchmark-point:hover .benchmark-point-tooltip` changes opacity, transform.

## 07 · integrations

- **Box:** 1440×440 px, starting 4167 px from the top. Background rgb(0, 0, 0), text rgb(255, 255, 255).
- **Layout:** grid, 2 columns (224px 1016px), gap normal.
- **Type:** Geist Sans 300 16px/24px · Geist Mono 400 7px/10.5px · Geist Sans 400 36px/40px · Geist Mono 400 11px/16.5px · Geist Mono 400 10px/15px (family weight size/line-height, most text first).
- **Inside:** 1 heading, 1 paragraph, 17 links, 15 pictures, 2 drawings.
- **Look:** `reference/sections/07-integrations.jpg` and its anatomy `reference/sections/07-integrations.anatomy.jpg`.
- **Markup:** `reference/sections/07-integrations.html`.
- **Drawings:** `reference/assets/svg/037-icon-integrations.svg` (icon, 14×14), `reference/assets/svg/038-icon-integrations.svg` (icon, 28×28).
- **Pictures:** `reference/assets/images/011-stripe-c0dozjf.svg`, `reference/assets/images/013-betterauth-symz-vfv.svg`, `reference/assets/images/015-inngest-drlwhelo.svg`, `reference/assets/images/017-supabase-d6vee-ys.svg`, `reference/assets/images/018-trigger-cg-qosvn.svg`, `reference/assets/images/020-clerk-8wmp9ekc.svg`, `reference/assets/images/021-resend-blaqxsol.svg`, `reference/assets/images/023-polar-df9qfirn.svg`, `reference/assets/images/025-authjs-dcvy7dzg.svg`, `reference/assets/images/026-autumn-bz-s349p.svg`.
- **Hover:** `.hover\:bg-white:hover` changes background; `.hover\:bg-white\/88:hover` changes background; `.hover\:z-10:hover` changes z-index; `.group:hover .group-hover\:-translate-y-1` changes transform; `.group:hover .group-hover\:translate-y-0` changes transform; `.group:hover .group-hover\:text-black` changes color; `.group:hover .group-hover\:opacity-100` changes opacity; `.group:hover .group-hover\:invert-0` changes filter.

## 08 · section

- **Box:** 1440×2287 px, starting 4607 px from the top. Background rgb(0, 0, 0), text rgb(255, 255, 255).
- **Layout:** grid, 2 columns (620px 620px), gap normal.
- **Type:** Geist Sans 300 16px/24px · ui-monospace 400 11px/24px · ui-monospace 400 10.5px/20px · Geist Pixel Square 500 24px/32px · Geist Mono 400 10px/15px (family weight size/line-height, most text first).
- **Inside:** 8 headings, 8 paragraphs, 14 buttons, 2 links, 9 pictures, 38 drawings.
- **Look:** `reference/sections/08-section.jpg` and its anatomy `reference/sections/08-section.anatomy.jpg`.
- **Markup:** `reference/sections/08-section.html`.
- **Drawings:** `reference/assets/svg/039-icon-section.svg` (icon, 14×14), `reference/assets/svg/040-icon-section.svg` (icon, 14×14), `reference/assets/svg/041-icon-section.svg` (icon, 12×12), `reference/assets/svg/042-icon-section.svg` (icon, 12×12, ×4), `reference/assets/svg/043-icon-section.svg` (icon, 14×14, ×4), `reference/assets/svg/044-icon-section.svg` (icon, 14×14, ×2), `reference/assets/svg/045-icon-section.svg` (icon, 14×14), `reference/assets/svg/046-icon-section.svg` (icon, 14×14), `reference/assets/svg/047-illustration-section.svg` (illustration, 241×208, animated), `reference/assets/svg/048-illustration-section.svg` (illustration, 578×243, animated), `reference/assets/svg/049-icon-section.svg` (icon, 12×12), `reference/assets/svg/050-icon-section.svg` (icon, 12×12), and 13 more.
- **Pictures:** `reference/assets/images/012-cloudflare-dropbqrh.svg`, `reference/assets/images/014-vercel-cibc0le.svg`, `reference/assets/images/019-docker-bdqjcm6t.svg`, `reference/assets/images/022-nitro-dmsvjzf4.svg`, `reference/assets/images/024-netlify-djrbvton.svg`, `reference/assets/images/033-firebase-cp-1xkbf.svg`, `reference/assets/images/034-render-s5zqhtqy.svg`, `reference/assets/images/035-nodedotjs-cxezsdot.svg`, `reference/assets/images/036-deno-cuqrn-5.svg`.
- **Motion:**
  - CSS `farm-route-caret` 1s steps(1) infinite on 1 element (e.g. `div.hidden.min-w-0 > div.farm-route-explorer.flex > svg > text:nth-of-type(1) > tspan`)
  - CSS `farm-route-draw` 0.52s cubic-bezier(0.22, 1, 0.36, 1) ×1 on 9 elements (e.g. `div.hidden.min-w-0 > div.farm-route-explorer.flex > svg > g:nth-of-type(3) > path:nth-of-type(1)`, staggered: 0s, 0.07s, 0.14s, 0.21s, 0.28s)
  - CSS `farm-route-fade` 0.16s ease-out ×1 on 1 element (e.g. `div.relative.z-10 > div.flex.min-w-0 > div.relative.flex:nth-of-type(2) > svg > rect`)
  - CSS `bf-spin` 0.9s linear infinite on 1 element (e.g. `div.bf-panel > div.bf-body:nth-of-type(2) > span.bf-item.bf-von:nth-of-type(2) > span.bf-item-state:nth-of-type(3) > span.bf-st.bf-st--run`)
  - choreography: 4 elements (circle) animate `cx` starting 1942–2784 ms after load, about 842 ms apart, each for about 16912 ms
  - choreography: 4 elements (circle) animate `cy` starting 1942–2784 ms after load, about 842 ms apart, each for about 16912 ms
  - choreography: 8 elements (circle) animate `opacity` starting 948–948 ms after load together, each for about 17906 ms, and keep looping
  - choreography: 3 elements (div) animate `data-state` starting 1350–3160 ms after load, about 992 ms apart, each for about 17068 ms, and keep looping
  - script writes `stroke-dashoffset` on `figure.blog-figure.blog-figure--fit > div.bf-stage > svg > g:nth-of-type(1) > path` 53 times over 17124 ms (on load): from `146.717` to ``
  - script writes `stroke-dashoffset` on `figure.blog-figure.blog-figure--fit > div.bf-stage > svg > g:nth-of-type(2) > path` 51 times over 17221 ms (on load): from `145.492` to ``
  - script writes `cx` on `figure.blog-figure.blog-figure--fit > div.bf-stage > svg > g:nth-of-type(1) > circle:nth-of-type(3)` 45 times over 16912 ms (on load): from `190` to ``
  - script writes `cx` on `figure.blog-figure.blog-figure--fit > div.bf-stage > svg > g:nth-of-type(1) > circle:nth-of-type(4)` 45 times over 16912 ms (on load): from `190` to ``
  - script writes `cx` on `figure.blog-figure.blog-figure--fit > div.bf-stage > svg > g:nth-of-type(2) > circle:nth-of-type(3)` 43 times over 16903 ms (on load): from `250` to ``
  - script writes `cx` on `figure.blog-figure.blog-figure--fit > div.bf-stage > svg > g:nth-of-type(2) > circle:nth-of-type(4)` 43 times over 16903 ms (on load): from `250` to ``
  - and 17 more recorded tracks (motion.json `recorded`)
  - scripts add `.text-white/46`, `.text-white/28`, `.text-white/40`, `.hover:bg-white/[0.035]`, `.hover:text-white/72`, `.text-white/88`, `.text-white/64`, `.bg-white/[0.055]`, `.text-white/92`, `.bf-flash` to 49 elements as the page scrolls (first at scrollY 0)
- **Film:** `reference/motion/films/02-drawing-section.jpg` (Animated drawing; it is `div.flex.min-w-0 > div.relative.flex:nth-of-type(2) > div.hidden.min-w-0 > div.farm-route-explorer.flex > svg` in the markup; frames captioned with ms).
- **Film:** `reference/motion/films/03-scripted-section.jpg` (Looping div: 83 moving parts (data-state, cx, stroke-dashoffset, cy); it is `article.group.flex:nth-of-type(8) > div.farm-feature-spotlight.relative:nth-of-type(2) > div.relative.z-10 > figure.blog-figure.blog-figure--fit > div.bf-stage` in the markup; frames captioned with ms).
- **Hover:** `.hover\:bg-white\/\[0\.035\]:hover` changes background; `.hover\:text-white\/68:hover` changes color; `.hover\:text-white\/72:hover` changes color; `.hover\:text-white\/88:hover` changes color; `.hover\:decoration-white:hover` changes text-decoration; `.group\/tile:hover .group-hover\/tile\:-translate-y-1` changes transform; `.group\/tile:hover .group-hover\/tile\:translate-y-0` changes transform; `.group\/deployment:hover .group-hover\/deployment\:border-white\/\[0\.14\]` changes border-color; `.group\/deployment:hover .group-hover\/deployment\:bg-white\/\[0\.075\]` changes background; `.group\/tile:hover .group-hover\/tile\:opacity-100` changes opacity.

## 09 · agents

- **Box:** 1440×420 px, starting 6894 px from the top. Background rgb(0, 0, 0), text rgb(255, 255, 255).
- **Layout:** grid, 2 columns (224px 1016px), gap normal.
- **Type:** Geist Sans 300 16px/24px · Geist Sans 400 36px/40px · Geist Sans 400 12.312px/18.468px · Geist Mono 400 10.0958px/15.1438px · Geist Mono 400 11px/16.5px (family weight size/line-height, most text first).
- **Inside:** 1 heading, 1 paragraph, 1 link, 1 picture, 4 drawings.
- **Look:** `reference/sections/09-agents.jpg` and its anatomy `reference/sections/09-agents.anatomy.jpg`.
- **Markup:** `reference/sections/09-agents.html`.
- **Drawings:** `reference/assets/svg/064-icon-agents.svg` (icon, 14×14), `reference/assets/svg/065-icon-agents.svg` (icon, 32×30), `reference/assets/svg/066-icon-agents.svg` (icon, 32×32), `reference/assets/svg/067-illustration-agents.svg` (illustration, 448×280).
- **Pictures:** `reference/assets/images/037-favicon.svg`, `reference/assets/images/038-canvas.png` (1240×384).
- **Motion:**
  - choreography: 4 elements (circle) animate `cx` starting 1531–3338 ms after load, about 1807 ms apart, each for about 19472 ms
  - choreography: 4 elements (circle) animate `cy` starting 1531–3338 ms after load, about 1807 ms apart, each for about 19472 ms
  - choreography: 8 elements (circle) animate `opacity` starting 948–948 ms after load together, each for about 19767 ms, and keep looping
  - choreography: 3 elements (div) animate `data-state` starting 1942–3762 ms after load, about 1191 ms apart, each for about 18563 ms, and keep looping
  - script writes `cx` on `figure.blog-figure.blog-figure--fit > div.bf-stage > svg > g:nth-of-type(1) > circle:nth-of-type(3)` 125 times over 19184 ms (on load): from `136.26131977248002` to ``
  - script writes `cx` on `figure.blog-figure.blog-figure--fit > div.bf-stage > svg > g:nth-of-type(1) > circle:nth-of-type(4)` 125 times over 19184 ms (on load): from `136.26131977248002` to ``
  - script writes `cx` on `figure.blog-figure.blog-figure--fit > div.bf-stage > svg > g:nth-of-type(2) > circle:nth-of-type(3)` 95 times over 19472 ms (on load): from `136.2087105195497` to ``
  - script writes `cx` on `figure.blog-figure.blog-figure--fit > div.bf-stage > svg > g:nth-of-type(2) > circle:nth-of-type(4)` 95 times over 19472 ms (on load): from `136.2087105195497` to ``
  - script writes `cy` on `figure.blog-figure.blog-figure--fit > div.bf-stage > svg > g:nth-of-type(1) > circle:nth-of-type(3)` 76 times over 19184 ms (on load): from `140` to ``
  - script writes `cy` on `figure.blog-figure.blog-figure--fit > div.bf-stage > svg > g:nth-of-type(1) > circle:nth-of-type(4)` 76 times over 19184 ms (on load): from `140` to ``
  - and 17 more recorded tracks (motion.json `recorded`)
  - scripts add `.bf-flash` to 10 elements as the page scrolls (first at scrollY 0)
- **Hover:** `.hover\:bg-white\/88:hover` changes background.

## 10 · section

- **Box:** 1440×583 px, starting 7314 px from the top. Background rgb(0, 0, 0), text rgb(255, 255, 255).
- **Layout:** grid, 2 columns (620px 620px), gap normal.
- **Type:** Geist Sans 300 16px/24px · ui-monospace 400 10.5px/20px · Geist Sans 400 7.69824px/10.7775px · Geist Pixel Square 500 24px/32px · Geist Mono 400 10px/15px (family weight size/line-height, most text first).
- **Inside:** 2 headings, 2 paragraphs, 2 buttons, 8 drawings.
- **Look:** `reference/sections/10-section.jpg` and its anatomy `reference/sections/10-section.anatomy.jpg`.
- **Markup:** `reference/sections/10-section.html`.
- **Drawings:** `reference/assets/svg/068-icon-section.svg` (icon, 14×14), `reference/assets/svg/069-icon-section.svg` (icon, 23×23), `reference/assets/svg/070-icon-section.svg` (icon, 23×23), `reference/assets/svg/071-icon-section.svg` (icon, 22×25, ×2), `reference/assets/svg/072-illustration-section.svg` (illustration, 540×284), `reference/assets/svg/073-icon-section.svg` (icon, 14×14).
- **Motion:**
  - choreography: 4 elements (circle) animate `cy` starting 2177–4712 ms after load, about 2535 ms apart, each for about 20633 ms
  - choreography: 4 elements (circle) animate `cx` starting 2177–4712 ms after load, about 2535 ms apart, each for about 20633 ms
  - choreography: 8 elements (circle) animate `opacity` starting 948–948 ms after load together, each for about 20284 ms, and keep looping
  - script writes `cy` on `figure.blog-figure.blog-figure--fit > div.bf-stage > svg > g:nth-of-type(1) > circle:nth-of-type(3)` 69 times over 20633 ms (on load): from `214` to ``
  - script writes `cy` on `figure.blog-figure.blog-figure--fit > div.bf-stage > svg > g:nth-of-type(1) > circle:nth-of-type(4)` 69 times over 20633 ms (on load): from `214` to ``
  - script writes `cy` on `figure.blog-figure.blog-figure--fit > div.bf-stage > svg > g:nth-of-type(2) > circle:nth-of-type(3)` 63 times over 11795 ms (on load): from `214` to ``
  - script writes `cy` on `figure.blog-figure.blog-figure--fit > div.bf-stage > svg > g:nth-of-type(2) > circle:nth-of-type(4)` 63 times over 11795 ms (on load): from `214` to ``
  - script writes `stroke-dashoffset` on `figure.blog-figure.blog-figure--fit > div.bf-stage > svg > g:nth-of-type(1) > path` 60 times over 20371 ms (on load): from `128.572` to ``
  - script writes `stroke-dashoffset` on `figure.blog-figure.blog-figure--fit > div.bf-stage > svg > g:nth-of-type(2) > path` 58 times over 20450 ms (on load): from `108.678` to ``
  - and 16 more recorded tracks (motion.json `recorded`)
  - scripts add `.bf-flash` to 6 elements as the page scrolls (first at scrollY 0)
- **Hover:** `.hover\:bg-white\/\[0\.035\]:hover` changes background; `.hover\:text-white\/68:hover` changes color.

## 11 · section

- **Box:** 1440×423 px, starting 7897 px from the top. Background rgb(0, 0, 0), text rgb(255, 255, 255).
- **Layout:** grid, 2 columns (224px 1016px), gap normal.
- **Type:** Geist Sans 300 16px/24px · Geist Mono 400 11.18px/16.77px · Geist Mono 400 13px/19.5px · Geist Sans 400 36px/40px · Geist Mono 400 11.18px/17.888px (family weight size/line-height, most text first).
- **Inside:** 1 heading, 1 paragraph, 2 links, 4 drawings.
- **Look:** `reference/sections/11-section.jpg` and its anatomy `reference/sections/11-section.anatomy.jpg`.
- **Markup:** `reference/sections/11-section.html`.
- **Drawings:** `reference/assets/svg/074-icon-section.svg` (icon, 14×14), `reference/assets/svg/075-icon-section.svg` (icon, 14×14, ×2), `reference/assets/svg/076-illustration-section.svg` (illustration, 480×327).
- **Motion:**
  - choreography: 3 elements (path) animate `stroke-dashoffset` starting 1011–1011 ms after load together, each for about 21279 ms
  - choreography: 6 elements (circle) animate `cy` starting 2342–3762 ms after load, about 902 ms apart, each for about 14044 ms
  - choreography: 6 elements (circle) animate `cx` starting 2342–3762 ms after load, about 902 ms apart, each for about 14044 ms, and keep looping
  - choreography: 12 elements (circle) animate `opacity` starting 948–948 ms after load together, each for about 20513 ms, and keep looping
  - choreography: 3 elements (path) animate `stroke-dasharray` starting 1011–1011 ms after load together, each for about 21279 ms, and keep looping
  - script writes `stroke-dashoffset` on `figure.blog-figure.blog-figure--fit > div.bf-stage > svg > g:nth-of-type(3) > path` 81 times over 21404 ms (on load): from `32.7266` to `32.7266`
  - script writes `stroke-dashoffset` on `figure.blog-figure.blog-figure--fit > div.bf-stage > svg > g:nth-of-type(2) > path` 79 times over 21279 ms (on load): from `213.23` to `155.444`
  - script writes `stroke-dashoffset` on `figure.blog-figure.blog-figure--fit > div.bf-stage > svg > g:nth-of-type(1) > path` 78 times over 21191 ms (on load): from `32.7266` to `11.2252`
  - script writes `cy` on `figure.blog-figure.blog-figure--fit > div.bf-stage > svg > g:nth-of-type(1) > circle:nth-of-type(3)` 50 times over 20784 ms (on load): from `128.5666668846494` to ``
  - script writes `cy` on `figure.blog-figure.blog-figure--fit > div.bf-stage > svg > g:nth-of-type(1) > circle:nth-of-type(4)` 50 times over 20784 ms (on load): from `128.5666668846494` to ``
  - script writes `cy` on `figure.blog-figure.blog-figure--fit > div.bf-stage > svg > g:nth-of-type(3) > circle:nth-of-type(3)` 47 times over 14037 ms (on load): from `129.27380974179204` to ``
  - and 26 more recorded tracks (motion.json `recorded`)
  - scripts add `.bf-flash` to 6 elements as the page scrolls (first at scrollY 0)
- **Hover:** `.hover\:text-white:hover` changes color; `.group:hover .group-hover\:-translate-y-0\.5` changes transform; `.group:hover .group-hover\:translate-x-0\.5` changes transform; `.group:hover .group-hover\:text-white` changes color.

## 12 · section

- **Box:** 1440×260 px, starting 8320 px from the top. Background rgb(0, 0, 0), text rgb(255, 255, 255).
- **Layout:** flex row of 2, gap 8px, center/center.
- **Type:** Geist Sans 300 16px/24px · Geist Pixel Square 500 24px/32px · Geist Mono 400 11px/16.5px (family weight size/line-height, most text first).
- **Inside:** 1 heading, 1 paragraph, 1 link.
- **Look:** `reference/sections/12-section.jpg` and its anatomy `reference/sections/12-section.anatomy.jpg`.
- **Markup:** `reference/sections/12-section.html`.
- **Pictures:** `reference/assets/images/038-canvas.png` (1240×384).
- **Hover:** `.hover\:bg-white\/88:hover` changes background.

## 13 · footer

- **Box:** 1440×254 px, starting 8580 px from the top. Background rgb(0, 0, 0), text rgb(255, 255, 255).
- **Layout:** grid, 4 columns (310px 310px 310px 310px), gap normal.
- **Type:** Geist Mono 400 9px/13.5px · Geist Mono 400 10px/15px · Geist Mono 400 9px/20px · Geist Mono 400 11px/16.5px (family weight size/line-height, most text first).
- **Inside:** 3 headings, 1 paragraph, 16 links, 3 pictures, 16 drawings.
- **Look:** `reference/sections/13-footer.jpg` and its anatomy `reference/sections/13-footer.anatomy.jpg`.
- **Markup:** `reference/sections/13-footer.html`.
- **Drawings:** `reference/assets/svg/077-icon-footer.svg` (icon, 14×14), `reference/assets/svg/078-icon-footer.svg` (icon, 14×14, ×2), `reference/assets/svg/079-icon-footer.svg` (icon, 12×12, ×9), `reference/assets/svg/080-icon-footer.svg` (icon, 14×14), `reference/assets/svg/081-icon-footer.svg` (icon, 14×14), `reference/assets/svg/082-icon-footer.svg` (icon, 12×12), `reference/assets/svg/083-icon-footer.svg` (icon, 12×12).
- **Pictures:** `reference/assets/images/004-farming-labs-logo-dark-lwxtiiae.svg`, `reference/assets/images/005-github-qpyq9fjq.svg`, `reference/assets/images/038-canvas.png` (1240×384).
- **Hover:** `.hover\:bg-white\/\[0\.035\]:hover` changes background; `.hover\:text-white:hover` changes color; `.group:hover .group-hover\:translate-x-0\.5` changes transform; `.group:hover .group-hover\:text-white\/56` changes color; `.group:hover .group-hover\:text-white\/72` changes color.

## 14 · div

- **Box:** 1440×8805 px, starting 29 px from the top. Background rgb(0, 0, 0), text rgb(255, 255, 255).
- **Layout:** stacked blocks.
- **Look:** `reference/sections/14-div.jpg` and its anatomy `reference/sections/14-div.anatomy.jpg`.
- **Markup:** `reference/sections/14-div.html`.
