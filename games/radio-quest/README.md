# Radio Quest — Signal Academy

A static, iPhone-first HAM radio study game. No build, backend, API keys,
accounts, analytics, or network calls during gameplay are required.

## Host
Upload the contents of `dist/` to any HTTP/HTTPS static web host.
Open `index.html`. Keep all files together; paths are relative.
The JavaScript game logic, sound synthesis, question pool, figures, and
Three.js engine are local assets. No external fonts or CDN are used.

For local testing, from dist/ run `python3 -m http.server 8000` and open
http://localhost:8000. Use HTTP rather than opening file:// directly,
because the 3D scene uses a JavaScript module. The question game remains
usable if WebGL is unavailable. A static server serves files only.

## Play
- Campaign: questions in source order; resumes the next unanswered question
  per selected topic. Wrong answers are added to Repair bay.
- Signal scramble: up to 10 unique random questions from the selected topic.
- Repair bay: up to 10 missed questions, with the most recent failure first
  when it belongs to the selected topic. A correct retry removes it.
- Resume your mission: restores the exact active question and its answer
  feedback, even if the browser closed before Next was tapped.
- 10 XP for correct answers; an extra 15 XP for every five-answer streak.
  Ranks unlock every 500 XP, up to Galaxy Commander. No timers or lost lives.
- Audio starts with a user gesture. The sound button saves the mute setting.

## Progress
Stored in localStorage under radioquest-technician-2026-v1 after each answer
and transition. Data is tied to this browser and site origin, does not sync
between devices, and can be lost when browser/site data is cleared or private
browsing ends. Settings includes JSON backup and restore. Download a backup
before changing hosts or clearing browser data. No progress is sent to a server.
Assets need to load from your static host; there is no guaranteed offline cache.

## Content
409 questions and answer keys from the supplied:
2026-2030 Technician Pool and Syllabus Public Release Feb 19 2026.pdf
Effective July 1, 2026 through June 30, 2030.
Includes February 19 errata for T1C01, T5A05, T7A09 and T0A10.
Original question wording and option order are retained; PDF line breaks are
normalized. Three circuit figures are cropped from source pages 78–79.
Feedback uses the source answer key, not generated technical explanations.
This game is practice, not an official exam or a substitute for instruction.

## Files
- dist/index.html: page shell and settings
- dist/style.css: mobile-first interface
- dist/questions.js: complete readable question data and official answer keys
- dist/engine.js: progress, scoring, mission selection and retry rules
- dist/app.js: UI, browser storage, audio and backups
- dist/space.js: optional animated Three.js satellite scene
- dist/figure-T-1.png through figure-T-3.png: official circuit figures
- dist/three.module.js and dist/THREE-LICENSE.txt: Three.js 0.160.1 and MIT license

## Verification
Checked all 409 unique IDs, four nonempty options and keys; all figure references;
four published errata; reload with an answered question; duplicate-answer guard;
missed priority and repair removal; unique random topic selection; campaign
continuation; XP and streak totals. JavaScript syntax and local assets validated.
No device/browser UI testing was performed in this build.
