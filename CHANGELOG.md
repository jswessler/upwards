Release Log:

id149.1
- Moved changelog to a new file
- Double jump glitch is gone

id148.3
* Added sliding (no animation yet)
   - Press S on the ground for a speed boost on a cooldown
   - Press S right after landing for a bigger speed boost
   - Jump at the end of the slide for a higher jump
   - Sliding off a ledge gives some extra airtime
   - Sliding can get you under obstacles
* Wallslide animation
- Wallslide is now more like a slide rather than low gravity
- Physics adjustments & fixes

id148.2
- Debug fixes
- Prep for physics overhaul (fork)

id148.1
* Tile updating now only occurs on-screen (about a 10% FPS gain)
- Different collision detection objects now have different debug colors to differentiate them
- Reduced amount of collision detection to reduce lag
- Fixed several animation problems when idealFps is not set to 60
- Diving while having 0 x-velocity now sends you in the direction you're facing (as opposed to always right)
+ Known issue - when collecting multiple dash crystals at once, double jump may be disabled until walljumping/collecting another dash crystal

id147.1
- Jump animations no longer bounce around a ton
- Jump animations when facing left also bounce around less
- Adjusted silver hearts (90% reduced flat energy gain, but each full heart gives you about 3% reduced gravity and slightly better air movement)
- Holding W now improves your platforming very slightly again


id146.2
- Clicking on phone no longer spams pause/unpause
- You can now pause with ESC

id146.1
* Changed hex art
- Slightly adjusted some physics

id145.4p
* Github is now public
- Slightly reduced width of floor collision (to not interfere with the wall collision)
- Cleaned up wall riding physics, extended right-side hitbox to better align with animiations
- Removed extraneous dive behavior
- Half/Quarter Blue hearts now apply properly

id145.3
- Made spawnpoints work no matter where they are in the map

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