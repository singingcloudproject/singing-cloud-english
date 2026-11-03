# SEO report — singing-cloud-english (English, Russian, Armenian)

Date: 3 November 2026 · Status: **online at https://singingcloudproject.github.io/singing-cloud-english/ but hidden from Google and Yandex with "noindex"** (see "Going live" below)

## Keywords chosen
Picked from how people really search (and how the big schools that rank — Skyeng, italki, Preply, British Council Armenia, local Yerevan schools — word their pages). Used naturally in titles, headings, intros and descriptions.

**Russian (Google + Yandex)** — the main focus
- репетитор английского онлайн (online English tutor) — the core phrase
- английский с носителем языка онлайн (English with a native speaker online)
- индивидуальные уроки английского онлайн (one-on-one online lessons)
- разговорный клуб английский онлайн (English speaking club online)
- подготовка к IELTS онлайн (IELTS preparation online)
- бизнес английский (Business English)
- английский для детей и подростков онлайн (English for kids & teens)
- пробный урок английского (trial English lesson)

**Armenian (Google)** — Armenian students also often search in English and Russian, which the other two language pages cover
- անգլերենի առցանց դասընթացներ (online English courses) — the most common phrase on Armenian school sites
- անգլերենի առցանց դասեր (online English lessons)
- անգլերենի անհատական դասեր (one-on-one English lessons)
- անգլերեն լեզվակրի հետ (English with a native speaker)
- IELTS-ի նախապատրաստում (IELTS preparation)
- խոսակցական անգլերեն (conversational English) · Speaking Club
- անգլերեն երեխաների համար (English for children)

**English**
- online English tutor · online English lessons
- learn English with a native speaker online
- English speaking club online · IELTS preparation online · Business English lessons online · English lessons for kids online

Note: Yandex Wordstat (wordstat.yandex.ru) shows exact Russian search volumes but needs a Yandex login — worth a quick check before launch.

## What changed
**On-page**
- Titles: "Online English Tutor & Native Speakers | …", "Репетитор английского онлайн и носители языка | …", "Անգլերենի առցանց դասեր լեզվակիրների հետ | …".
- Descriptions (under 150 characters) with lesson types and "from $12 / от 1 200 ₽".
- The line under the main heading and the opening paragraph now name one-on-one lessons, native speakers, the Speaking Club and IELTS.
- Armenian: hero label and lessons intro reworded with the search phrases; photo descriptions updated in all languages.
- The singing cloud has a proper description in each language.

**Honest content (nothing invented)**
- Removed the "[100+] students" placeholder stat. Kept only your real facts: 6 years of teaching and your master's degree.

**Technical**
- `noindex` on every page (switch: `"noindex": true` in `content/site.json`).
- Canonical links, `hreflang` (en, ru, hy, x-default) and a sitemap with alternate-language links and today's date.
- Open Graph + Twitter/X tags with a new 1200×630 sharing image (`assets/og-image.jpg`); the other languages are listed as alternates.
- Structured data: `EducationalOrganization` (lesson types, languages, and your prices — USD on the English and Armenian pages, rubles on the Russian page), `WebSite`, `WebPage` and `FAQPage` (your FAQ questions and answers).
- robots.txt allows crawling on purpose (search engines must read a page to see "noindex").
- Already fast: animation pauses off-screen; flags are tiny SVGs; fonts load with `display=swap`.

## Still to do by you
- **Armenian text is a draft** — have a native Armenian speaker check it (including the new SEO wording) before launch.
- Russian wording: worth a quick check by a native speaker too.

## Going live — checklist
1. Set your real web address in `content/site.json` → `"site_url"` (now `https://singingcloudproject.github.io/singing-cloud-english/`).
2. Set `"noindex": false`, then run `python build.py`.
3. Add the site to **Google Search Console** and **Yandex Webmaster** (important for Russian students) and submit `sitemap.xml` in both.
