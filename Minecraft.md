# Minecraft Prompt

## Original

```
Create a completely playable minecraft clone from scratch with following list in mind:

- A single html file hosting everything. 
- Using Three JS
- Having different materials in order to build homes and other structures. 
- A good realistic biome. 
- Player uses WASD controllers to move, left click to hit things and right click to put things in place (like original game)

Excess CSS or JS code must be included inside the main html file since it's a proof of concept.
```

## Improved

```
Here's a significantly more detailed and structured version of your prompt:

---

# Build a Fully Playable Minecraft Clone in a Single HTML File

## Overview
Create a complete, playable voxel-based sandbox game (Minecraft clone) from scratch, packaged entirely within a single self-contained HTML file. Use Three.js (loaded via CDN) for 3D rendering. This is a proof-of-concept, so all CSS and JavaScript must live inside the HTML file — no external stylesheets, no separate `.js` files, no build step.

## Technical Requirements

### 1. Single File Architecture
- One `.html` file containing all HTML, CSS (inside `<style>` tags), and JavaScript (inside `<script>` tags).
- Load Three.js from a CDN (e.g., `https://unpkg.com/three@0.160.0/build/three.min.js` or a similar reliable CDN).
- No bundlers, no npm, no transpilation — just open the file in a browser and play.

### 2. Rendering Engine: Three.js
- Use Three.js for all 3D rendering, camera control, lighting, and scene management.
- Implement a first-person camera using `PointerLockControls` (or a custom equivalent) so mouse movement controls the view.
- Include directional sunlight + ambient light for a natural outdoor feel.
- Implement basic sky (sky-blue background or a gradient).
- Add simple fog so distant terrain fades naturally, hiding the world boundary.

### 3. World Generation & Biomes
- Implement procedural terrain generation using a noise function (e.g., a simple Perlin/Simplex noise implementation included inline, or a lightweight library via CDN).
- Generate at least **two distinct biomes** that blend naturally:
  - **Grassland/Forest biome** — grass-covered terrain with scattered trees (trunk + leaf blocks), gentle hills.
  - **Desert biome** — sand terrain, flatter, with occasional cactus structures.
- Terrain should have varied elevation (hills, valleys) driven by noise.
- World size: at minimum a 64×64 or 128×128 block grid with enough depth for hills and underground. Choose a size that performs well in-browser.

### 4. Block & Material System
- Define a block-type registry with at least these materials:
  - **Grass** (green top, dirt sides)
  - **Dirt** (brown)
  - **Stone** (gray)
  - **Wood/Log** (brown with bark texture)
  - **Leaves** (green, semi-opaque)
  - **Sand** (tan/yellow)
  - **Water** (blue, semi-transparent, non-collidable)
  - **Plank** (for building structures)
- Each block type should have visually distinct colors or simple procedural textures (you can use solid colors, vertex colors, or canvas-generated textures — no external image files).
- Blocks should use a unit cube geometry (1×1×1). Optimize by using instanced meshes or merged geometries per block type so the game doesn't lag.

### 5. Player Controls & Interaction
- **Movement:** WASD keys for walking, Space to jump, Shift to crouch/descend (if flying). Implement basic gravity and collision detection against blocks (don't let the player walk through terrain or fall through the world).
- **Camera/Mouse:** Pointer lock for first-person look (mouse moves the view).
- **Left Click:** "Mine" or "hit" — remove/destroy the block the player is looking at (raycasting from camera center to find the targeted block).
- **Right Click:** "Place" — place the currently selected block type adjacent to the targeted block face.
- **Number Keys (1–8) or Scroll Wheel:** Switch between available block types in the hotbar.
- Show a simple **hotbar UI** at the bottom of the screen indicating the currently selected block type (can be colored squares with labels).
- Show a **crosshair** in the center of the screen.

### 6. Physics & Collision
- Implement AABB (axis-aligned bounding box) collision between the player and solid blocks.
- Apply gravity to the player each frame.
- Allow jumping when standing on a block (ground check).
- Prevent falling through the world — if the player goes below a certain Y, respawn them on the surface.

### 7. Performance
- Use **greedy meshing** or at minimum **face culling** (don't render faces between two adjacent solid blocks) to keep frame rates acceptable.
- Only render/track blocks within the generated world bounds.
- Consider chunking the world (e.g., 16×16 chunks) and only rendering visible chunks if the world is large.

### 8. UI / HUD
- **Crosshair** centered on screen.
- **Hotbar** at bottom showing available blocks and current selection.
- Optionally: a small instructions overlay on start ("Click to play — WASD to move, Left click to break, Right click to place, 1-8 to select block").
- Click-to-start screen that requests pointer lock.

## Deliverable
A single `index.html` file that, when opened in any modern browser (Chrome/Firefox/Edge), immediately launches a playable Minecraft-like sandbox where the player can walk around a procedurally generated biome-rich world, mine blocks, place blocks, and build structures.

---

**Key improvements made to your original prompt:**
- Specified exact block types and their visual characteristics.
- Added collision detection, gravity, and physics requirements (your original didn't mention these — without them the game isn't "playable").
- Added performance guidance (face culling/chunking) so it actually runs smoothly.
- Specified the noise-based terrain generation approach.
- Added hotbar UI, crosshair, and click-to-start overlay.
- Clarified the biome requirements with concrete examples.
- Added water as a non-collidable block type for realism.
- Specified texture approach (procedural/canvas-based, no external assets).
- Added a clear deliverable statement.
```

