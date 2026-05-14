import re
from mkdocs.plugins import BasePlugin
from bs4 import BeautifulSoup

FIGURE_RE = re.compile(r'!\[(.*?)\]\((.*?)\)')
TABLE_PREFIX_RE = re.compile(r'^\s*Table:\s*(.+)$', re.IGNORECASE | re.MULTILINE)


class CaptionPerBookPlugin(BasePlugin):
    """Continuous figure/table numbering for the book, respecting nav order."""

    def on_nav(self, nav, config, files):
        """Collect book pages in nav order and precompute per-page figure/table start offsets."""
        self.pages = []
        self.book_pages = set()

        def count_figures_tables(md_file):
            try:
                with open(md_file, "r", encoding="utf-8") as f:
                    content = f.read()
            except Exception:
                return 0, 0
            return len(FIGURE_RE.findall(content)), len(TABLE_PREFIX_RE.findall(content))

        def collect(item):
            if getattr(item, "file", None):
                src_uri = item.file.src_uri
                if src_uri.startswith("book/"):
                    num_fig, num_tab = count_figures_tables(item.file.abs_src_path)
                    self.pages.append({
                        "src_uri": src_uri,
                        "num_fig": num_fig,
                        "num_tab": num_tab,
                    })
                    self.book_pages.add(src_uri)
            for child in getattr(item, "children", []) or []:
                collect(child)

        for item in nav or []:
            collect(item)

        # Precompute cumulative start offsets
        fig_offset = 0
        tab_offset = 0
        for page_info in self.pages:
            page_info["start_figure"] = fig_offset
            page_info["start_table"] = tab_offset
            fig_offset += page_info["num_fig"]
            tab_offset += page_info["num_tab"]

        return nav

    def on_page_content(self, html, page, config, files):
        """Add figure/table captions with continuous numbering."""
        src_uri = getattr(page.file, "src_uri", None)
        if not src_uri or src_uri not in self.book_pages:
            return html

        # Find starting counters for this page
        start_fig = 0
        start_tab = 0
        for page_info in self.pages:
            if page_info["src_uri"] == src_uri:
                start_fig = page_info["start_figure"]
                start_tab = page_info["start_table"]
                break

        soup = BeautifulSoup(html, "html.parser")

        # Figures
        fig_num = start_fig
        for img in soup.find_all("img"):
            fig_num += 1
            alt = img.get("alt", "")
            figure = soup.new_tag("figure")
            img.replace_with(figure)
            figure.append(img)
            figcaption = soup.new_tag("figcaption")
            figcaption.string = f"Figure {fig_num}: {alt}"
            figure.append(figcaption)

        # Tables
        tab_num = start_tab
        for table in soup.find_all("table"):
            caption_text = None
            prev = table.find_previous_sibling("p")
            if prev:
                match = TABLE_PREFIX_RE.match(prev.get_text(strip=True))
                if match:
                    caption_text = match.group(1).strip()
                    prev.decompose()
            if caption_text:
                tab_num += 1
                caption_tag = soup.new_tag(
                    "p",
                    **{"class": "table-caption", "style": "text-align:center; font-style:italic;"}
                )
                caption_tag.string = f"Table {tab_num}: {caption_text}"
                table.insert_after(caption_tag)

        return str(soup)