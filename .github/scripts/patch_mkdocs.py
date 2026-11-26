import os

import yaml

BRANCH = os.environ.get("BRANCH", "main")
REPO = os.environ.get("REPO_NAME", "book")

MKDOCS_FILE = "mkdocs.yml"
BOOK_DESC_FILE = "docs/book/book-desc.yml"
INDEX_FILE = "docs/index.md"

# -------------------------------
# Load mkdocs.yml
# -------------------------------
with open(MKDOCS_FILE, "r") as f:
    config = yaml.safe_load(f)

# -------------------------------
# 1. Switch extra.css for branches
# -------------------------------
extra_css = config.get("extra_css", [])

if BRANCH != "main":
    extra_css = [
        "stylesheets/extra-branch.css" if css == "stylesheets/extra.css" else css
        for css in extra_css
    ]

config["extra_css"] = extra_css


# -------------------------------
# 2. Build book menus
# -------------------------------
book_links = [
    {"PDF Book": f"download/{REPO}.pdf"},
    {"ePUB Book": f"download/{REPO}.epub"},
]

if BRANCH != "main":
    book_links.append(
        {"DOCX Book (for review only)": f"download/{REPO}.docx"}
    )

# -------------------------------
# 3. Insert menus before "About us"
# -------------------------------
nav = config.get("nav", [])
new_nav = []
inserted = False

for item in nav:
    if isinstance(item, dict) and "About us" in item and not inserted:
        for link in book_links:
            new_nav.append(link)
        inserted = True
    new_nav.append(item)

if not inserted:
    new_nav.extend(book_links)

config["nav"] = new_nav


# -------------------------------
# 4. Book metadata for the landing page (overrides/home.html)
# -------------------------------
def first_book_page(items):
    for item in items:
        value = list(item.values())[0] if isinstance(item, dict) else item
        if isinstance(value, list):
            found = first_book_page(value)
            if found:
                return found
        elif isinstance(value, str) and value.startswith("book/") and value.endswith(".md"):
            return value
    return None


def as_list(value):
    if not value:
        return []
    return value if isinstance(value, list) else [value]


book_meta = {}
if os.path.exists(BOOK_DESC_FILE):
    with open(BOOK_DESC_FILE, "r") as f:
        docs = [d for d in yaml.safe_load_all(f) if d]
        if docs:
            book_meta = docs[0]

portal = book_meta.get("portal") or {}

authors = portal.get("authors")
if not authors:
    authors = [
        {"name": name.strip()}
        for name in str(book_meta.get("author", "")).split(",")
        if name.strip()
    ]
for author in authors:
    author["initials"] = "".join(p[0] for p in author["name"].split()[:2]).upper()

first_page = first_book_page(config["nav"]) or "book/chapter1.md"
read_url = first_page[:-3] + "/" if config.get("use_directory_urls", True) else first_page[:-3] + ".html"

downloads = [
    {"label": "PDF", "url": f"download/{REPO}.pdf"},
    {"label": "ePUB", "url": f"download/{REPO}.epub"},
]
if BRANCH != "main":
    downloads.append({"label": "DOCX", "url": f"download/{REPO}.docx"})

config.setdefault("extra", {})
config["extra"]["book"] = {
    "title": book_meta.get("title", "Untitled book"),
    "subtitle": book_meta.get("subtitle", ""),
    "subject": book_meta.get("subject", ""),
    "keywords": as_list(book_meta.get("keywords")),
    "highlights": as_list(portal.get("highlights")),
    "authors": authors,
    "read_url": read_url,
    "cover": f"download/{REPO}.png",
    "downloads": downloads,
    "catalog_url": "https://networkingdocs.hpe.com/documentation/jnbooks/us/en/day-one-books/",
}

if BRANCH != "main":
    config["extra"]["preview_branch"] = BRANCH

# -------------------------------
# 5. Write back mkdocs.yml
# -------------------------------
with open(MKDOCS_FILE, "w") as f:
    yaml.dump(config, f, sort_keys=False, allow_unicode=True)

print(f"mkdocs.yml patched for branch: {BRANCH}")

# -------------------------------
# 6. Generate docs/index.md
# -------------------------------
# The page layout (hero, authors, formats, versions) lives in
# overrides/home.html; the page body is the book abstract.
abstract = str(portal.get("abstract") or (
    f"This is the digital Day One book **{config['extra']['book']['title']}**. "
    "You will find the book in three versions: Web, PDF and ePUB."
)).strip()

index_md = f"""---
template: home.html
title: {yaml.safe_dump(config['extra']['book']['title'], allow_unicode=True).splitlines()[0]}
hide:
  - navigation
  - toc
  - feedback
---

{abstract}
"""

os.makedirs("docs", exist_ok=True)
with open(INDEX_FILE, "w") as f:
    f.write(index_md)

print(f"docs/index.md generated for branch: {BRANCH}")
