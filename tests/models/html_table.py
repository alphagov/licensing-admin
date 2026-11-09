from bs4 import BeautifulSoup


class HtmlTable:
    def to_json(table_html: str) -> list[dict]:
        table = BeautifulSoup(table_html, "html.parser")

        headers = [th.get_text(strip=True) for th in table.select("thead th")]

        results = []

        for row in table.select("tbody tr"):
            cells = [td.get_text(strip=True) for td in row.select("td")]

            results.append(dict(zip(headers, cells, strict=True)))

        return results
