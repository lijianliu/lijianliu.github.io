# Radio Quest — Island Defender

Static HTML / CSS / JavaScript / Three.js game. Upload the contents of dist/
to an HTTP/HTTPS static host. No build, backend, external CDN, account or API key.
For local preview: inside dist/ run python3 -m http.server 8000.

GAMEPLAY
Walk around a 3D island using the thumb joystick, WASD or arrow keys.
Hold FIRE (or Space) to shoot auto-aimed energy bolts at nearby rogue robots.
Robots approach, avoid obstacles, and deal contact damage. Each needs two hits.
A correct HAM answer restores 35 health and adds eight shots, capped at 100 HP
and 30 shots. Press HEAL + RELOAD (or E) to answer. Combat pauses while reading.
Wrong answers enter the missed queue. A downed hero recovers by answering.
Defeat a wave to unlock the next island with more enemies and a new palette.
Pause with P or the top-right button. Sound starts after a user gesture.

QUESTIONS AND SAVES
409 official questions and keys from the supplied 2026–2030 Technician pool,
February 19, 2026 release, including its four errata and all three circuit figures.
Choose ordered, random, or missed-question mode and optionally a topic.
Original source wording and answer order are retained.

Existing Radio Quest study progress is preserved using the same localStorage
key: radioquest-technician-2026-v1. Combat state, enemies, position, health,
ammunition and island progress are saved too. Answers and recharge rewards
are saved together; reloading feedback does not award a second recharge.
Progress remains on this browser and origin; no automatic device sync.
Pause-menu JSON backups support transfer between browsers or devices.
Clearing website data or ending private browsing may remove saves.
Assets initially load from the static host; offline availability is not guaranteed.

FILES
index.html / style.css — full-screen mobile game UI
app.js — question panels, audio, save/restore, menus and game integration
combat.js — damage, health, ammo and wave rules
battle.js — 3D terrain, hero, robots, movement, combat, minimap and effects
engine.js — retained study logic, scoring, randomization and missed queue
questions.js — complete official question data
figure-T-*.png — source circuit diagrams
three.module.js / THREE-LICENSE.txt — bundled Three.js engine and license
space.js — original satellite scene retained for reference, not loaded

VALIDATION
JavaScript syntax and static asset references checked. Core tests cover ammo
consumption, enemy hits and defeat, wave progression, downed recovery, save
round-trips, reward caps and duplicate-answer prevention. No browser/device
UI testing was performed. This is a study game, not an official examination.
