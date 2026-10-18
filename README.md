# Watch Review

A small web app for the phone: go through a Zotero collection **one item at a time** and decide – read it, keep it
or reject it – straight through Zotero's web API. No server and no install: open
<https://ibst1.github.io/zotero-watch-review/>, add it to the home screen, paste a Zotero key. Made because Zotero
for Android can't edit tags.

Useful for any pile of items waiting for a decision: what the Zotero Connector saved this week, papers someone sent
you – or new articles from your own searches and feeds, which the app fetches itself (below). They go in a collection
(by default **To review**), and you go through them.

## Sources: new articles by themselves

In Settings → *Sources*, add searches and feeds; their new items are put in the collection when the app opens (at
most every 6 hours; a new source looks two weeks back), with the source in the item's *Extra*. Nothing already in your
library – or in its trash, so what you rejected doesn't come back – is added again (by DOI, else by title).

- **PubMed search** – any PubMed query, e.g. `wilms tumour[tiab] OR nephroblastoma[tiab]`.
- **Europe PMC search** – PubMed plus preprints (bioRxiv, medRxiv …), e.g. `"wilms tumour" OR nephroblastoma`.
- **Journal, by ISSN** – the journal's new articles, from Crossref (works for nearly every journal).
- **RSS or Atom feed** – PubMed's own feeds work as they are; most journals' feeds don't let a web page read them,
  so use the journal's ISSN instead, or a feed proxy of your own: `feed-proxy/worker.js` is a Cloudflare Worker
  (free) for that – its address with `?url=` goes in Settings.

The sources are kept in a Zotero note (tag `watch-review-sources`), so all your devices share them and know when they
were last read. Nothing is filtered by relevance: you get what the search finds, and decide in the app.

## Each item

You see the title, authors, journal, date and abstract, and:

- **Already in your library** / **related** – the same work (by title), or works by the same first authors that
  you already have (Zotero's quick search).
- **Open PDF** – when OpenAlex knows a free full text for the DOI.
- **✎ Note** – a short note (typed or dictated), saved as a child note of the item in Zotero.

And you choose:

- **Read** – one tap on a reading tag (`to-read` by default; you can have several).
- **Keep** – kept in the library, nothing to read now.
- **Reject** – with a reason (saved as a tag, e.g. `rejected: off topic`), to Zotero's trash (recoverable there).
- **‹ / ›** – back to the one before, on to the next one (they stay).
- **Swipe** the card right to keep it, left to reject it.

Read and Keep take the item out of the collection – and, if so set up, into its parent collection. Every change can
be undone: *Undo* in the message right after, or the undo arrow at the top, as many steps back as you like (this
session).

## Settings (⚙)

- **Zotero API key** – zotero.org → Settings → Security → *Create new private key*, with **Allow library access**
  and **Allow write access**. Kept in this browser only and sent only to `api.zotero.org` (OpenAlex gets only DOIs;
  the sources get only your searches).
- **Setup** – *Simple* (the collection *To review*, no tags needed) or *Partitur* (below), or your own:
  - the collection to go through – every collection with that name is a queue; under a parent collection, the
    parent's first word labels it, and you can filter by it (e.g. *F – Research / To review*, *T – Theology / To
    review*);
  - a queue tag (optional) – then only items with it are shown, and reading or keeping one removes it;
  - the reading tags; where Read and Keep move the item (its parent collection, or just out of the collection);
  - a tag for what you read or keep (optional), the reasons to reject (*Label = tag*) and their tag prefix, and the
    tag on your notes.

## With Partitur

The preset *Partitur* is for the author's own sync setup, Partitur, whose literature watch puts new articles in
`<field> / Bevakning`, tagged `bevakning`, with a note from Claude on why. Its tags are Swedish, because Partitur reads
them: reading or keeping adds `från-bevakning` and moves the item to the field's top collection (where Partitur's
Claude sorts it into a subcollection); a rejection adds `avvisad: <reason>`, which the watch learns from. When
Partitur's notes are there – whatever the setup – the app also shows:

- Claude's note on why the item was picked, and its relevance (*high* before *medium*: the items come most relevant
  first);
- **＋ Project** – put the item in one of the active projects (from Partitur's note tagged `partitur-projekt`); the
  tag `projekt: <vault> – <project>` makes Partitur add it to the project's literature list.

Partitur also keeps a Todoist task *Bevakning: N att gå igenom*, linked here, while there is something to go through.

## How it works

One page, `index.html`, no build step and no server of its own. It reads the collections, the items in them, and the
items' child notes, and changes items with `PATCH` (with Zotero's version check: if the item was changed elsewhere
meanwhile, the change is made again on the item as it is now). `sw.js` keeps the app's own files for offline start;
Zotero's answers are never cached.

Try it without touching a real library: `python tests/mock_zotero.py`, then open
<http://localhost:8765/?api=http://localhost:8765> (any key works; `?api=` alone switches back to Zotero).

## Licence

Copyright (C) 2026 Sebastian Ibstedt. GNU Affero General Public License v3.0 or later (`LICENSE`). Not affiliated
with or endorsed by Zotero, the Corporation for Digital Scholarship or OpenAlex.
