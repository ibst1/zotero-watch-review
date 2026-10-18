// SPDX-License-Identifier: AGPL-3.0-or-later
// Watch Review – a feed proxy of your own, as a Cloudflare Worker (free): most journals' RSS feeds don't let a web
// page read them, this does. Deploy it (dash.cloudflare.com → Workers → Create → paste this), then put
// https://<name>.<you>.workers.dev/?url= in Watch Review's settings as the feed proxy. It passes on feeds only.
export default {
  async fetch(request) {
    const url = new URL(request.url).searchParams.get("url");
    if (request.method !== "GET" || !url || !/^https?:\/\//.test(url)) return new Response("?url=<feed address>", { status: 400 });
    const res = await fetch(url, { headers: { "User-Agent": "Watch Review feed proxy", Accept: "application/rss+xml, application/atom+xml, application/xml, text/xml" } });
    const type = res.headers.get("Content-Type") || "";
    if (!/xml|rss|atom/i.test(type)) return new Response("not a feed", { status: 415 });
    return new Response(res.body, { status: res.status, headers: { "Content-Type": type, "Access-Control-Allow-Origin": "*",
                                                                   "Cache-Control": "max-age=900" } });
  },
};
