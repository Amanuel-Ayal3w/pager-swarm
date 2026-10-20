# How it moves, step by step

Every animation and behaviour found on the page, as recipes: what starts it, which element, which property from what to what, for how long, on which curve, in what order. Times are from the moment the trigger happens. Build them one at a time and check each against its film (frames captioned with their time, or with the scroll position).

Measured at 1440 px on farmjs.dev. Values in `code` are exactly as the browser reported them.

## The page's motion language

- **Curves:** `cubic-bezier(0.22, 1, 0.36, 1)` (41×), `ease` (5×), `steps(1)` (5×), `linear` (4×), `ease-out` (2×).
- **Durations:** 160 ms, 180 ms, 300 ms, 420 ms, 520 ms, 800 ms, 900 ms, 1000 ms, 9600 ms, 10800 ms, 12000 ms, 96000 ms.

## When the page scrolls

### 1. Classes and attributes the scroll switches

- `div.grid.duration-200 > ul.farm-tree-guide.min-h-0 > li.min-w-0 > button.relative.flex > svg` classes `+text-white/88 -text-white/46`, 915 ms after the scroll.
- `div.grid.duration-200 > ul.farm-tree-guide.min-h-0 > li.min-w-0 > button.relative.flex > span.ml-2.shrink-0:nth-of-type(3)` classes `+text-white/64 -text-white/28`, 915 ms after the scroll.
- `li.min-w-0:nth-of-type(3) > div.grid.duration-200 > ul.farm-tree-guide.min-h-0 > li.min-w-0 > button.relative.flex` `aria-current` `(unset)` → ``, 915 ms after the scroll.
- `li.min-w-0:nth-of-type(3) > div.grid.duration-200 > ul.farm-tree-guide.min-h-0 > li.min-w-0 > button.relative.flex` classes `+text-white/40 +hover:bg-white/[0.035] +hover:text-white/72 -bg-white/[0.055] -text-white/92`, 915 ms after the scroll.
- `li.min-w-0 > div.grid.duration-200 > ul.farm-tree-guide.min-h-0 > li.min-w-0 > button.relative.flex` `aria-current` `true` → `true`, 915 ms after the scroll.
- `li.min-w-0 > div.grid.duration-200 > ul.farm-tree-guide.min-h-0 > li.min-w-0 > button.relative.flex` classes `+bg-white/[0.055] +text-white/92 -text-white/40 -hover:bg-white/[0.035] -hover:text-white/72`, 915 ms after the scroll.
- `div.relative.z-10 > div.flex.min-w-0 > div.relative.flex:nth-of-type(2) > svg > path` `d` `M308,216H314Q320,216 320,210V46Q320,40 326,40H343` → `M308,216H314Q320,216 320,210V46Q320,40 326,40H343`, 915 ms after the scroll.
- `div.relative.z-10 > div.flex.min-w-0 > div.relative.flex:nth-of-type(2) > svg > circle` `cy` `216` → `216`, 915 ms after the scroll.
- **In the code:** `reference/scripts/03-farm-client-h6d37fabf.js` at character 7198 (`flex`: `on:t,label:n}){return(0,S.jsxs)('span',{className:'flex min-w-0 items-center gap-1.5 font-mono text-[10px] font-normal u`).

### 2. `section.farm-full-rule.farm-hero-rule > div.relative.z-10 > div.farm-hero-title.relative > div.farm-sw-layer > div.farm-sw-select` follows the scroll

- **What:** it changes `opacity`, `transform`, `height` as the page scrolls.
- `section.farm-full-rule.farm-hero-rule:nth-of-type(1) > div.relative.z-10:nth-of-type(1) > div.farm-hero-title.relative:nth-of-type(2) > div.farm-sw-layer > div.farm-sw-select` `opacity`: `0.926644` → `0.247124` over 4 frames, at rest 192 ms after the scroll.
- `section.farm-full-rule.farm-hero-rule:nth-of-type(1) > div.relative.z-10:nth-of-type(1) > div.farm-hero-title.relative:nth-of-type(2) > div.farm-sw-layer > div.farm-sw-select` `transform`: `translate3d(46.9812px, 78.1209px, 0px)` → `translate3d(391.771px, 128.996px, 0px)` over 4 frames, at rest 192 ms after the scroll.
- `section.farm-full-rule.farm-hero-rule:nth-of-type(1) > div.relative.z-10:nth-of-type(1) > div.farm-hero-title.relative:nth-of-type(2) > div.farm-sw-layer > div.farm-sw-select` `height`: `69.3766px` → `18.5019px` over 4 frames, at rest 192 ms after the scroll.
- **How:** derive the values above from the scroll position each frame (a scroll listener or requestAnimationFrame).
- **In the code:** `reference/scripts/03-farm-client-h6d37fabf.js` at character 34161 (`farm-sw-layer`: `,p]),(0,S.jsxs)('div',{"aria-hidden":!0,className:'farm-sw-layer',ref:m,children:[(0,S.jsxs)('div',{className:'farm-sw-s`); `reference/scripts/03-farm-client-h6d37fabf.js` at character 34221 (`farm-sw-select`: `ayer',ref:m,children:[(0,S.jsxs)('div',{className:'farm-sw-select',ref:h,children:[(0,S.jsx)('span',{className:'farm-sw-`).

### 3. `pre.min-h-0.max-w-full > code.farm-highlighted-code.block > span.sh__line.sh__line--highlighted > span.farm-renderer-value > span.farm-inline-typewriter` follows the scroll

- **What:** it changes `data-typewriter-phase` as the page scrolls.
- `pre.min-h-0.max-w-full > code.farm-highlighted-code.block > span.sh__line.sh__line--highlighted:nth-of-type(4) > span.farm-renderer-value:nth-of-type(3) > span.farm-inline-typewriter` `data-typewriter-phase`: `deleting` → `holding` over 3 frames, at rest 1608 ms after the scroll.
- **How:** derive the values above from the scroll position each frame (a scroll listener or requestAnimationFrame).

### 4. `div.relative > canvas`: a 1240×384 canvas, moved by time and scroll

- **What it draws:** canvas 2d.
- **In the markup:** `page.html` and `sections/` show it as a still picture (`img[data-livery-canvas]`). On the page it is a live <canvas> drawn every frame: build a canvas there, not an image.
- **Calls in one frame:** fillRect ×5934, clearRect ×1.
- **Scroll:** it redraws as the page scrolls and keeps moving for about 1463 ms after the scroll stops (eased).
- **Time:** it also moves on its own, every frame.

## Moving scenes (filmed)

### 5. Animated drawing

- **Film:** `reference/motion/films/02-drawing-section.jpg` (captions are ms).
- **Element:** `div.flex.min-w-0 > div.relative.flex:nth-of-type(2) > div.hidden.min-w-0 > div.farm-route-explorer.flex > svg` in section `08-section`.
- **In the code:** `reference/scripts/03-farm-client-h6d37fabf.js` at character 7198 (`flex`: `on:t,label:n}){return(0,S.jsxs)('span',{className:'flex min-w-0 items-center gap-1.5 font-mono text-[10px] font-normal u`).

### 6. Looping div: 83 moving parts (data-state, cx, stroke-dashoffset, cy)

- **Film:** `reference/motion/films/03-scripted-section.jpg` (captions are ms).
- **Element:** `article.group.flex:nth-of-type(8) > div.farm-feature-spotlight.relative:nth-of-type(2) > div.relative.z-10 > figure.blog-figure.blog-figure--fit > div.bf-stage` in section `08-section`.

### 7. Looping drawing: 62 moving parts (d, cy, points, cx)

- **Film:** `reference/motion/films/04-drawing-benchmarks.jpg` (captions are ms).
- **Element:** `section#benchmarks:nth-of-type(4) > div.grid.bg-black:nth-of-type(1) > article.flex.flex-col > div.benchmark-illustration.benchmark-hairline > svg` in section `06-benchmarks`.

### 8. Looping drawing: 17 moving parts (points, d, cx, cy)

- **Film:** `reference/motion/films/05-drawing-benchmarks.jpg` (captions are ms).
- **Element:** `div.grid.bg-black:nth-of-type(1) > div.border-t:nth-of-type(1) > article.flex.flex-col > div.benchmark-illustration.benchmark-hairline > svg` in section `06-benchmarks`.

### 9. The header `header.farm-full-rule` as you scroll

- **Behaviour:** it slides away when you scroll down.
- **In the code:** `reference/scripts/03-farm-client-h6d37fabf.js` at character 9229 (`farm-full-rule`: `ctivePage:e}){return(0,S.jsx)('header',{className:'farm-full-rule sticky top-0 z-50 bg-black/94 backdrop-blur-xl',childr`).

### 10. The phone menu (`button.inline-flex` at 390 px)

- **In order:**
  1. 112 ms: `aside#nd-sidebar-mobile` `data-state` set to `open`
  1. 112 ms: `aside#nd-sidebar-mobile` classes `-invisible`
- **Animations that ran:**
  - 125 ms: `div#nd-docs-layout > div.fixed.z-40` CSS animation `fd-fade-in` on `opacity`, 300 ms, `ease` (opacity: 0 → 1)
  - 125 ms: `aside#nd-sidebar-mobile` CSS animation `fd-pixel-sidebar-in` on `transform`, 180 ms, `ease-out` (transform: translate(-100%) → translate(0px))
- **Film:** `reference/motion/menu.jpg`.
- **In the code:** `reference/scripts/03-farm-client-h6d37fabf.js` at character 8842 (`inline-flex`: `js v0.1.0 is released'}),(0,S.jsx)('a',{className:'inline-flex min-h-7 shrink-0 items-center text-white/80 underline dec`).

## Hovering (what scripts do; CSS hover rules are in styles.css)

### 11. Hovering `div.farm-announcement.flex`

- **Text swap:** `pre#react-compiler-config > code.farm-highlighted-code.block > span.farm-code-typewriter.block:nth-of-type(2)` runs `compiler: true` → `compiler: tru` → `compiler: tr` → `compiler: t` → `compiler:` → `compiler: {` → `compiler: {      m` over 783 ms.
- **Text scramble:** `div.relative.flex:nth-of-type(2) > div.hidden.min-w-0 > div.farm-route-explorer.flex > svg > text:nth-of-type(1)` runs `/d▏` → `/da▏` → `/das▏` → `/dash▏` → `/dashb▏` → `/dashbo▏` → `/dashboa▏` → `/dashboar▏` → `/dashboard▏` over 262 ms.
- **Text scramble:** `div.farm-hero-title.relative:nth-of-type(2) > h1.max-w-full.font-medium > span.block.whitespace-nowrap:nth-of-type(2) > span.farm-hero-swap > span.farm-hero-swap-text` runs `1?0&+>=%>=>*` → `*?&1>!<1!&#!` → `<?0=?01/_!>!` → `#<!#>/>##>>=` → `!?%1>%#>+0&*0` → `…` → `product-inte<%>?` → `product-inte/<=+` → `product-integ%__` → `product-integ&>#` over 319 ms.
- 506 ms: `main > section.farm-full-rule.farm-hero-rule:nth-of-type(1) > div.relative.z-10:nth-of-type(1) > div.farm-hero-title.relative:nth-of-type(2) > a.farm-hero-tag` `data-sw-state` set to `off`
- 7 × 18967 ms: `div.farm-route-explorer.flex > svg > g > path` CSS animation `farm-route-draw` on `strokeDashoffset`, 520 ms, `cubic-bezier(0.22, 1, 0.36, 1)` (strokeDashoffset: 1px → 0px), each starting 70 ms after the one before
- 18968 ms: `div.flex.min-w-0 > div.relative.flex > svg > path` CSS animation `farm-route-draw` on `strokeDashoffset`, 420 ms, `cubic-bezier(0.22, 1, 0.36, 1)` (strokeDashoffset: 1px → 0px)
- 19328 ms: `div.flex.min-w-0 > div.relative.flex > svg > rect` CSS animation `farm-route-fade` on `opacity`, 160 ms after 360 ms, `ease-out` (opacity: 0 → 1)
- **Film:** `reference/motion/hovers/01-div-farm-announcement-fl.jpg`.
- **In the code:** `reference/scripts/03-farm-client-h6d37fabf.js` at character 35171 (`farm-hero-title`: `o,linkLabel:s}){return(0,S.jsxs)('div',{className:'farm-hero-title relative mt-3 w-fit max-w-full px-4 pb-4 pt-2 sm:px-5`); `reference/scripts/03-farm-client-h6d37fabf.js` at character 35677 (`farm-hero-tag`: `ull]})]}),(0,S.jsx)('a',{"aria-label":s,className:'farm-hero-tag',href:a,children:o}),(0,S.jsx)(Le,{heading:'h1',holdOnT`).

### 12. Hovering `a.inline-flex.min-h-7`

- **Text typewriter:** `pre#react-compiler-config > code.farm-highlighted-code.block > span.farm-code-typewriter.block:nth-of-type(2)` runs `compiler: {      mode: "annotation",      directive: "us` → `compiler: {      mode: "annotation",      directive: "use` → `compiler: {      mode: "annotation",      directive: "use c` → `compiler: {      mode: "annotation",      directive: "use co` → `compiler: {      mode: "annotation",      directive: "use com` → `…` → `compiler: {      mode: "annotation",      directive: "use compiler` → `compiler: {      mode: "annotation",      directive: "use compiler"` → `compiler: {      mode: "annotation",      directive: "use compiler",` → `compiler: {      mode: "annotation",      directive: "use compiler",    }` over 792 ms.
- **Text scramble:** `div.farm-hero-title.relative:nth-of-type(2) > h1.max-w-full.font-medium > span.block.whitespace-nowrap:nth-of-type(2) > span.farm-hero-swap > span.farm-hero-swap-text` runs `/&%_00=/+#_1#?!#1&` → `1#1*=+??/!#</11?#<` → `/*!=*=#+?%+&%_#<00` → `>_<_?!1+!11/+?&?=_` → `#>&!*1&0/&11=_&<0` → `1/!1_#>%#0+%_1__!` → `%</1#0+/%=_#&=!=*` → `<%<+&%<#/<#0?/*&&` → `&?=>#!%*?#/+!00>?` → `?#><?0%+?=>%+%=_>` over 70 ms.
- 4 ms: `section.farm-full-rule.farm-hero-rule:nth-of-type(1) > div.relative.z-10:nth-of-type(1) > div.farm-hero-title.relative:nth-of-type(2) > div.farm-sw-layer > div.farm-sw-select` `height` `0.110233px` → `74.8688px` (36 steps)
- 4 ms: `section.farm-full-rule.farm-hero-rule:nth-of-type(1) > div.relative.z-10:nth-of-type(1) > div.farm-hero-title.relative:nth-of-type(2) > div.farm-sw-layer > svg:nth-of-type(2)` `transform` `translate3d(7.50707px, 70.739px, 0px) scale(0.86)` → `translate3d(511.693px, 145.498px, 0px) scale(1)` (41 steps)
- 35 ms: `section.farm-full-rule.farm-hero-rule:nth-of-type(1) > div.relative.z-10:nth-of-type(1) > div.farm-hero-title.relative:nth-of-type(2) > div.farm-sw-layer > div.farm-sw-select` `data-corners` set to ``
- 3 × 21675 ms: `div.farm-route-explorer.flex > svg > g > path` CSS animation `farm-route-draw` on `strokeDashoffset`, 520 ms, `cubic-bezier(0.22, 1, 0.36, 1)` (strokeDashoffset: 1px → 0px), each starting 70 ms after the one before
- 21777 ms: `div.flex.min-w-0 > div.relative.flex > svg > path` CSS animation `farm-route-draw` on `strokeDashoffset`, 420 ms, `cubic-bezier(0.22, 1, 0.36, 1)` (strokeDashoffset: 1px → 0px)
- 4 × 21936 ms: `div.farm-route-explorer.flex > svg > g > text` CSS animation `farm-route-fade` on `opacity`, 260 ms after 180 ms, `ease-out` (opacity: 0 → 1), each starting 90 ms after the one before
- 22037 ms: `div.flex.min-w-0 > div.relative.flex > svg > rect` CSS animation `farm-route-fade` on `opacity`, 160 ms after 360 ms, `ease-out` (opacity: 0 → 1)
- **Film:** `reference/motion/hovers/02-a-inline-flex-min-h-7.jpg`.
- **In the code:** `reference/scripts/03-farm-client-h6d37fabf.js` at character 34161 (`farm-sw-layer`: `,p]),(0,S.jsxs)('div',{"aria-hidden":!0,className:'farm-sw-layer',ref:m,children:[(0,S.jsxs)('div',{className:'farm-sw-s`); `reference/scripts/03-farm-client-h6d37fabf.js` at character 34221 (`farm-sw-select`: `ayer',ref:m,children:[(0,S.jsxs)('div',{className:'farm-sw-select',ref:h,children:[(0,S.jsx)('span',{className:'farm-sw-`).

### 13. Hovering `div.relative.z-10`

- 4 ms: `section.farm-full-rule.farm-hero-rule:nth-of-type(1) > div.relative.z-10:nth-of-type(1) > div.farm-hero-title.relative:nth-of-type(2) > div.farm-sw-layer > svg:nth-of-type(2)` `transform` `translate3d(391.735px, 160.938px, 0px) scale(1)` → `translate3d(425.954px, 163.338px, 0px) scale(1)` (24 steps)
- 48 ms: `div.grid.duration-200 > ul.farm-tree-guide.min-h-0 > li.min-w-0:nth-of-type(1) > button.relative.flex > svg` classes `+text-white/46 -text-white/88`
- 48 ms: `div.grid.duration-200 > ul.farm-tree-guide.min-h-0 > li.min-w-0:nth-of-type(1) > button.relative.flex > span.ml-2.shrink-0:nth-of-type(3)` classes `+text-white/28 -text-white/64`
- 48 ms: `li.min-w-0 > div.grid.duration-200 > ul.farm-tree-guide.min-h-0 > li.min-w-0:nth-of-type(1) > button.relative.flex` `aria-current` set to ``
- 48 ms: `li.min-w-0 > div.grid.duration-200 > ul.farm-tree-guide.min-h-0 > li.min-w-0:nth-of-type(1) > button.relative.flex` classes `+text-white/40 +hover:bg-white/[0.035] +hover:text-white/72 -bg-white/[0.055] -text-white/92`
- 48 ms: `div.grid.duration-200 > ul.farm-tree-guide.min-h-0 > li.min-w-0:nth-of-type(2) > button.relative.flex > svg` classes `+text-white/88 -text-white/46`
- 24918 ms: `section.farm-full-rule.farm-hero-rule > div.relative.z-10 > div.farm-hero-title.relative > a.farm-hero-tag` CSS transition on `backgroundColor`, 200 ms, `linear` (backgroundColor: rgba(0, 0, 0, 0) → rgba(255, 255, 255, 0.14))
- 24918 ms: `section.farm-full-rule.farm-hero-rule > div.relative.z-10 > div.farm-hero-title.relative > a.farm-hero-tag` CSS transition on `borderBottomColor`, 200 ms, `linear` (borderBottomColor: rgba(255, 255, 255, 0.576) → rgb(255, 255, 255))
- 24918 ms: `section.farm-full-rule.farm-hero-rule > div.relative.z-10 > div.farm-hero-title.relative > a.farm-hero-tag` CSS transition on `borderLeftColor`, 200 ms, `linear` (borderLeftColor: rgba(255, 255, 255, 0.576) → rgb(255, 255, 255))
- 24918 ms: `section.farm-full-rule.farm-hero-rule > div.relative.z-10 > div.farm-hero-title.relative > a.farm-hero-tag` CSS transition on `borderRightColor`, 200 ms, `linear` (borderRightColor: rgba(255, 255, 255, 0.576) → rgb(255, 255, 255))
- 24919 ms: `section.farm-full-rule.farm-hero-rule > div.relative.z-10 > div.farm-hero-title.relative > a.farm-hero-tag` CSS transition on `borderTopColor`, 200 ms, `linear` (borderTopColor: rgba(255, 255, 255, 0.576) → rgb(255, 255, 255))
- 24985 ms: `div.grid.duration-200 > ul.farm-tree-guide.min-h-0 > li.min-w-0 > button.relative.flex` CSS transition on `backgroundColor`, 150 ms, `cubic-bezier(0.4, 0, 0.2, 1)` (backgroundColor: rgba(255, 255, 255, 0.055) → rgba(0, 0, 0, 0))
- 24985 ms: `div.grid.duration-200 > ul.farm-tree-guide.min-h-0 > li.min-w-0 > button.relative.flex` CSS transition on `backgroundColor`, 150 ms, `cubic-bezier(0.4, 0, 0.2, 1)` (backgroundColor: rgba(0, 0, 0, 0) → rgba(255, 255, 255, 0.055))
- 24985 ms: `div.grid.duration-200 > ul.farm-tree-guide.min-h-0 > li.min-w-0 > button.relative.flex` CSS transition on `color`, 150 ms, `cubic-bezier(0.4, 0, 0.2, 1)` (color: rgb(255, 255, 255) → rgba(255, 255, 255, 0.4))
- 24985 ms: `div.grid.duration-200 > ul.farm-tree-guide.min-h-0 > li.min-w-0 > button.relative.flex` CSS transition on `color`, 150 ms, `cubic-bezier(0.4, 0, 0.2, 1)` (color: rgba(255, 255, 255, 0.4) → rgb(255, 255, 255))
- 24985 ms: `div.farm-route-explorer.flex > svg > g > path` CSS transition on `stroke`, 200 ms, `linear` (stroke: rgba(255, 255, 255, 0.52) → rgba(255, 255, 255, 0.26))
- 24985 ms: `div.farm-route-explorer.flex > svg > g > path` CSS transition on `stroke`, 200 ms, `linear` (stroke: rgba(255, 255, 255, 0.28) → rgba(255, 255, 255, 0.14))
- 24989 ms: `div.farm-route-explorer.flex > svg > g > path` CSS animation `farm-route-draw` on `strokeDashoffset`, 520 ms, `cubic-bezier(0.22, 1, 0.36, 1)` (strokeDashoffset: 1px → 0px)
- **Film:** `reference/motion/hovers/03-div-relative-z-10.jpg`.
- **In the code:** `reference/scripts/03-farm-client-h6d37fabf.js` at character 34161 (`farm-sw-layer`: `,p]),(0,S.jsxs)('div',{"aria-hidden":!0,className:'farm-sw-layer',ref:m,children:[(0,S.jsxs)('div',{className:'farm-sw-s`).

### 14. Hovering `a.inline-flex.min-w-0`

- **Text typewriter:** `pre#react-compiler-config > code.farm-highlighted-code.block > span.farm-code-typewriter.block:nth-of-type(2)` runs `compiler: {      mode: "annotation",      directive: "us` → `compiler: {      mode: "annotation",      directive: "u` → `compiler: {      mode: "annotation",      directive: "` → `compiler: {      mode: "annotation",      directive:` → `compiler: {      mode: "annotation",      directive` → `…` → `compiler: {      mode: "annot` → `compiler: {      mode: "anno` → `compiler: {      mode: "ann` → `compiler: {      mode: "an` over 962 ms.
- **Text scramble:** `pre.min-h-0.max-w-full > code.farm-highlighted-code.block > span.sh__line.sh__line--highlighted:nth-of-type(4) > span.farm-renderer-value:nth-of-type(3) > span.farm-inline-typewriter` runs `vue()` → `vue(` → `vue` → `vu` → `v` → `…` → `sv` → `sve` → `svel` → `svelt` over 619 ms.
- 337 ms: `pre.min-h-0.max-w-full > code.farm-highlighted-code.block > span.sh__line.sh__line--highlighted:nth-of-type(4) > span.farm-renderer-value:nth-of-type(3) > span.farm-inline-typewriter` `data-typewriter-phase` `deleting` → `typing`
- 7 × 27560 ms: `div.farm-route-explorer.flex > svg > g > path` CSS animation `farm-route-draw` on `strokeDashoffset`, 520 ms, `cubic-bezier(0.22, 1, 0.36, 1)` (strokeDashoffset: 1px → 0px), each starting 70 ms after the one before
- 27661 ms: `div.flex.min-w-0 > div.relative.flex > svg > path` CSS animation `farm-route-draw` on `strokeDashoffset`, 420 ms, `cubic-bezier(0.22, 1, 0.36, 1)` (strokeDashoffset: 1px → 0px)
- 27921 ms: `div.flex.min-w-0 > div.relative.flex > svg > rect` CSS animation `farm-route-fade` on `opacity`, 160 ms after 360 ms, `ease-out` (opacity: 0 → 1)
- 27927 ms: `section.farm-full-rule.farm-hero-rule > div.relative.z-10 > div.mt-6.flex > a.inline-flex.min-w-0` CSS transition on `backgroundColor`, 150 ms, `cubic-bezier(0.4, 0, 0.2, 1)` (backgroundColor: rgb(255, 255, 255) → rgba(255, 255, 255, 0.88))

### 15. Hovering `button.group.relative`

- **Text scramble:** `pre#react-compiler-config > code.farm-highlighted-code.block > span.farm-code-typewriter.block:nth-of-type(2)` runs `compiler: {` → `compiler:` → `compiler: t` over 806 ms.
- **Text scramble:** `div.relative.flex:nth-of-type(2) > div.hidden.min-w-0 > div.farm-route-explorer.flex > svg > text:nth-of-type(1)` runs `/api▏` → `/api/▏` → `/api/u▏` → `/api/us▏` → `/api/use▏` → `/api/user▏` → `/api/users▏` over 316 ms.
- **Text scramble:** `div.farm-hero-title.relative:nth-of-type(2) > h1.max-w-full.font-medium > span.block.whitespace-nowrap:nth-of-type(2) > span.farm-hero-swap > span.farm-hero-swap-text` runs `>_&%#?!/&!%*` → `+<_%/_&&<_%*` → `#+<<_*1>!>&#` → `10>*=00<<+%+` → `=#%0+!?0/#/!` → `…` → `product-integrat1` → `product-integrat&` → `product-integrate` → `product-integrated` over 508 ms.
- 28 ms: `main > section.farm-full-rule.farm-hero-rule:nth-of-type(1) > div.relative.z-10:nth-of-type(1) > div.farm-hero-title.relative:nth-of-type(2) > a.farm-hero-tag` `data-sw-state` set to `off`
- 531 ms: `section.farm-full-rule.farm-hero-rule:nth-of-type(1) > div.relative.z-10:nth-of-type(1) > div.farm-hero-title.relative:nth-of-type(2) > div.farm-sw-layer > div.farm-sw-select` `opacity` `1` → `0.443707` (16 steps)
- 531 ms: `section.farm-full-rule.farm-hero-rule:nth-of-type(1) > div.relative.z-10:nth-of-type(1) > div.farm-hero-title.relative:nth-of-type(2) > div.farm-sw-layer > div.farm-sw-select` `transform` `translate3d(9.76px, 72.6287px, 0px)` → `translate3d(292.024px, 114.278px, 0px)` (16 steps)
- 531 ms: `section.farm-full-rule.farm-hero-rule:nth-of-type(1) > div.relative.z-10:nth-of-type(1) > div.farm-hero-title.relative:nth-of-type(2) > div.farm-sw-layer > div.farm-sw-select` `height` `74.8688px` → `33.2198px` (16 steps)
- 3 × 28983 ms: `div.farm-route-explorer.flex > svg > g > path` CSS animation `farm-route-draw` on `strokeDashoffset`, 520 ms, `cubic-bezier(0.22, 1, 0.36, 1)` (strokeDashoffset: 1px → 0px), each starting 70 ms after the one before
- 29146 ms: `section.farm-full-rule.farm-hero-rule > div.relative.z-10 > div.farm-hero-title.relative > a.farm-hero-tag` CSS transition on `backgroundColor`, 200 ms, `linear` (backgroundColor: rgb(255, 255, 255) → rgba(0, 0, 0, 0))
- 29146 ms: `section.farm-full-rule.farm-hero-rule > div.relative.z-10 > div.farm-hero-title.relative > a.farm-hero-tag` CSS transition on `borderBottomColor`, 200 ms, `linear` (borderBottomColor: rgb(255, 255, 255) → rgba(0, 0, 0, 0))
- 29146 ms: `section.farm-full-rule.farm-hero-rule > div.relative.z-10 > div.farm-hero-title.relative > a.farm-hero-tag` CSS transition on `borderLeftColor`, 200 ms, `linear` (borderLeftColor: rgb(255, 255, 255) → rgba(0, 0, 0, 0))
- 29146 ms: `section.farm-full-rule.farm-hero-rule > div.relative.z-10 > div.farm-hero-title.relative > a.farm-hero-tag` CSS transition on `borderRightColor`, 200 ms, `linear` (borderRightColor: rgb(255, 255, 255) → rgba(0, 0, 0, 0))
- 29146 ms: `section.farm-full-rule.farm-hero-rule > div.relative.z-10 > div.farm-hero-title.relative > a.farm-hero-tag` CSS transition on `borderTopColor`, 200 ms, `linear` (borderTopColor: rgb(255, 255, 255) → rgba(0, 0, 0, 0))
- 29146 ms: `section.farm-full-rule.farm-hero-rule > div.relative.z-10 > div.farm-hero-title.relative > a.farm-hero-tag` CSS transition on `color`, 200 ms, `linear` (color: rgb(0, 0, 0) → rgba(255, 255, 255, 0.5))
- 3 × 29164 ms: `div.farm-route-explorer.flex > svg > g > text` CSS animation `farm-route-fade` on `opacity`, 260 ms after 180 ms, `ease-out` (opacity: 0 → 1), each starting 90 ms after the one before
- **In the code:** `reference/scripts/03-farm-client-h6d37fabf.js` at character 35171 (`farm-hero-title`: `o,linkLabel:s}){return(0,S.jsxs)('div',{className:'farm-hero-title relative mt-3 w-fit max-w-full px-4 pb-4 pt-2 sm:px-5`); `reference/scripts/03-farm-client-h6d37fabf.js` at character 35677 (`farm-hero-tag`: `ull]})]}),(0,S.jsx)('a',{"aria-label":s,className:'farm-hero-tag',href:a,children:o}),(0,S.jsx)(Le,{heading:'h1',holdOnT`).

### 16. Hovering `div.grid.min-h-9`

- **Text scramble:** `pre.min-h-0.max-w-full > code.farm-highlighted-code.block > span.sh__line.sh__line--highlighted:nth-of-type(4) > span.farm-renderer-value:nth-of-type(3) > span.farm-inline-typewriter` runs `svelte()` → `svelte(` → `svelte` → `svelt` → `svel` → `…` → `s` → `​` → `p` → `pr` over 750 ms.
- 462 ms: `pre.min-h-0.max-w-full > code.farm-highlighted-code.block > span.sh__line.sh__line--highlighted:nth-of-type(4) > span.farm-renderer-value:nth-of-type(3) > span.farm-inline-typewriter` `data-typewriter-phase` `deleting` → `typing`
- 571 ms: `div.grid.duration-200 > ul.farm-tree-guide.min-h-0 > li.min-w-0:nth-of-type(1) > button.relative.flex > svg` classes `+text-white/88 -text-white/46`
- 571 ms: `div.grid.duration-200 > ul.farm-tree-guide.min-h-0 > li.min-w-0:nth-of-type(1) > button.relative.flex > span.ml-2.shrink-0:nth-of-type(3)` classes `+text-white/64 -text-white/28`
- 571 ms: `li.min-w-0 > div.grid.duration-200 > ul.farm-tree-guide.min-h-0 > li.min-w-0:nth-of-type(1) > button.relative.flex` `aria-current` set to `true`
- 571 ms: `li.min-w-0 > div.grid.duration-200 > ul.farm-tree-guide.min-h-0 > li.min-w-0:nth-of-type(1) > button.relative.flex` classes `+bg-white/[0.055] +text-white/92 -text-white/40 -hover:bg-white/[0.035] -hover:text-white/72`
- 571 ms: `div.grid.duration-200 > ul.farm-tree-guide.min-h-0 > li.min-w-0 > button.relative.flex > svg` classes `+text-white/46 -text-white/88`
- 3 × 30308 ms: `div.farm-route-explorer.flex > svg > g > path` CSS animation `farm-route-draw` on `strokeDashoffset`, 520 ms, `cubic-bezier(0.22, 1, 0.36, 1)` (strokeDashoffset: 1px → 0px), each starting 70 ms after the one before
- 30413 ms: `div.flex.min-w-0 > div.relative.flex > svg > path` CSS animation `farm-route-draw` on `strokeDashoffset`, 420 ms, `cubic-bezier(0.22, 1, 0.36, 1)` (strokeDashoffset: 1px → 0px)
- 4 × 30569 ms: `div.farm-route-explorer.flex > svg > g > text` CSS animation `farm-route-fade` on `opacity`, 260 ms after 180 ms, `ease-out` (opacity: 0 → 1), each starting 90 ms after the one before
- 30673 ms: `div.flex.min-w-0 > div.relative.flex > svg > rect` CSS animation `farm-route-fade` on `opacity`, 160 ms after 360 ms, `ease-out` (opacity: 0 → 1)

### 17. Hovering `code.flex.h-full`

- **Text scramble:** `div.farm-hero-title.relative:nth-of-type(2) > h1.max-w-full.font-medium > span.block.whitespace-nowrap:nth-of-type(2) > span.farm-hero-swap > span.farm-hero-swap-text` runs `?=><=0?*??!#&+*0=&` → `!<0%1=0*=_%<<0=0/=` → `=/?&>/*1#<=!+=/+>*` → `#&&0=<&1?&++=00*?0` → `&_0!#&%*!*=+#%+11` → `…` → `agent-nativ&+=` → `agent-native%` → `agent-native0` → `agent-native` over 354 ms.
- 5 ms: `section.farm-full-rule.farm-hero-rule:nth-of-type(1) > div.relative.z-10:nth-of-type(1) > div.farm-hero-title.relative:nth-of-type(2) > div.farm-sw-layer > div.farm-sw-select` `height` `45.3745px` → `74.8688px` (20 steps)
- 5 ms: `section.farm-full-rule.farm-hero-rule:nth-of-type(1) > div.relative.z-10:nth-of-type(1) > div.farm-hero-title.relative:nth-of-type(2) > div.farm-sw-layer > svg:nth-of-type(2)` `transform` `translate3d(314.273px, 116.003px, 0px) scale(0.86)` → `translate3d(363.209px, 145.498px, 0px) scale(1)` (40 steps)
- 3 × 31602 ms: `div.farm-route-explorer.flex > svg > g > path` CSS animation `farm-route-draw` on `strokeDashoffset`, 520 ms, `cubic-bezier(0.22, 1, 0.36, 1)` (strokeDashoffset: 1px → 0px), each starting 70 ms after the one before
- 31703 ms: `div.flex.min-w-0 > div.relative.flex > svg > path` CSS animation `farm-route-draw` on `strokeDashoffset`, 420 ms, `cubic-bezier(0.22, 1, 0.36, 1)` (strokeDashoffset: 1px → 0px)
- 31963 ms: `div.flex.min-w-0 > div.relative.flex > svg > rect` CSS animation `farm-route-fade` on `opacity`, 160 ms after 360 ms, `ease-out` (opacity: 0 → 1)
- **In the code:** `reference/scripts/03-farm-client-h6d37fabf.js` at character 34161 (`farm-sw-layer`: `,p]),(0,S.jsxs)('div',{"aria-hidden":!0,className:'farm-sw-layer',ref:m,children:[(0,S.jsxs)('div',{className:'farm-sw-s`); `reference/scripts/03-farm-client-h6d37fabf.js` at character 34221 (`farm-sw-select`: `ayer',ref:m,children:[(0,S.jsxs)('div',{className:'farm-sw-select',ref:h,children:[(0,S.jsx)('span',{className:'farm-sw-`).

### 18. Hovering `button.inline-flex.min-w-9`

- **Text scramble:** `pre.min-h-0.max-w-full > code.farm-highlighted-code.block > span.sh__line.sh__line--highlighted:nth-of-type(4) > span.farm-renderer-value:nth-of-type(3) > span.farm-inline-typewriter` runs `preact()` → `preact(` → `preact` → `preac` → `prea` → `pre` → `pr` → `p` → `​` over 162 ms.
- 8 ms: `section.farm-full-rule.farm-hero-rule:nth-of-type(1) > div.relative.z-10:nth-of-type(1) > div.farm-hero-title.relative:nth-of-type(2) > div.farm-sw-layer > svg:nth-of-type(2)` `transform` `translate3d(347.505px, 145.498px, 0px) scale(1)` → `translate3d(362.111px, 160.938px, 0px) scale(0.86)` (44 steps)
- 622 ms: `pre.min-h-0.max-w-full > code.farm-highlighted-code.block > span.sh__line.sh__line--highlighted:nth-of-type(4) > span.farm-renderer-value:nth-of-type(3) > span.farm-inline-typewriter` `data-typewriter-phase` set to `deleting`
- 5 × 32971 ms: `div.farm-route-explorer.flex > svg > g > path` CSS animation `farm-route-draw` on `strokeDashoffset`, 520 ms, `cubic-bezier(0.22, 1, 0.36, 1)` (strokeDashoffset: 1px → 0px), each starting 70 ms after the one before
- 32972 ms: `div.flex.min-w-0 > div.relative.flex > svg > path` CSS animation `farm-route-draw` on `strokeDashoffset`, 420 ms, `cubic-bezier(0.22, 1, 0.36, 1)` (strokeDashoffset: 1px → 0px)
- 33200 ms: `div#install-command-panel > button.inline-flex.min-w-9` CSS transition on `backgroundColor`, 150 ms, `cubic-bezier(0.4, 0, 0.2, 1)` (backgroundColor: rgba(255, 255, 255, 0.024) → rgba(255, 255, 255, 0.075))
- 33200 ms: `div#install-command-panel > button.inline-flex.min-w-9` CSS transition on `color`, 150 ms, `cubic-bezier(0.4, 0, 0.2, 1)` (color: rgba(255, 255, 255, 0.48) → rgb(255, 255, 255))
- 33332 ms: `div.flex.min-w-0 > div.relative.flex > svg > rect` CSS animation `farm-route-fade` on `opacity`, 160 ms after 360 ms, `ease-out` (opacity: 0 → 1)
- **In the code:** `reference/scripts/03-farm-client-h6d37fabf.js` at character 34161 (`farm-sw-layer`: `,p]),(0,S.jsxs)('div',{"aria-hidden":!0,className:'farm-sw-layer',ref:m,children:[(0,S.jsxs)('div',{className:'farm-sw-s`).

### 19. Hovering `div.flex.min-w-0`

- **Text typewriter:** `pre.min-h-0.max-w-full > code.farm-highlighted-code.block > span.sh__line.sh__line--highlighted:nth-of-type(4) > span.farm-renderer-value:nth-of-type(3) > span.farm-inline-typewriter` runs `solid` → `solid(` → `solid()` → `solid(),` over 75 ms.
- **Text scramble:** `pre#react-compiler-config > code.farm-highlighted-code.block > span.farm-code-typewriter.block:nth-of-type(2)` runs `compiler: true,` → `compiler: true` → `compiler: tru` → `compiler: tr` → `compiler: t` → `compiler:` → `compiler: {` → `compiler: {      m` → `compiler: {      mo` over 718 ms.
- **Text scramble:** `div.relative.flex:nth-of-type(2) > div.hidden.min-w-0 > div.farm-route-explorer.flex > svg > text:nth-of-type(1)` runs `▏` → `/▏` → `/d▏` → `/da▏` → `/das▏` over 128 ms.
- 5 ms: `section.farm-full-rule.farm-hero-rule:nth-of-type(1) > div.relative.z-10:nth-of-type(1) > div.farm-hero-title.relative:nth-of-type(2) > div.farm-sw-layer > svg:nth-of-type(2)` `transform` `translate3d(391.095px, 160.938px, 0px) scale(0.86)` → `translate3d(425.954px, 163.338px, 0px) scale(1)` (32 steps)
- 89 ms: `pre.min-h-0.max-w-full > code.farm-highlighted-code.block > span.sh__line.sh__line--highlighted:nth-of-type(4) > span.farm-renderer-value:nth-of-type(3) > span.farm-inline-typewriter` `data-typewriter-phase` set to `holding`
- 105 ms: `main > section.farm-full-rule.farm-hero-rule:nth-of-type(1) > div.relative.z-10:nth-of-type(1) > div.farm-hero-title.relative:nth-of-type(2) > a.farm-hero-tag` `data-sw-state` `linked` → `on` (4 steps)
- 670 ms: `section.farm-full-rule.farm-hero-rule:nth-of-type(1) > div.relative.z-10:nth-of-type(1) > div.farm-hero-title.relative:nth-of-type(2) > div.farm-sw-layer > span.farm-sw-ripple:nth-of-type(1)` `opacity` `0` → `0.5193` (11 steps)
- 670 ms: `section.farm-full-rule.farm-hero-rule:nth-of-type(1) > div.relative.z-10:nth-of-type(1) > div.farm-hero-title.relative:nth-of-type(2) > div.farm-sw-layer > span.farm-sw-ripple:nth-of-type(1)` `transform` `translate3d(428.954px, 165.338px, 0px) scale(2.8)` → `translate3d(428.954px, 165.338px, 0px) scale(0.378901)` (11 steps)
- 684 ms: `div.grid.duration-200 > ul.farm-tree-guide.min-h-0 > li.min-w-0:nth-of-type(2) > button.relative.flex > svg` classes `+text-white/46 -text-white/88`
- 5 × 33903 ms: `div.farm-route-explorer.flex > svg > g > path` CSS animation `farm-route-draw` on `strokeDashoffset`, 520 ms, `cubic-bezier(0.22, 1, 0.36, 1)` (strokeDashoffset: 1px → 0px), each starting 70 ms after the one before
- 34003 ms: `div.flex.min-w-0 > div.relative.flex > svg > path` CSS animation `farm-route-draw` on `strokeDashoffset`, 420 ms, `cubic-bezier(0.22, 1, 0.36, 1)` (strokeDashoffset: 1px → 0px)
- 34263 ms: `div.flex.min-w-0 > div.relative.flex > svg > rect` CSS animation `farm-route-fade` on `opacity`, 160 ms after 360 ms, `ease-out` (opacity: 0 → 1)
- 34386 ms: `section.farm-full-rule.farm-hero-rule > div.relative.z-10 > div.farm-hero-title.relative > a.farm-hero-tag` CSS transition on `borderBottomColor`, 200 ms, `linear` (borderBottomColor: rgba(255, 255, 255, 0.34) → rgba(255, 255, 255, 0.6))
- 34386 ms: `section.farm-full-rule.farm-hero-rule > div.relative.z-10 > div.farm-hero-title.relative > a.farm-hero-tag` CSS transition on `borderLeftColor`, 200 ms, `linear` (borderLeftColor: rgba(255, 255, 255, 0.34) → rgba(255, 255, 255, 0.6))
- 34386 ms: `section.farm-full-rule.farm-hero-rule > div.relative.z-10 > div.farm-hero-title.relative > a.farm-hero-tag` CSS transition on `borderRightColor`, 200 ms, `linear` (borderRightColor: rgba(255, 255, 255, 0.34) → rgba(255, 255, 255, 0.6))
- 34386 ms: `section.farm-full-rule.farm-hero-rule > div.relative.z-10 > div.farm-hero-title.relative > a.farm-hero-tag` CSS transition on `borderTopColor`, 200 ms, `linear` (borderTopColor: rgba(255, 255, 255, 0.34) → rgba(255, 255, 255, 0.6))
- 34386 ms: `section.farm-full-rule.farm-hero-rule > div.relative.z-10 > div.farm-hero-title.relative > a.farm-hero-tag` CSS transition on `color`, 200 ms, `linear` (color: rgba(255, 255, 255, 0.5) → rgb(255, 255, 255))
- **In the code:** `reference/scripts/03-farm-client-h6d37fabf.js` at character 34161 (`farm-sw-layer`: `,p]),(0,S.jsxs)('div',{"aria-hidden":!0,className:'farm-sw-layer',ref:m,children:[(0,S.jsxs)('div',{className:'farm-sw-s`).

### 20. Hovering `a.flex.h-16`

- **Text typewriter:** `pre#react-compiler-config > code.farm-highlighted-code.block > span.farm-code-typewriter.block:nth-of-type(2)` runs `compiler: {      mode: "ann` → `compiler: {      mode: "anno` → `compiler: {      mode: "annot` → `compiler: {      mode: "annota` → `compiler: {      mode: "annotat` → `…` → `compiler: {      mode: "annotation",      d` → `compiler: {      mode: "annotation",      di` → `compiler: {      mode: "annotation",      dir` → `compiler: {      mode: "annotation",      dire` over 806 ms.
- **Text typewriter:** `pre.min-h-0.max-w-full > code.farm-highlighted-code.block > span.sh__line.sh__line--highlighted:nth-of-type(4) > span.farm-renderer-value:nth-of-type(3) > span.farm-inline-typewriter` runs `solid()` → `solid(` → `solid` → `soli` → `sol` over 69 ms.
- 5 ms: `section.farm-full-rule.farm-hero-rule:nth-of-type(1) > div.relative.z-10:nth-of-type(1) > div.farm-hero-title.relative:nth-of-type(2) > div.farm-sw-layer > span.farm-sw-ripple:nth-of-type(1)` `opacity` `0.2193` → `0` (14 steps)
- 5 ms: `section.farm-full-rule.farm-hero-rule:nth-of-type(1) > div.relative.z-10:nth-of-type(1) > div.farm-hero-title.relative:nth-of-type(2) > div.farm-sw-layer > span.farm-sw-ripple:nth-of-type(1)` `transform` `translate3d(428.954px, 165.338px, 0px) scale(2.48022)` → `translate3d(428.954px, 165.338px, 0px) scale(2.8)` (13 steps)
- 5 ms: `section.farm-full-rule.farm-hero-rule:nth-of-type(1) > div.relative.z-10:nth-of-type(1) > div.farm-hero-title.relative:nth-of-type(2) > div.farm-sw-layer > span.farm-sw-ripple:nth-of-type(2)` `opacity` `0.3393` → `0` (21 steps)
- 5 ms: `section.farm-full-rule.farm-hero-rule:nth-of-type(1) > div.relative.z-10:nth-of-type(1) > div.farm-hero-title.relative:nth-of-type(2) > div.farm-sw-layer > span.farm-sw-ripple:nth-of-type(2)` `transform` `translate3d(428.954px, 165.338px, 0px) scale(1.61562)` → `translate3d(428.954px, 165.338px, 0px) scale(2.79999)` (20 steps)
- 194 ms: `section.farm-full-rule.farm-hero-rule:nth-of-type(1) > div.relative.z-10:nth-of-type(1) > div.farm-hero-title.relative:nth-of-type(2) > div.farm-sw-layer > svg:nth-of-type(2)` `opacity` `1` → `0` (28 steps)
- 194 ms: `section.farm-full-rule.farm-hero-rule:nth-of-type(1) > div.relative.z-10:nth-of-type(1) > div.farm-hero-title.relative:nth-of-type(2) > div.farm-sw-layer > svg:nth-of-type(2)` `transform` `translate3d(425.954px, 163.338px, 0px) scale(1)` → `translate3d(435.953px, 173.337px, 0px) scale(1)` (27 steps)
- 7 × 35053 ms: `div.farm-route-explorer.flex > svg > g > path` CSS animation `farm-route-draw` on `strokeDashoffset`, 520 ms, `cubic-bezier(0.22, 1, 0.36, 1)` (strokeDashoffset: 1px → 0px), each starting 70 ms after the one before
- 35154 ms: `div.flex.min-w-0 > div.relative.flex > svg > path` CSS animation `farm-route-draw` on `strokeDashoffset`, 420 ms, `cubic-bezier(0.22, 1, 0.36, 1)` (strokeDashoffset: 1px → 0px)
- 35415 ms: `div.flex.min-w-0 > div.relative.flex > svg > rect` CSS animation `farm-route-fade` on `opacity`, 160 ms after 360 ms, `ease-out` (opacity: 0 → 1)
- **In the code:** `reference/scripts/03-farm-client-h6d37fabf.js` at character 34161 (`farm-sw-layer`: `,p]),(0,S.jsxs)('div',{"aria-hidden":!0,className:'farm-sw-layer',ref:m,children:[(0,S.jsxs)('div',{className:'farm-sw-s`); `reference/scripts/03-farm-client-h6d37fabf.js` at character 34769 (`farm-sw-ripple`: `end',r:'3',ref:y})]}),(0,S.jsx)('span',{className:'farm-sw-ripple',ref:b}),(0,S.jsx)('span',{className:'farm-sw-ripple',`).

## Text that changes in place

### 21. `pre.min-h-0.max-w-full > code.farm-highlighted-code.block > span.sh__line.sh__line--highlighted:nth-of-type(4) > span.farm-renderer-value:nth-of-type(3) > span.farm-inline-typewriter`: a typewriter, on its own

- **Sequence:** `prea` → `preac` → `preact` → `preact(` → `preact()` → `preact(),` (156 ms).
- **How:** add one character at a time.

### 22. `div.relative.flex:nth-of-type(2) > div.hidden.min-w-0 > div.farm-route-explorer.flex > svg > text:nth-of-type(1)`: a scramble, on its own

- **Sequence:** `▏` → `/▏` → `/d▏` → `/da▏` → `/das▏` → `…` → `/dashbo▏` → `/dashboa▏` → `/dashboar▏` → `/dashboard▏` (325 ms).
- **How:** each frame, show the final text with the not-yet-settled letters replaced by random characters, settling one more letter every few frames from left to right.

### 23. `div.farm-hero-title.relative:nth-of-type(2) > h1.max-w-full.font-medium > span.block.whitespace-nowrap:nth-of-type(2) > span.farm-hero-swap > span.farm-hero-swap-text`: a scramble, on its own

- **Sequence:** `&>!#1>#&__/+` → `%=*10+0#=+*!` → `?/<_=0/1!??_` → `!=+%=??#&=!!<` → `0&+1*+1&0*=+_` → `…` → `product-integrat*` → `product-integrat&` → `product-integrat_` → `product-integrated` (436 ms).
- **How:** each frame, show the final text with the not-yet-settled letters replaced by random characters, settling one more letter every few frames from left to right.
- **In the code:** `reference/scripts/03-farm-client-h6d37fabf.js` at character 35501 (`farm-hero-swap`: `ace-nowrap',children:[(0,S.jsx)('span',{className:'farm-hero-swap',children:(0,S.jsx)('span',{className:'farm-hero-swap-`); `reference/scripts/03-farm-client-h6d37fabf.js` at character 35555 (`farm-hero-swap-text`: `m-hero-swap',children:(0,S.jsx)('span',{className:'farm-hero-swap-text',dangerouslySetInnerHTML:{__html:n}})}),i?' ${i}'`).

### 24. `pre#react-compiler-config > code.farm-highlighted-code.block > span.farm-code-typewriter.block:nth-of-type(2)`: a typewriter, while scrolling

- **Sequence:** `compiler: {      mode: "annotation",      directive: "use compiler",    },` → `compiler: {      mode: "annotation",      directive: "use compiler",    }` → `compiler: {      mode: "annotation",      directive: "use compiler",` → `compiler: {      mode: "annotation",      directive: "use compiler"` → `compiler: {      mode: "annotation",      directive: "use compiler` → `…` → `compiler: {      mode` → `compiler: {      mod` → `compiler: {      mo` → `compiler: {      m` (1795 ms).
- **How:** add one character at a time.
- **In the code:** `reference/scripts/03-farm-client-h6d37fabf.js` at character 35383 (`block`: `className:e,children:[(0,S.jsx)('span',{className:'block',children:t}),' ',(0,S.jsxs)('span',{className:'block whitespac`).

### 25. `pre.min-h-0.max-w-full > code.farm-highlighted-code.block > span.sh__line.sh__line--highlighted:nth-of-type(4) > span.farm-renderer-value:nth-of-type(3) > span.farm-inline-typewriter`: a scramble, while scrolling

- **Sequence:** `preact()` → `preact(` → `preact` → `preac` → `prea` → `…` → `solid` → `solid(` → `solid()` → `solid(),` (991 ms).
- **How:** each frame, show the final text with the not-yet-settled letters replaced by random characters, settling one more letter every few frames from left to right.

## Following the pointer

### 26. `section.farm-full-rule.farm-hero-rule:nth-of-type(1) > div.relative.z-10:nth-of-type(1) > div.farm-hero-title.relative:nth-of-type(2) > div.farm-sw-layer > svg:nth-of-type(2)` answers to the pointer

- `opacity` `3.14611e-06` → `0` over 8 frames.
- **In the code:** `reference/scripts/03-farm-client-h6d37fabf.js` at character 34161 (`farm-sw-layer`: `,p]),(0,S.jsxs)('div',{"aria-hidden":!0,className:'farm-sw-layer',ref:m,children:[(0,S.jsxs)('div',{className:'farm-sw-s`).

### 27. `section.farm-full-rule.farm-hero-rule:nth-of-type(1) > div.relative.z-10:nth-of-type(1) > div.farm-hero-title.relative:nth-of-type(2) > div.farm-sw-layer > svg:nth-of-type(2)` answers to the pointer

- `transform` `translate3d(-27.2399px, 44.6288px, 0px) scale(1)` → `translate3d(-25.5009px, 45.9587px, 0px) scale(1)` over 7 frames, easing 0.123 a frame.
- **In the code:** `reference/scripts/03-farm-client-h6d37fabf.js` at character 34161 (`farm-sw-layer`: `,p]),(0,S.jsxs)('div',{"aria-hidden":!0,className:'farm-sw-layer',ref:m,children:[(0,S.jsxs)('div',{className:'farm-sw-s`).

### 28. `pre.min-h-0.max-w-full > code.farm-highlighted-code.block > span.sh__line.sh__line--highlighted:nth-of-type(4) > span.farm-renderer-value:nth-of-type(3) > span.farm-inline-typewriter` answers to the pointer

- `data-typewriter-phase` `deleting` → `holding` over 3 frames.

### 29. `section.farm-full-rule.farm-hero-rule:nth-of-type(1) > div.relative.z-10:nth-of-type(1) > div.farm-hero-title.relative:nth-of-type(2) > div.farm-sw-layer > div.farm-sw-select` answers to the pointer

- `opacity` `0` → `1` over 1 frames.
- **In the code:** `reference/scripts/03-farm-client-h6d37fabf.js` at character 34161 (`farm-sw-layer`: `,p]),(0,S.jsxs)('div',{"aria-hidden":!0,className:'farm-sw-layer',ref:m,children:[(0,S.jsxs)('div',{className:'farm-sw-s`); `reference/scripts/03-farm-client-h6d37fabf.js` at character 34221 (`farm-sw-select`: `ayer',ref:m,children:[(0,S.jsxs)('div',{className:'farm-sw-select',ref:h,children:[(0,S.jsx)('span',{className:'farm-sw-`).

### 30. `section.farm-full-rule.farm-hero-rule:nth-of-type(1) > div.relative.z-10:nth-of-type(1) > div.farm-hero-title.relative:nth-of-type(2) > div.farm-sw-layer > div.farm-sw-select` answers to the pointer

- `transform` `translate3d(517.148px, 147.495px, 0px)` → `translate3d(9.76px, 72.6287px, 0px)` over 1 frames.
- **In the code:** `reference/scripts/03-farm-client-h6d37fabf.js` at character 34161 (`farm-sw-layer`: `,p]),(0,S.jsxs)('div',{"aria-hidden":!0,className:'farm-sw-layer',ref:m,children:[(0,S.jsxs)('div',{className:'farm-sw-s`); `reference/scripts/03-farm-client-h6d37fabf.js` at character 34221 (`farm-sw-select`: `ayer',ref:m,children:[(0,S.jsxs)('div',{className:'farm-sw-select',ref:h,children:[(0,S.jsx)('span',{className:'farm-sw-`).

### 31. `section.farm-full-rule.farm-hero-rule:nth-of-type(1) > div.relative.z-10:nth-of-type(1) > div.farm-hero-title.relative:nth-of-type(2) > div.farm-sw-layer > div.farm-sw-select` answers to the pointer

- `height` `0.0020645px` → `74.8688px` over 1 frames.
- **In the code:** `reference/scripts/03-farm-client-h6d37fabf.js` at character 34161 (`farm-sw-layer`: `,p]),(0,S.jsxs)('div',{"aria-hidden":!0,className:'farm-sw-layer',ref:m,children:[(0,S.jsxs)('div',{className:'farm-sw-s`); `reference/scripts/03-farm-client-h6d37fabf.js` at character 34221 (`farm-sw-select`: `ayer',ref:m,children:[(0,S.jsxs)('div',{className:'farm-sw-select',ref:h,children:[(0,S.jsx)('span',{className:'farm-sw-`).

## CSS animations (rules and @keyframes in styles.css)

- `main > section.farm-full-rule.w-full:nth-of-type(2) > div.grid.h-16 > div.farm-logo-viewport.min-w-0:nth-of-type(2) > div.farm-logo-rail.flex`: `farm-logo-rail` 96s `linear` infinite.
- `pre.min-h-0.flex-1 > code.block.min-w-0 > span.block.min-w-max > span.block.h-5:nth-of-type(1) > span.farm-terminal-command-text.inline-block:nth-of-type(2)`: `farm-terminal-command-type` 9.6s `ease` infinite.
- `pre.min-h-0.flex-1 > code.block.min-w-0 > span.block.min-w-max > span.block.h-5:nth-of-type(1) > span.farm-terminal-command-cursor.inline-block:nth-of-type(3)`: `farm-terminal-cursor-window` 9.6s `linear` infinite.
- `pre.min-h-0.flex-1 > code.block.min-w-0 > span.block.min-w-max > span.block.h-5:nth-of-type(1) > span.farm-terminal-command-cursor.inline-block:nth-of-type(3)::before`: `farm-terminal-cursor-blink` 0.8s `steps(1)` infinite.
- `figure.relative.z-10 > pre.min-h-0.flex-1 > code.block.min-w-0 > span.block.min-w-max > span.farm-terminal-output.block:nth-of-type(2)`: `farm-terminal-output` 9.6s `ease` infinite.
- `figure.relative.z-10 > pre.min-h-0.flex-1 > code.block.min-w-0 > span.block.h-5:nth-of-type(1) > span.farm-build-command-text.inline-block:nth-of-type(2)`: `farm-build-command-type` 10.8s `ease` infinite.
- `figure.relative.z-10 > pre.min-h-0.flex-1 > code.block.min-w-0 > span.block.h-5:nth-of-type(1) > span.farm-build-command-cursor.inline-block:nth-of-type(3)`: `farm-build-cursor-window` 10.8s `linear` infinite.
- `figure.relative.z-10 > pre.min-h-0.flex-1 > code.block.min-w-0 > span.block.h-5:nth-of-type(1) > span.farm-build-command-cursor.inline-block:nth-of-type(3)::before`: `farm-terminal-cursor-blink` 0.8s `steps(1)` infinite.
- `div.farm-feature-spotlight.relative:nth-of-type(2) > figure.relative.z-10 > pre.min-h-0.flex-1 > code.block.min-w-0 > span.farm-build-output.mt-2:nth-of-type(2)`: `farm-build-output` 10.8s `ease` infinite.
- `pre.min-h-0.max-w-full > code.farm-highlighted-code.block > span.sh__line.sh__line--highlighted:nth-of-type(4) > span.farm-renderer-value:nth-of-type(3) > span.farm-inline-typewriter::after`: `farm-terminal-cursor-blink` 0.8s `steps(1)` infinite.
- `figure.min-w-0.max-w-full > pre#react-compiler-config > code.farm-highlighted-code.block > span.farm-code-typewriter.block:nth-of-type(2) > span.sh__line.sh__line--highlighted:nth-of-type(2)::after`: `farm-terminal-cursor-blink` 0.8s `steps(1)` infinite.
- `article.flex.flex-col > h3.mt-4.max-w-xl > span.mt-1.grid:nth-of-type(3) > span.benchmark-comparison-rotator.block:nth-of-type(1) > span.benchmark-comparison-item.block:nth-of-type(1)`: `benchmark-comparison-cycle` 12s `cubic-bezier(0.22, 1, 0.36, 1)` infinite, delay -0.48s.

## The page's own code

The scripts the page ran are in `reference/scripts/` (3 files), so you can read exactly how each effect is made. Don't paste them in whole: rebuild each effect in the project's own code, following the recipe and the source together.

Not tried: navigation: cdpSession.send: Protocol error (Page.captureScreenshot): Not attached to an active page.
