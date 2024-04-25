# upwards

A pygame platformer by jswessler
Requires: pygame > 2.3, numpy

id146.1 (planned)
* Significantly reduced lag in level generator (by only drawing the part of the screen you're looking at)
* Changed hex art

id145.4p
* Github is now public
- Slightly reduced width of floor collision (to not interfere with the wall collision)
- Cleaned up wall riding physics, extended right-side hitbox to better align with animiations
- Removed extraneous dive behavior
- Half/Quarter Blue hearts now heal properly

id145.3
- Made spawnpoints work properly

id145.2
- Made floor collision cover more of your body, which should eliminate getting stuck halfway in walls

id145.1
* You now spawn at a designated spawn point (5-0 tile). This currently only works if the spawnpoint is on-screen at the time of spawning naturally.
* Level generator now has descriptions (based on lvldesc.txt)
- Added speed option for level generator
- Cleaned up 'Other' folder
- Camera box is now only visible when pressing R
- Camera box is 50% less sticky (mouse movement has 0.5x impact when in box, rather than 0x)

id144.1 (previously id42424.1)
- Code&Comment adjustments
- Adjusted Kunai behavior & spawn position
- Level creator now tied to specific build

8/11/23 Build 1
* Added throwing knives & HUD

8/9/23 Build 1
- Lowered top speed
- Various Fixes

7/31/23 Build 3
- Added maxSpd, you can now run 3.15u/f instead of 2.05u/f
- Double jump & dive give you more horizontal speed
- Nerfed silver hearts

7/31/23 Build 2
- Adjusted landing physics

7/31/23 Build 1
- Adjusted energy regen, brought back mid-air regen

7/29/23 Build 1
* Show debug text on every block with T
- Adjusted hover physics
- Moved loading tilemap into loadlevel function
- Silver hearts fully implemented
- Standardized & expanded collision detection

7/28/23 Build 1
* New renderer, draws actual tiles instead of pg.rect
* Shows tiles on level editor
- Adjusted physics
- Energy regens slower
- Lag reduction (Hearts, Level Renderer)
- Sensor now detects subtypes
- DoubleBuf mode
- Silver hearts can spawn
