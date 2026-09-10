"""
=====================================================================
  THE FRACTAL CANOPY — T-SHIRT DESIGN MASTERPIECE (FINAL VERSION)
=====================================================================
A fully recursive fractal tree that bursts into 16 interconnected 
mandalas. Features a custom 2-Pass rendering engine to perfectly merge 
thousands of intersecting branches into a single seamless vector shape.
The Trunk is a high-visibility glowing energy conduit, and the roots
have been extended for better visual balance!
"""

import matplotlib.pyplot as plt
import math

# ---------------------------------------------------------------
# DYNAMIC COLOR ENGINE
# ---------------------------------------------------------------
# Canopy Palettes (Horizontal X-Axis Gradient)
PALETTE_SUNSET   = [(255, 32, 110), (255, 140, 66), (255, 214, 90)]
PALETTE_TOXIC    = [(0, 100, 120),  (0, 214, 150),  (198, 255, 92)]
PALETTE_ELECTRIC = [(45, 0, 120),   (123, 47, 247), (0, 229, 255)]

# Tree & Root Palettes (Vertical Y-Axis Gradient for high visibility)
# Trunk fades from Luminous White/Blue -> Electric Cyan -> Deep Purple
PALETTE_TRUNK    = [(240, 248, 255), (0, 229, 255), (123, 47, 247)]
# Roots fade from Dark Navy (tips) -> Vibrant Blue -> Luminous White (base)
PALETTE_ROOTS    = [(10, 15, 30),    (0, 120, 200), (240, 248, 255)]

def lerp_color(c1, c2, t):
    """Linear interpolation between two RGB tuples."""
    r = int(c1[0] + (c2[0] - c1[0]) * t)
    g = int(c1[1] + (c2[1] - c1[1]) * t)
    b = int(c1[2] + (c2[2] - c1[2]) * t)
    return (r, g, b)

def rgb_to_hex(rgb):
    return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"

def blend_palettes(pal1, pal2, t):
    """Blends two entire palettes together based on a ratio t (0 to 1)."""
    return [lerp_color(pal1[i], pal2[i], t) for i in range(3)]

def get_palette_for_x(x):
    """Calculates a custom palette based on the horizontal position in the tree."""
    # The tree canopy spans roughly from X = -180 to X = +180
    min_x, max_x = -180.0, 180.0 
    t = (x - min_x) / (max_x - min_x)
    t = max(0.0, min(1.0, t)) # Clamp between 0 and 1
    
    if t < 0.5:
        # Left side to Center: Blend Sunset into Toxic
        return blend_palettes(PALETTE_SUNSET, PALETTE_TOXIC, t * 2)
    else:
        # Center to Right side: Blend Toxic into Electric
        return blend_palettes(PALETTE_TOXIC, PALETTE_ELECTRIC, (t - 0.5) * 2)

def get_gradient(palette, t):
    """Gets the specific color from a palette based on branch depth."""
    t = max(0.0, min(1.0, t))
    if t <= 0.5:
        return rgb_to_hex(lerp_color(palette[0], palette[1], t * 2))
    return rgb_to_hex(lerp_color(palette[1], palette[2], (t - 0.5) * 2))

# ---------------------------------------------------------------
# 2-PASS VECTOR ENGINE (Stores lines instead of drawing immediately)
# ---------------------------------------------------------------
SEGMENTS = []

def add_segment(x1, y1, x2, y2, color, lw, z_order):
    """Stores a geometric line to be rendered later."""
    SEGMENTS.append({
        'x': [x1, x2],
        'y': [y1, y2],
        'color': color,
        'lw': lw,
        'z': z_order
    })

# ---------------------------------------------------------------
# FRACTAL GENERATORS
# ---------------------------------------------------------------
def generate_mandala_arm(x, y, angle, length, depth, max_depth, palette, z_base):
    """The recursive structure of the leaves/blooms."""
    if depth == 0 or length < 0.5: 
        return

    x2 = x + length * math.cos(angle)
    y2 = y + length * math.sin(angle)

    t = 1.0 - (depth / max_depth)
    color = get_gradient(palette, t)
    
    # Smooth taper
    lw = max(0.8, (depth / max_depth) * 4.5)
    
    # Add to our geometry engine
    add_segment(x, y, x2, y2, color, lw, z_base + depth)

    # Magic ratios for a dense, beautiful bloom
    spread = math.radians(24.5) 
    ratio = 0.72 

    generate_mandala_arm(x2, y2, angle + spread, length * ratio, depth - 1, max_depth, palette, z_base)
    generate_mandala_arm(x2, y2, angle - spread, length * ratio, depth - 1, max_depth, palette, z_base)

def generate_mandala(cx, cy, radius, z_base):
    """Creates a 6-arm radial starburst at the tip of a tree branch."""
    # Calculate this specific mandala's color palette based on its X coordinate!
    custom_palette = get_palette_for_x(cx)
    
    arms = 6
    for i in range(arms):
        angle = (math.pi * 2 / arms) * i + (math.pi / 2)
        generate_mandala_arm(cx, cy, angle, radius, 5, 5, custom_palette, z_base)

def generate_tree(x, y, angle, length, depth, max_depth):
    """The main recursive tree skeleton."""
    x2 = x + length * math.cos(angle)
    y2 = y + length * math.sin(angle)
    
    # Calculate brilliant glowing color for the trunk based on depth
    t = 1.0 - (depth / max_depth) # 0.0 at base (bright), ~0.8 at tips (darker)
    color = get_gradient(PALETTE_TRUNK, t)
    
    lw = max(4.0, (depth / max_depth) * 16.0)
    
    # Tree Z-order is lower so it sits behind the vivid canopy
    z_base = depth 
    add_segment(x, y, x2, y2, color, lw, z_base)

    if depth == 1:
        # BASE CASE: We reached the tips of the main tree. Sprout the Mandalas!
        generate_mandala(x2, y2, radius=42, z_base=20)
    else:
        # RECURSIVE CASE: Keep splitting the tree branches
        spread = math.radians(28)
        ratio = 0.76
        generate_tree(x2, y2, angle + spread, length * ratio, depth - 1, max_depth)
        generate_tree(x2, y2, angle - spread, length * ratio, depth - 1, max_depth)

def generate_roots(x, y, angle, length, depth, max_depth):
    """Grounds the design with a downward fractal that fades into the dark."""
    if depth == 0:
        return
    x2 = x + length * math.cos(angle)
    y2 = y + length * math.sin(angle)
    
    # Base of root (touching trunk) is t=1.0, tips are t=0.0
    t = depth / max_depth 
    color = get_gradient(PALETTE_ROOTS, t)

    # Calculate line width to seamlessly match the trunk thickness where they meet
    lw = max(2.0, (depth / max_depth) * 16.0)
    add_segment(x, y, x2, y2, color, lw, -depth)

    # Spread and length ratios for the roots
    spread = 0.48 
    ratio = 0.68
    
    generate_roots(x2, y2, angle + spread, length * ratio, depth - 1, max_depth)
    generate_roots(x2, y2, angle - spread, length * ratio, depth - 1, max_depth)

# ---------------------------------------------------------------
# RENDER & EXPORT
# ---------------------------------------------------------------
def main():
    print("Generating Fractal Geometry... (Calculating thousands of branches)")
    
    # 1. Generate all the math and lines
    # INCREASED ROOT DEPTH FROM 4 to 5! (Shortened initial length slightly to fit frame)
    generate_roots(0, 0, -math.pi/2, 45, 5, 5)
    
    # Tree generation remains unchanged
    generate_tree(0, 0, math.pi/2, 110, 5, 5)  

    print(f"Geometry finished. Rendering {len(SEGMENTS)} intersecting vectors...")

    # 2. Setup the canvas
    fig, ax = plt.subplots(figsize=(16, 16), dpi=300)
    bg_color = "#0A0A0F" # Almost pure black
    fig.patch.set_facecolor(bg_color)
    ax.set_facecolor(bg_color)
    ax.axis('off')

    # 3. THE 2-PASS RENDER (The secret to the "Sticker" aesthetic)
    
    # PASS 1: OUTLINES. Draw every single line purely in black, slightly thicker.
    for seg in SEGMENTS:
        ax.plot(seg['x'], seg['y'], color="#000000", lw=seg['lw'] + 3.8, 
                solid_capstyle='round', zorder=10)
                
    # PASS 2: FILLS. Draw the colors directly on top of the black silhouette.
    for seg in SEGMENTS:
        ax.plot(seg['x'], seg['y'], color=seg['color'], lw=seg['lw'], 
                solid_capstyle='round', zorder=100 + seg['z'])

    # 4. Save and wrap up
    ax.autoscale()
    plt.tight_layout(pad=1.5)

    filename = "fractal_masterpiece_final.png"
    plt.savefig(filename, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
    print(f"Masterpiece saved as '{filename}'! The roots are now deeper and more intricate.")
    
if __name__ == "__main__":
    main()