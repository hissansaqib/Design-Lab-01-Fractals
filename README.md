# The Fractal Canopy: Energy & Symmetry
**Design Lab 01: Designing Using Fractals**

**Student Name:** Muhammad Hissan Saqib  
**Registration Number:** 543530  

## Project Description
"The Fractal Canopy" is a visual composition generated entirely through recursive mathematical functions. It features a central glowing energy conduit (the trunk) that mathematically branches out into a dense canopy of 16 interconnected, 6-arm geometric mandalas. The madalas python file shows an interactive visualization of the mandalas that inspired the tree design. The root system mirrors the canopy with an inverted fractal structure that fades into the background, anchoring the design.

## Fractal Types Implemented
1. **Recursive Fractal Tree:** Used for the main skeletal structure of the trunk and branches.
2. **Inverted Fractal Roots:** A descending recursive tree with modified angles and length ratios.
3. **Recursive Starbursts / Mandalas:** At the terminal nodes of the tree (depth 1), the algorithm triggers a completely different recursive function to bloom 6-arm geometric clusters.

## Creativity & Design Elements
* **Dynamic Color Engine:** Uses linear interpolation (`lerp`) to calculate colors mathematically based on the X/Y coordinates and depth of the branches. 
* **Two-Pass Vector Rendering:** To achieve a cohesive "sticker" or "apparel" aesthetic, the script stores all geometric segments in a 2D array. It then renders a background pass (thick black lines for silhouettes) followed by a foreground pass (vibrant colors), merging thousands of intersecting branches into a single seamless shape.

## Tools, Languages, and Libraries Used
* **Language:** Python 3.x
* **Libraries:** 
  * `matplotlib.pyplot` (for drawing the vector lines and rendering the canvas)
  * `math` (for trigonometric calculations, angles, and geometry)

## Setup and Run Instructions
1. Ensure you have Python installed on your system.
2. Install the required `matplotlib` library by running the following command in your terminal:
`pip install matplotlib`
3. Run the python script:
`python fractal_canopy.py`
4. The terminal will display the generation progress, and upon completion, a high-resolution image named `fractal_masterpiece_final.png` will be saved in the same directory.

## Visual Outputs

### 1. Interactive Simulation (Pygame)
Here is a preview of the interactive, rotating fractal mandala:
![Mandala Simulation](mandala_simulation.gif)

### 2. T-Shirt Design Masterpiece (Matplotlib Vector Export)
Here is the high-resolution, print-ready vector composition featuring the luminous energy trunk and 16 interconnected gradient mandalas:
![T-Shirt Design](fractal_masterpiece_final.png)