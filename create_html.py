#!/usr/bin/env python3
"""Build a single-file HTML page presenting three unlisted YouTube videos
for the University of Sydney postdoc application (position 0158347).
Usage:  python make_application_page.py     ->  writes app.html
No third-party packages needed."""
import html
import re
from pathlib import Path


APPLICANT = "Moe Thiri Zun"
POSITION = "Postdoctoral Research Associate in Carbon-Neutral Demand Forecasting"
EMPLOYER = "The University of Sydney"
POSITION_ID = "0158347"
CONTACT = "moethiri.zun97@gmail.com"         
OUTPUT = "app.html"

EMBED = True

VIDEOS = [
    {
        "url": "https://youtu.be/zXviWyK7QHA",
        "length": "5 min",
        "title": "Introduction and motivation",
        "points": [
            "Academic background and research highlights",
            "Motivation for applying for this position",
            "Career aspirations",
            "Experience in industry collaboration",
            "Experience with AI, with examples of how I used it",
            "Availability to start",
        ],
    },
    {
        "url": "https://youtu.be/DdzRYfqK3os",
        "length": "10 min",
        "title": "Research presentation",
        "points": ["One research problem, presented in academic-conference format"],
    },
    {
        "url": "https://youtu.be/KV6lUoqSMJo",
        "length": "10 min",
        "title": "Industry-partner presentation",
        "points": ["The same research framed for an industry audience: how it supports their business"],
    },
]
# -----------------------------------------------------------------------------

ID_RE = re.compile(r"(?:youtu\.be/|v=|embed/|shorts/)([A-Za-z0-9_-]{11})")


SCRIPT = """<script>
// YouTube refuses embeds on file:// pages (error 153). Over http(s) the player
// loads in place; from a local file the click opens the video on YouTube instead.
document.querySelectorAll(".player").forEach(function (box) {
  box.addEventListener("click", function () {
    var id = box.dataset.vid;
    if (location.protocol !== "http:" && location.protocol !== "https:") {
      window.open("https://www.youtube.com/watch?v=" + id, "_blank", "noopener");
      return;
    }
    var f = document.createElement("iframe");
    f.src = "https://www.youtube.com/embed/" + id + "?rel=0&playsinline=1&autoplay=1";
    f.title = box.dataset.title;
    f.allow = "accelerometer; autoplay; encrypted-media; picture-in-picture; fullscreen";
    f.referrerPolicy = "strict-origin-when-cross-origin";
    f.allowFullscreen = true;
    box.innerHTML = "";
    box.appendChild(f);
  });
});
</script>"""


def video_id(url: str) -> str:
    m = ID_RE.search(url)
    if not m:
        raise ValueError(f"Cannot find a YouTube video ID in: {url}")
    return m.group(1)


def card(n: int, v: dict) -> str:
    vid = video_id(v["url"])
    e = html.escape
    points = "".join(f"<li>{e(p)}</li>" for p in v["points"])
    if EMBED:
        opener = f'<button type="button" class="play" aria-label="Play: {e(v["title"])}">'
        closer = "</button>"
    else:
        opener = (f'<a class="play" href="https://www.youtube.com/watch?v={vid}" '
                  f'target="_blank" rel="noopener" aria-label="Watch on YouTube: {e(v["title"])}">')
        closer = "</a>"
    return f"""
    <article class="card">
      <div class="meta"><span class="num">{n}</span><span class="len">{e(v['length'])}</span></div>
      <h2>{e(v['title'])}</h2>
      <div class="player" data-vid="{vid}" data-title="{e(v['title'])}">
        {opener}
          <img src="https://img.youtube.com/vi/{vid}/hqdefault.jpg" alt="" loading="lazy"
               onerror="this.style.display='none'">
          <span class="tri"></span>
        {closer}
      </div>
      <ul>{points}</ul>
      <a class="yt" href="https://www.youtube.com/watch?v={vid}" target="_blank" rel="noopener">Watch on YouTube &#8599;</a>
    </article>"""


def build() -> str:
    e = html.escape
    cards = "".join(card(i, v) for i, v in enumerate(VIDEOS, 1))
    script = SCRIPT if EMBED else ""
    contact = f'<p class="contact">{e(CONTACT)}</p>' if CONTACT else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>{e(APPLICANT)} – Video presentations – Position {e(POSITION_ID)}</title>
<style>
  :root {{ --bg:#f6f7f9; --card:#fff; --ink:#1b1f24; --mute:#5b6570; --acc:#0b5cab; --line:#e1e5ea; }}
  @media (prefers-color-scheme: dark) {{
    :root {{ --bg:#14171b; --card:#1d2227; --ink:#eef1f4; --mute:#9aa5b1; --acc:#6fb0f2; --line:#2c333a; }}
  }}
  * {{ box-sizing:border-box; }}
  body {{ margin:0; background:var(--bg); color:var(--ink);
         font:16px/1.55 system-ui,-apple-system,"Segoe UI",Roboto,"Hiragino Sans",sans-serif; }}
  main {{ max-width:960px; margin:0 auto; padding:40px 20px 64px; }}
  header h1 {{ margin:0 0 4px; font-size:28px; }}
  header p {{ margin:2px 0; color:var(--mute); }}
  .contact {{ color:var(--ink); }}
  .grid {{ display:grid; gap:24px; margin-top:32px; }}
  .card {{ background:var(--card); border:1px solid var(--line); border-radius:12px; padding:20px; }}
  .card h2 {{ margin:6px 0 12px; font-size:20px; }}
  .meta {{ display:flex; gap:10px; align-items:center; font-size:13px; color:var(--mute); }}
  .num {{ background:var(--acc); color:#fff; border-radius:50%; width:24px; height:24px;
          display:inline-grid; place-items:center; font-weight:700; }}
  .player {{ position:relative; aspect-ratio:16/9; background:#000; border-radius:8px; overflow:hidden; }}
  .player iframe, .player .play {{ position:absolute; inset:0; width:100%; height:100%; border:0; }}
  .play {{ display:block; padding:0; background:#000; cursor:pointer; }}
  .play img {{ width:100%; height:100%; object-fit:cover; display:block; }}
  .tri {{ position:absolute; left:50%; top:50%; width:68px; height:48px; transform:translate(-50%,-50%);
          background:#e62117; border-radius:12px; }}
  .tri::after {{ content:""; position:absolute; left:27px; top:14px; border-style:solid;
                 border-width:10px 0 10px 18px; border-color:transparent transparent transparent #fff; }}
  .play:hover .tri {{ background:#ff0000; }}
  ul {{ margin:14px 0 8px; padding-left:20px; color:var(--mute); }}
  .yt {{ color:var(--acc); text-decoration:none; font-size:14px; }}
  .yt:hover {{ text-decoration:underline; }}
  footer {{ margin-top:32px; font-size:13px; color:var(--mute); }}
</style>
</head>
<body>
<main>
  <header>
    <h1>{e(APPLICANT)}</h1>
    <p>Application for {e(POSITION)}</p>
    <p>{e(EMPLOYER)} &middot; Position {e(POSITION_ID)}</p>
    {contact}
  </header>
  <section class="grid">{cards}
  </section>
  <footer>Videos are unlisted on YouTube and shared only for this application. Click a video to watch it on YouTube.</footer>
</main>
{script}
</body>
</html>
"""


if __name__ == "__main__":
    Path(OUTPUT).write_text(build(), encoding="utf-8")
    print(f"Wrote {OUTPUT} ({len(VIDEOS)} videos)")