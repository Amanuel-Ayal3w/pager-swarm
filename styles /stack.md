# Stack

What the source site appears to be built with, read from its page: script and asset URLs, attributes and class patterns. It is evidence, not certainty. Treat "likely" entries as a guess.

**Never switch your project's framework or add these libraries just to match.** Recreate each effect with what your project already uses; reach for a library only when the user asks.

| | Built with | Evidence | Confidence |
|---|---|---|---|
| Framework | React | React fiber on DOM nodes | detected |
| Styling | Tailwind CSS | 1039 utility classes | detected |

## 3D and canvas

- The page draws into a canvas that takes 38% of the first screen.
- Its engine isn't identifiable from the page: it may be a 2D canvas, raw WebGL, or a library loaded as a module.
- The scene's main colours, most used first: #040404, #4d4d4d. Light, materials and background should land on these, so the page around it can share the same palette.
- Keep it light: cap devicePixelRatio at 2, render only while the canvas is on screen, show a still frame under prefers-reduced-motion, and a static image when WebGL isn't available.
