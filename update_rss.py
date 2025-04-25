import feedparser
from datetime import datetime, timezone
from xml.etree.ElementTree import Element, SubElement, ElementTree

# RSS Sources (official + media)
FEEDS = [
    "https://developer.apple.com/news/releases/rss/releases.rss",
    "https://support.google.com/android-developer/rss/policies",
    "https://techcrunch.com/feed/",
    "https://www.theverge.com/rss/index.xml"
]

# Keywords of interest
KEYWORDS = [
    "child safety", "children", "kids", "minor", "age",
    "content moderation", "offensive", "review guidelines",
    "monetization", "billing", "subscriptions", "ads",
    "developer compliance", "policy update", "guidelines",
    "app store", "google play", "trust and safety"
]

def get_relevant_items():
    items = []
    for url in FEEDS:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            title = entry.get("title", "").lower()
            summary = entry.get("summary", "").lower()
            if any(k in title or k in summary for k in KEYWORDS):
                items.append({
                    "title": entry.get("title"),
                    "link": entry.get("link"),
                    "description": summary[:300],
                    "pubDate": entry.get("published", datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S GMT")),
                    "guid": entry.get("id", entry.get("link"))
                })
    return items[:10]

def create_rss(items):
    rss = Element("rss", version="2.0")
    channel = SubElement(rss, "channel")
    SubElement(channel, "title").text = "App Store & Play Store Policy Updates"
    SubElement(channel, "link").text = "https://app-policy-updates.github.io/app-policy-updates/feed.xml"
    SubElement(channel, "description").text = "Auto-curated updates on App Store & Google Play policy changes."
    SubElement(channel, "language").text = "en-us"
    SubElement(channel, "lastBuildDate").text = datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S GMT")

    for item in items:
        itm = SubElement(channel, "item")
        SubElement(itm, "title").text = item["title"]
        SubElement(itm, "link").text = item["link"]
        SubElement(itm, "description").text = item["description"]
        SubElement(itm, "pubDate").text = item["pubDate"]
        SubElement(itm, "guid").text = item["guid"]

    tree = ElementTree(rss)
    tree.write("feed.xml", encoding="utf-8", xml_declaration=True)

if __name__ == "__main__":
    items = get_relevant_items()
    create_rss(items)
