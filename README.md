# The Sample DayOne Book

## 📚 New Day One Book as a Code

HPE Networking is introducing a new version of the **Day One Book** platform relying on the Doc As A Code frameworks. It offers online technical books dedicated to networking. This book is available both online, in PDF format and ePub, providing in-depth insights into HPE Networking technologies and best practices. The book will be continuously updated to reflect the latest advancements, ensuring that readers always have access to the most current information.

---

---

## 🧩 Customizing the book portal

The landing page (hero, abstract, authors) is generated from
[`docs/book/book-desc.yml`](docs/book/book-desc.yml). Besides the Pandoc fields (`title`,
`subtitle`, `author`, `date`, `subject`, `keywords`), fill in the `portal:` block:

| Key | Content |
|-----|---------|
| `abstract` | Book abstract (Markdown) |
| `highlights` | Bullet list for "What you will learn" |
| `authors` | `name`, `role`, `bio` of each author |

The look follows the [HPE design system colors](https://design-system.hpe.design/foundation/color):
styles are in [`docs/stylesheets/extra.css`](docs/stylesheets/extra.css) and the page layouts in
[`overrides/`](overrides/). Branch builds add a "Preview" banner and an orange accent.

### Preview locally

Run this from a scratch copy, because `patch_mkdocs.py` rewrites `mkdocs.yml` and creates `docs/index.md`:

```bash
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt && pip install .
BRANCH=main REPO_NAME=ebooks python3 .github/scripts/patch_mkdocs.py
mkdocs serve
```

## 💬 Feedback & Support

Got a question, found a bug, or have suggestions?  

Feel free to share your ideas, feedback, or requests for additional information. To do so, please open a GitHub issue.
You may also reach out at the authors — we’re always happy to help or hear your feedback.

Thanks for contributing to HPE Networking's growing knowledge base.  

**Enjoy reading & learning!**

## Legal disclaimer 

*HPE Networking may disclose information related to development and plans for future products, features or enhancements, known as a Plan of Record (“POR”).  These details provided are based on HPE Networking’s current development efforts and plans. These development efforts and plans are subject to change at HPE Networking’s sole discretion, without notice.  Except as may be set forth in definitive agreements, HPE Networking provides no assurances and assumes no responsibility to introduce products, features or enhancements described in this presentation.  Purchasing decisions by third-parties should not be based on this POR and no purchases are contingent upon HPE Networking delivering any feature or functionality depicted in this presentation.*