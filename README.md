# Watch Review

A small web app for the phone: go through the Zotero items that Partitur's
literature watch has put in **`<top collection> / Bevakning`**, one at a time. Zotero for Android can't edit tags,
so this does it straight through Zotero's web API.

The items come most relevant first (Claude's *hög* before *medel*), then oldest first. For each item you see the title, authors, journal, abstract and Claude's note on why it was picked, and choose:

- **Read** – one tap on a reading tag (`to-read`, `to-skim`, `to-read-methods`, `to-read-background`,
  `to-review`).
- **Keep** – kept in the library, nothing to read now.
- **Reject** – with a reason (off topic, too clinical, too technical, already known, weak study – or none), saved as
  the tag `avvisad: <reason>`; to Zotero's trash (recoverable there). Partitur's watch learns from your decisions:
  what you read, keep and reject – and why – is shown to Claude when it screens the next ones.
- **›** / **‹** – on to the next one or back to the one before (they stay).
- **＋ Project** – put it in one of your active projects (more than one is fine; × takes it out again). It stays in
  Bevakning: read, keep or reject it as before.

Read and Keep take the item out of Bevakning into its field's top collection (e.g. *F – Forskning*), from which
Partitur's `sort_articles` moves it into the right subcollection; remove the tag `bevakning` (= gone through); and add
the tag `från-bevakning`, so you can always see where it came from. Every change can be undone: *Undo* in the message right after, or the undo arrow at the top, as many steps back as you like (this session).

**Projects** come from Partitur: its `project_literature` keeps a Zotero note tagged `partitur-projekt` listing the
active project folders, and the projects Claude named for the item are offered first. Putting an item in a project
sets the tag `projekt: <vault> – <project folder>`; at Partitur's next run the item is added to that project's
`Litteratur (Claude).md` (with Claude's reason), marked *föreslagen av dig*.

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
