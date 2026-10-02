# BandCraft 2D (Mi Band 9)  -  v0.6.0

Built on top of the working 0.4.0 build (same package `com.breno.bandcraft.stable`, so it replaces it).

## Build
    npm install
    npm run build          # -> dist/com.breno.bandcraft.stable.debug.0.6.0.rpk
(`npm start` = `aiot start`; this toolkit has no `--watch` option.)

## IMPORTANT: manifest.json
`"deviceTypeList": ["watch"]` MUST stay in src/manifest.json. Without it aiot-toolkit builds a
phone (Android) quick app, which the band opens and closes instantly.

## Where to edit
- `src/pages/game/game.ux`  : game logic. Top of the <script> has CONFIG (walk speed, jump, gravity).
- `tools/make_assets.py`    : draws src/common/generated/*.png (scene, hotbar, HUD, buttons, craft panel).
                              Needs `pip install pillow`. Run: `python tools/make_assets.py`
- Layout numbers (block 32px, 6 columns, hotbar slots, buttons) are listed at the top of BOTH files and must match.

## Controls
Left / Right: HOLD to walk.  Up arrow: jump.  Pickaxe: mine the block in front of Steve.
Block icon: place the selected hotbar block (slots 1-6 are placeable).  4-squares icon: crafting panel (visual only).

## World
The world is 40 screens wide (6 blocks each). Walk off the right/left edge to go to the next/previous screen.
Mined / placed blocks are remembered per screen. Looks (plains / forest / desert) are set by `LOOK` in game.ux.
## Holding buttons
Walk, jump, mine and place all work while held. If the band sends only "click" events (no touch events),
tap an arrow to start walking and tap it again to stop.
