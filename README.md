# Watch Review

A small web app for the phone: go through the Zotero items that Partitur's
literature watch has put in **`<top collection> / Bevakning`**, one at a time. Zotero for Android can't edit tags,
so this does it straight through Zotero's web API.

For each item you see the title, authors, journal, abstract and Claude's note on why it was picked, and choose:

- **Read** – one tap on a reading tag (`to-read`, `to-skim`, `to-read-methods`, `to-read-background`,
  `to-review`).
- **Keep** – kept in the library, nothing to read now.
- **Reject** – to Zotero's trash (recoverable there).
- **Skip** – the next one; this one stays.

Read and Keep take the item out of Bevakning into its field's top collection (e.g. *F – Forskning*), from which
Partitur's `sort_articles` moves it into the right subcollection; remove the tag `bevakning` (= gone through); and add
the tag `från-bevakning`, so you can always see where it came from. Every action can be undone right after (*Undo*).

## Use

Open the page on the phone, then the browser's menu → *Add to Home screen* (it works as an app). Settings (⚙):
your Zotero API key – zotero.org → Settings → Security → *Create new private key*, with **Allow library access**
and **Allow write access**. The key is kept in this browser only and sent only to `api.zotero.org`.

## How it works

One page, `index.html`, no build step and no server of its own: it reads the collections named *Bevakning*, the
items in them tagged `bevakning`, and each item's child note tagged `claude-bevakning`, and changes items with
`PATCH` (with Zotero's version check: if the item was changed elsewhere meanwhile, the change is made again on
the item as it is now). `sw.js` keeps the app's own files for offline start; Zotero's answers are never cached.

Try it without touching a real library: `python tests/mock_zotero.py`, then open
<http://localhost:8765/?api=http://localhost:8765> (any key works; `?api=` alone switches back to Zotero).

## Licence

Copyright (C) 2026 Sebastian Ibstedt. GNU Affero General Public License v3.0 or later (`LICENSE`). Not affiliated
with or endorsed by Zotero or the Corporation for Digital Scholarship.
