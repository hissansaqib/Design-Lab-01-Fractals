"""
=====================================================================
  INTERACTIVE FRACTAL MANDALA  (v2 — redesigned)
  Design Lab 01: Designing Using Fractals
=====================================================================

MATH BEHIND THIS FRACTAL
-------------------------
The generative core is still a classic RECURSIVE binary branching
fractal: draw_branch() draws one segment, then calls ITSELF twice from
the segment's tip -- once rotated left, once rotated right, each
shorter by a fixed `ratio`. That single rule, applied recursively, is
what produces SELF-SIMILARITY: any sub-branch is a smaller copy of the
whole structure.

For a branch at (x1, y1), length L, angle theta:
    x2 = x1 + L * cos(theta)
    y2 = y1 - L * sin(theta)
Children spawn from (x2, y2) with length L*ratio and angles
theta +- branch_angle. `ratio` < 1 makes total branch length converge
(geometric series) -- the ITERATION component layered on the recursion.

WHAT'S NEW IN v2 (the redesign)
---------------------------------
The v1 submission was a single ground-based tree with a soft navy
background -- functional, but visually plain. v2 keeps the exact same
recursive math and turns it into a **fractal mandala**: the recursive
branch function is called `n_arms` times around a common center, each
copy rotated by 360/n_arms degrees. Because every arm is the identical
recursive structure, the whole composition stays mathematically
grounded in recursion + self-similarity, but now reads as a bold,
symmetric, poster-like graphic -- the kind of composition that would
actually work printed on a t-shirt.

Other design upgrades:
  1. RADIAL SYMMETRY (mandala)   - n_arms copies of the recursive tree,
     evenly rotated around a center point.
  2. CURATED COLOR PALETTES      - four hand-picked 3-stop gradients
     (Sunset Bloom / Electric Dream / Toxic Bloom / Solar Flare) that
     interpolate only through *adjacent* hues, so there's no muddy
     brown/grey "in-between" the way naive hue-cycling produces.
  3. BOLD OUTLINED / STICKER LOOK - every branch gets a dark outline
     drawn first, then the colored line on top, like screen-printed
     vector art.
  4. FLAT / POSTER COLOR MODE    - press F to snap the smooth gradient
     into a handful of discrete color bands -- a bolder, more
     print-friendly look, toggle-able live.
  5. SLOW HYPNOTIC ROTATION + BREATHING PULSE -  the whole mandala
     continuously rotates and gently scales in/out (sine-driven).
  6. LIVE MOUSE INTERACTIVITY    - mouse X changes the number of arms
     (petals), mouse Y changes recursion depth.
  7. HIGH-CONTRAST BLACK BACKGROUND - maximizes color pop and mirrors
     how the design would actually look printed on dark apparel.

CONTROLS
--------
  Mouse X       -> number of arms / petals (3-9)
  Mouse Y       -> recursion depth (more/fewer self-similar generations)
  Left click    -> cycle palette (Sunset Bloom / Electric Dream /
                   Toxic Bloom / Solar Flare)
  Right click   -> toggle glow on/off
  LEFT / RIGHT  -> decrease / increase branch spread angle
  UP / DOWN     -> increase / decrease branch length ratio
  F             -> toggle flat poster-color mode vs smooth gradient
  SPACE         -> pause / resume rotation + breathing animation
  H             -> show / hide HUD
  ESC / close   -> quit

INSTALL & RUN
--------------
    pip install pygame
    python fractal_mandala.py
=====================================================================
"""

import sys
import math
import pygame

# ---------------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------------
WIDTH, HEIGHT = 900, 900          # square canvas -> reads well as a print/logo
BG_COLOR = (8, 8, 10)              # near-black, maximizes color contrast
OUTLINE_COLOR = (10, 10, 12)
FPS = 60

MIN_ARMS, MAX_ARMS = 3, 9
MIN_DEPTH, MAX_DEPTH = 6, 10
MIN_SPREAD, MAX_SPREAD = 12, 40
MIN_RATIO, MAX_RATIO = 0.58, 0.80

TRUNK_LENGTH = 130
ROTATION_SPEED = 0.12      # radians/sec of slow continuous spin
BREATH_SPEED = 0.9
BREATH_AMOUNT = 0.06       # +/- fraction of scale from breathing

# ---------------------------------------------------------------
# CURATED PALETTES: 3 color stops each. index0 = trunk, index2 = tip.
# Interpolating only through neighboring hues (pink->orange->yellow,
# navy->violet->cyan, etc.) keeps every in-between shade vivid instead
# of drifting into muddy brown/grey.
# ---------------------------------------------------------------
PALETTES = {
    "Sunset Bloom":   [(255, 32, 110), (255, 140, 66), (255, 214, 90)],
    "Electric Dream": [(15, 20, 60), (123, 47, 247), (0, 229, 255)],
    "Toxic Bloom":    [(9, 12, 41), (0, 214, 150), (198, 255, 92)],
    "Solar Flare":    [(60, 0, 20), (255, 76, 0), (255, 226, 110)],
}
PALETTE_NAMES = list(PALETTES.keys())


def lerp_color(a, b, f):
    return (int(a[0] + (b[0] - a[0]) * f),
            int(a[1] + (b[1] - a[1]) * f),
            int(a[2] + (b[2] - a[2]) * f))


def gradient_color(t, anchors, flat_bands):
    """t in [0,1]: 0 = trunk, 1 = tip. If flat_bands > 0, quantize into
    that many discrete steps for a bold flat/poster look."""
    if flat_bands:
        step = 1.0 / max(1, flat_bands - 1)
        t = round(t / step) * step
        t = min(1.0, max(0.0, t))
    if t <= 0.5:
        return lerp_color(anchors[0], anchors[1], t * 2)
    return lerp_color(anchors[1], anchors[2], (t - 0.5) * 2)


# ---------------------------------------------------------------
# RECURSIVE FRACTAL DRAWING
# ---------------------------------------------------------------
def draw_branch(surface, x1, y1, length, angle, depth, max_depth,
                 branch_angle, ratio, anchors, flat_bands, outline, glow_surface):
    """
    Recursive core. Base case: depth == 0 or branch too short.
    Recursive case: draw this branch, then call draw_branch() twice
    more (self-similarity) for the two shorter, rotated child branches.
    """
    if depth <= 0 or length < 2:
        return

    x2 = x1 + length * math.cos(angle)
    y2 = y1 - length * math.sin(angle)

    t = 1 - depth / max_depth  # 0 at trunk, 1 at tips
    color = gradient_color(t, anchors, flat_bands)
    thickness = max(1, int(round(depth * 1.0)))

    if outline:
        pygame.draw.line(surface, OUTLINE_COLOR, (x1, y1), (x2, y2), thickness + 3)
    if glow_surface is not None:
        glow_color = (min(255, color[0] + 30), min(255, color[1] + 30),
                      min(255, color[2] + 30), 90)
        pygame.draw.line(glow_surface, glow_color, (x1, y1), (x2, y2), thickness + 9)
    pygame.draw.line(surface, color, (x1, y1), (x2, y2), thickness)

    new_length = length * ratio
    # --- the two recursive calls: heart of the fractal ---
    draw_branch(surface, x2, y2, new_length, angle + math.radians(branch_angle),
                depth - 1, max_depth, branch_angle, ratio, anchors, flat_bands,
                outline, glow_surface)
    draw_branch(surface, x2, y2, new_length, angle - math.radians(branch_angle),
                depth - 1, max_depth, branch_angle, ratio, anchors, flat_bands,
                outline, glow_surface)


def draw_mandala(surface, cx, cy, n_arms, trunk_length, depth, branch_angle,
                  ratio, rotation, anchors, flat_bands, outline, glow_surface):
    """Radial symmetry: call the recursive branch function once per arm,
    evenly spaced around the center -- this is what turns the tree into
    a mandala while the underlying generative rule stays recursive."""
    for arm in range(n_arms):
        base_angle = math.pi / 2 + arm * (2 * math.pi / n_arms) + rotation
        draw_branch(surface, cx, cy, trunk_length, base_angle, depth, depth,
                    branch_angle, ratio, anchors, flat_bands, outline, glow_surface)
    # small center disc as a clean focal point
    pygame.draw.circle(surface, anchors[0], (int(cx), int(cy)), 8)


# ---------------------------------------------------------------
# MAIN PROGRAM LOOP
# ---------------------------------------------------------------
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Interactive Fractal Mandala — Design Lab 01")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("consolas", 16)

    palette_index = 0
    glow_enabled = True
    flat_mode = False
    anim_paused = False
    show_hud = True
    ratio = 0.72
    spread = 24.0

    rotation = 0.0
    t = 0.0
    growth = 0.0  # 0 -> 1 growth-in animation on launch

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0
        if not anim_paused:
            t += dt
            rotation += ROTATION_SPEED * dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    anim_paused = not anim_paused
                elif event.key == pygame.K_h:
                    show_hud = not show_hud
                elif event.key == pygame.K_f:
                    flat_mode = not flat_mode
                elif event.key == pygame.K_UP:
                    ratio = min(MAX_RATIO, ratio + 0.02)
                elif event.key == pygame.K_DOWN:
                    ratio = max(MIN_RATIO, ratio - 0.02)
                elif event.key == pygame.K_RIGHT:
                    spread = min(MAX_SPREAD, spread + 1.5)
                elif event.key == pygame.K_LEFT:
                    spread = max(MIN_SPREAD, spread - 1.5)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    palette_index = (palette_index + 1) % len(PALETTE_NAMES)
                elif event.button == 3:
                    glow_enabled = not glow_enabled

        mx, my = pygame.mouse.get_pos()
        mx = max(0, min(WIDTH, mx))
        my = max(0, min(HEIGHT, my))
        n_arms = int(round(MIN_ARMS + (mx / WIDTH) * (MAX_ARMS - MIN_ARMS)))
        n_arms = max(MIN_ARMS, min(MAX_ARMS, n_arms))
        depth = int(round(MIN_DEPTH + (1 - my / HEIGHT) * (MAX_DEPTH - MIN_DEPTH)))
        depth = max(MIN_DEPTH, min(MAX_DEPTH, depth))

        if growth < 1.0:
            growth = min(1.0, growth + dt / 2.0)

        breathing = 1.0 + BREATH_AMOUNT * math.sin(t * BREATH_SPEED)
        trunk_length = TRUNK_LENGTH * growth * breathing

        anchors = PALETTES[PALETTE_NAMES[palette_index]]
        flat_bands = 5 if flat_mode else 0

        # --- Render ---
        screen.fill(BG_COLOR)
        glow_surface = None
        if glow_enabled:
            glow_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

        draw_mandala(screen, WIDTH / 2, HEIGHT / 2, n_arms, trunk_length,
                     depth, spread, ratio, rotation, anchors, flat_bands,
                     True, glow_surface)

        if glow_surface is not None:
            # blur-free cheap glow: additive blend of the wide translucent
            # lines already drawn onto glow_surface, placed beneath is not
            # possible after the fact, so we overlay with ADD for a bloom
            # highlight on top of the crisp lines instead.
            screen.blit(glow_surface, (0, 0), special_flags=pygame.BLEND_ADD)

        if show_hud:
            lines = [
                f"Palette: {PALETTE_NAMES[palette_index]}  (left-click to cycle)   "
                f"Mode: {'FLAT' if flat_mode else 'GRADIENT'} (F)",
                f"Arms: {n_arms}   Depth: {depth}   Spread: {spread:.0f}deg   Ratio: {ratio:.2f}",
                f"Glow: {'ON' if glow_enabled else 'OFF'} (right-click)   "
                f"Anim: {'PAUSED' if anim_paused else 'ON'} (SPACE)",
                "Mouse: X = arms | Y = depth   LEFT/RIGHT = spread   "
                "UP/DOWN = ratio   H = hide HUD",
            ]
            for i, line in enumerate(lines):
                text_surf = font.render(line, True, (230, 230, 235))
                screen.blit(text_surf, (12, 10 + i * 20))

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
