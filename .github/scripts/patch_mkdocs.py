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
# 0. Switch extra.css for branches
# -------------------------------
extra_css = config.get("extra_css", [])

if BRANCH != "main":
    extra_css = [
        "stylesheets/extra-branch.css" if css == "stylesheets/extra.css" else css
        for css in extra_css
    ]
    
config["extra_css"] = extra_css

# -------------------------------
# 1. site_dir logic
# -------------------------------
if BRANCH != "main":
    config["site_dir"] = BRANCH
else:
    config.pop("site_dir", None)

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
# 4. Write back mkdocs.yml
# -------------------------------
with open(MKDOCS_FILE, "w") as f:
    yaml.dump(config, f, sort_keys=False)

print(f"mkdocs.yml patched for branch: {BRANCH}")

# -------------------------------
# 5. Generate docs/index.md
# -------------------------------
# Load book description YAML
book_title = book_subtitle = book_author = "Unknown"
if os.path.exists(BOOK_DESC_FILE):
    with open(BOOK_DESC_FILE, "r") as f:
        all_docs = list(yaml.safe_load_all(f))
        if len(all_docs) > 0:
            # Take first document (adjust if needed)
            book_meta = all_docs[0]
            book_title = book_meta.get("title", book_title)
            book_subtitle = book_meta.get("subtitle", book_subtitle)
            book_author = book_meta.get("author", book_author)

# Prepare WARNING message
if BRANCH == "main":
    warning_md = ""
else:
    warning_md = (
        '<p align="center">'
        '<i class="fa-solid fa-triangle-exclamation" style="color:red; font-size:1.2em;"></i> '
        f'<strong>THIS IS A WORK-IN-PROGRESS BOOK - BRANCH {BRANCH}</strong>'
        '</p>\n'
    )

# Markdown template
index_md = f"""# {book_title} - Dayone Book
{warning_md}
<p align="center">
  <a href="https://juniper.net">
    <img class="my-icon" src="images/jnpr_logo.png?sanitize=true" alt="logo"/>
  </a>
</p>
## About the content

This is the digital Dayone book repository of: **{book_title} - {book_subtitle}**

By {book_author}

You will find the book in three versions: Web, PDF and ePUB.

Enjoy reading!

## Legal disclaimer

*Juniper Networks may disclose information related to development and plans for future products, features or enhancements, known as a Plan of Record (“POR”).  These details provided are based on Juniper’s current development efforts and plans. These development efforts and plans are subject to change at Juniper’s sole discretion, without notice.  Except as may be set forth in definitive agreements, Juniper Networks provides no assurances and assumes no responsibility to introduce products, features or enhancements described in this presentation.  Purchasing decisions by third-parties should not be based on this POR and no purchases are contingent upon Juniper Networks delivering any feature or functionality depicted in this presentation.*
"""

# Ensure docs directory exists
os.makedirs("docs", exist_ok=True)

# Write index.md
with open(INDEX_FILE, "w") as f:
    f.write(index_md)

print(f"docs/index.md generated for branch: {BRANCH}")