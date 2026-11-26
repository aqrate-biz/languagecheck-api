"""Build an RSS feed from the versioned sections of docs/changelog.md."""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from email.utils import format_datetime
from pathlib import Path
from xml.sax.saxutils import escape

import markdown
from markdown.extensions.toc import slugify

log = logging.getLogger("mkdocs.hooks.changelog_feed")

VERSION_HEADING = re.compile(r"^(\d+\.\d+\.\d+) - (\d{4}-\d{2}-\d{2})$")
SKIP_HEADINGS = {"Unreleased", "Versioning Policy"}
SECTION_SPLIT = re.compile(r"^## ", re.MULTILINE)


@dataclass(frozen=True)
class Release:
    version: str
    published: datetime
    body_markdown: str

    @property
    def heading(self) -> str:
        day = self.published.date().isoformat()
        return f"{self.version} - {day}"

    @property
    def slug(self) -> str:
        return slugify(self.heading, "-")


def on_post_build(config, **kwargs) -> None:
    changelog = Path(config.docs_dir) / "changelog.md"
    releases = parse_releases(changelog.read_text(encoding="utf-8"))
    if not releases:
        raise RuntimeError(f"No releases found in {changelog}")

    site_url = (config.site_url or "").rstrip("/")
    if not site_url:
        raise RuntimeError("site_url is required to build the changelog RSS feed")

    destination = Path(config.site_dir) / "changelog" / "feed.xml"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(render_feed(releases, site_url), encoding="utf-8")
    log.info("Wrote changelog RSS feed to %s", destination)


def parse_releases(text: str) -> list[Release]:
    releases: list[Release] = []
    for part in SECTION_SPLIT.split(text)[1:]:
        lines = part.splitlines()
        heading = lines[0].strip()
        if heading in SKIP_HEADINGS:
            continue
        match = VERSION_HEADING.fullmatch(heading)
        if match is None:
            raise RuntimeError(f"Unrecognized changelog heading: {heading!r}")
        published = datetime.strptime(match.group(2), "%Y-%m-%d").replace(tzinfo=timezone.utc)
        releases.append(
            Release(
                version=match.group(1),
                published=published,
                body_markdown="\n".join(lines[1:]).strip(),
            )
        )
    return releases


def render_feed(releases: list[Release], site_url: str) -> str:
    page_url = f"{site_url}/changelog/"
    feed_url = f"{site_url}/changelog/feed.xml"
    items = "\n".join(render_item(release, page_url) for release in releases)
    last_build = format_datetime(releases[0].published)
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>LanguageCheck API changelog</title>
    <link>{escape(page_url)}</link>
    <description>Notable changes to the LanguageCheck API and documentation.</description>
    <language>en</language>
    <lastBuildDate>{last_build}</lastBuildDate>
    <atom:link href="{escape(feed_url)}" rel="self" type="application/rss+xml"/>
{items}
  </channel>
</rss>
"""


def render_item(release: Release, page_url: str) -> str:
    link = f"{page_url}#{release.slug}"
    description = markdown.markdown(release.body_markdown)
    return f"""    <item>
      <title>{escape(release.version)}</title>
      <link>{escape(link)}</link>
      <guid isPermaLink="true">{escape(link)}</guid>
      <pubDate>{format_datetime(release.published)}</pubDate>
      <description><![CDATA[{escape_cdata(description)}]]></description>
    </item>"""


def escape_cdata(value: str) -> str:
    return value.replace("]]>", "]]]]><![CDATA[>")
