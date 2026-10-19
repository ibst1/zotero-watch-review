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

## Cards or a list

On the phone the items come one at a time, as cards. On a big screen (and whenever you switch with the button at the
top) they come as a **list**: title, relevance, Claude's reason and the abstract (folded) for each, with its own Read,
Keep and Reject – or tick several and read, keep or reject them together (one Undo takes them all back). *Card* opens
an item as a card, with everything below.

## Each item

You see the title, authors, journal, date and abstract, and:

- **Already in your library** / **related** – the same work (by title), or works by the same first authors that
  you already have (Zotero's quick search).
- **Open PDF** – when OpenAlex knows a free full text for the DOI.
- **Full text via library** – if you give your library's proxy address in Settings (EZproxy and the like, e.g.
  `https://ludwig.lub.lu.se/login?qurl=%u`): the publisher's page through your library's subscriptions.
- **✎ Note** – a short note (typed or dictated), saved as a child note of the item in Zotero.

And you choose:

- **Read** – one tap on a reading tag (`to-read` by default; you can have several). If you want, pick a date first –
  today, tomorrow, in a week or any day – saved as the tag `due: <date>` (a tool making reading tasks can use it).
- **Keep** – kept in the library, nothing to read now.
- **Reject** – with a reason (saved as a tag, e.g. `rejected: off topic`), to Zotero's trash (recoverable there).
- **‹ / ›** – back to the one before, on to the next one (they stay).
- **Swipe** the card right to keep it, left to reject it.

Read and Keep take the item out of the collection – into its parent collection, if it has one – and tag it with where
it came from (`from: To review`); Reject puts it in Zotero's trash, tagged `rejected: <reason>`. These tags are the same
for everyone, so a tool that fills the collection can learn from them. Every change can be undone: *Undo* in the
message right after, or the undo arrow at the top, as many steps back as you like (this session).

## Settings (⚙)

- **Zotero API key** – zotero.org → Settings → Security → *Create new private key*, with **Allow library access**
  and **Allow write access**. Kept in this browser only and sent only to `api.zotero.org` (OpenAlex gets only DOIs;
  the sources get only your searches).
- **Collection to go through** – *To review* unless you name another. Every collection with that name is a queue;
  under a parent collection, the parent's first word labels it and you can filter by it (e.g. *F – Research / To
  review* and *T – Theology / To review*).
- **Reading tags** – the tags Read offers (`to-read` unless you name others).
- **Library link for full text** – your library's proxy address with `%u` where the article's address goes.
- **Sources** and a **feed proxy** – above.

## With other tools

Anything can put items in the collection – the app only goes through what is there. A tool that does (a literature
watch, an alert service) can also write a child note on an item, tagged `claude-bevakning`, saying why it was picked
("Relevans: hög/medel" orders the queue, most relevant first), and keep a list of projects in a note tagged
`partitur-projekt`: then the app shows the reason and the relevance, and **＋ Project** puts an item in a project
with the tag `projekt: <project>`. The author's own setup, Partitur, does this with Claude: it screens new literature
into `<field> / Bevakning`, learns from what you read, keep and reject, adds what you put in a project to that
project's literature list, and keeps a Todoist task *Bevakning: N att gå igenom*, linked here, while there is something
to go through.

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
