# Singing Cloud English — website

A one-page website in English (main), Russian and Armenian.
Nothing has been uploaded yet — it all lives in this folder on your computer.

## What's in this folder

| File / folder | What it is | Do you edit it? |
|---|---|---|
| `content/en.json`, `ru.json`, `hy.json` | **All the words on the site**, one file per language | ✅ Yes — this is where you change text |
| `content/site.json` | Settings: WhatsApp number, the two Formspree form IDs, website address, languages | ✅ Yes |
| `assets/styles.css` | The look: colours, fonts, animations | Only if you want to change the design |
| `logo.png` | Your 3D cloud logo (copied from Singing Cloud Studio) | No |
| `assets/logo-header.*`, `logo-hero.png` | The logo with a transparent background: small (header/footer) and large (shown to Google) | No |
| `assets/favicon-32.png`, `favicon-180.png` | The browser-tab icon and the phone home-screen icon | No |
| `mascot.py` | Draws the singing cloud in the hero as layers so its mouth can move (same cloud as the Studio) | Only to change its look |
| `assets/flags/` | The official Canada, USA and UK flags (from Wikimedia Commons) | No |
| `assets/script.js` | Small helpers: phone menu, fade-in animation, sending the form | No |
| `build.py` | The "page builder": turns the text files into web pages | No |
| `index.html`, `ru/index.html`, `hy/index.html` | The finished pages (made by `build.py`) | ❌ No — they get overwritten |
| `sitemap.xml`, `robots.txt` | Help Google find all three languages | No (made by `build.py`) |

## How to change text

1. Open `content/en.json` (or `ru.json` / `hy.json`) in Notepad or VS Code.
2. Change only the words **inside the quotes on the right side**, e.g.
   `"title": "Lessons for every goal"` → `"title": "English lessons for every goal"`.
   Keep the quotes, commas and brackets exactly as they are.
3. Open a terminal in this folder and run:

   ```bash
   python build.py
   ```

4. Double-click `index.html` to see the result in your browser.

Anything in `[square brackets]` is a placeholder for you to replace.
The Russian text is a draft translation — please check it. **The Armenian text (`hy.json`) is a DRAFT for a native Armenian speaker to check** before the site goes live (the file starts with a note saying so, and the Armenian page carries a hidden reminder in its code).

## Things to fill in before going live (`content/site.json`)

- **`whatsapp_number`** — your WhatsApp number, digits only with country code, no `+` or spaces (e.g. `374XXXXXXXX`).
- **`formspree_id`** — the contact form for students. Create a free form at formspree.io; it gives you an address like `https://formspree.io/f/abcdwxyz`. Put just the last part (`abcdwxyz`) here. Until then, the form politely tells visitors to use WhatsApp.
- **`formspree_teachers_id`** — the "Teach with us" application form. Make a **second** Formspree form (so teacher applications arrive separately) and put its ID here.
- **`site_url`** — your real web address once you have one (used by Google).

## Adding your photo and intro video

- **Photo:** make a folder called `images`, put your photo in it (e.g. `images/me.jpg`), then in `content/site.json` set `"about_photo": "images/me.jpg"`.
- **Intro video:** upload it to YouTube (it can be "Unlisted"). Copy the code at the end of the link — for `https://youtu.be/AbC123xyz` that's `AbC123xyz` — and set `"intro_video_youtube_id": "AbC123xyz"` in `content/site.json`.
- **Bio:** edit it in the language files (`[square brackets]` are placeholders).
- Run `python build.py` after any change.

## Russian search words

The Russian page uses the phrases **«репетитор английского онлайн»** and **«бизнес английский»** in the page title, the Google description and the headings, so Russian speakers searching for them are more likely to find you. If you rewrite the Russian text, try to keep those phrases.

## About the look

Warm and calm on purpose: white and soft cream backgrounds, sky-blue and gold accents, the rounded Nunito font (Noto Sans Armenian for Armenian, because Nunito has no Armenian letters). Sections fade in gently as you scroll.

The **singing cloud** in the hero is your 3D logo, redrawn so its mouth can move — the same singer as on Singing Cloud Studio: it opens wide ("ah"), round ("oh") and nearly closed ("mm") to a little melody, stretches up on big notes and squashes down between phrases. Instead of music notes, the letters **A, B, C, D** float out of its mouth one after another in soft colours (sky blue, gold, coral, mint) and fade away. It pauses when the hero is off screen. If a visitor has **"Reduce motion"** switched on, the cloud stays still and no letters appear.

This site's design is separate from Singing Cloud Studio's dark tech look — changing one does not change the other.

## Prices

Prices live in each language file under `"prices"`: English and Armenian show US dollars, Russian shows rubles.
Each card has `"for"` (who teaches), `"name"`, `"price"` and `"per"`; `"best": true` adds the gold **Best value** badge.
The line at the top is `"range"`.

## Teach with us

A section near the bottom (linked from the footer and the Teachers section) invites teachers to apply. The form asks for name, email, country, native language, years of experience, the lessons they can teach (tick boxes), weekly availability, a link to an intro video and a message. Applications go to the Formspree form set in `formspree_teachers_id`.
