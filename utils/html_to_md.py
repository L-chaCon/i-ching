import os
from pathlib import Path

from bs4 import BeautifulSoup, element


def format_html(
    html_text: element.Tag | element.NavigableString | BeautifulSoup,
    md_format: list = [],
) -> list:
    # print(f"{html_text.name} -> {str(html_text).split('dasdasda')}")
    # print(f"{html_text.name}: {type(html_text)} -> {str(html_text).split('dasdasda')}")
    if type(html_text) is BeautifulSoup:
        for content in html_text.contents:
            md_format = format_html(content, md_format=md_format)
    if type(html_text) is element.Tag:
        # print(html_text.name)
        if html_text.name == "br":
            md_format.append("\n")
        elif html_text.name == "b":
            for content in html_text.contents:
                md_format = format_html(content, md_format=md_format)
        elif html_text.name == "i":
            format_sting = str(html_text.string).replace("\n", "").strip()
            if format_sting != "":
                md_format.append(f"> {format_sting}")
        elif html_text.name == "h3":
            format_sting = str(html_text.string).replace("\n", "").strip()
            if format_sting != "":
                md_format.append(f"## {format_sting}")

    elif type(html_text) is element.NavigableString:
        format_sting = str(html_text).replace("\n", "").strip()
        if format_sting != "":
            md_format.append(f"{format_sting}")
    return md_format


def html_to_md(html_file: str = "", out_path=Path):
    file_name = out_path.stem
    # h_number = int(file_name.split("_")[0])
    # h_name = file_name.split("_")[1]
    soup = BeautifulSoup(html_file, "html.parser")

    md_content = []
    for h2 in soup.find_all("h2")[2:3]:
        if not h2.string:
            break
        title = h2.string.replace("\n", "").strip()
        md_content.append(f"# {title}")

        next = h2.next_sibling
        html_raw_parts = []
        while next and next.name != "h2":
            html_raw_parts.append(next)
            next = next.next_sibling
        html_raw = "".join([str(element) for element in html_raw_parts])
        soup_raw = BeautifulSoup(html_raw, "html.parser")
        formated_next = format_html(soup_raw, md_format=[])
        formateded_next_str = "".join(formated_next)
        md_content.append(formateded_next_str)

        # md_content_next = []
        # while next and next.name != "h2":
        #     formateded_next = format_html(next, md_format=[])
        #     formateded_next_str = "\n\n".join(formateded_next)
        #     if formateded_next_str != "":
        #         md_content_next.append(formateded_next_str)
        #     # print(f"HTML CONTENT:\n{next}\n")
        #     print(f"Formated Next:\n{formateded_next}\n")
        #     # print(f"MD list:\n{md_content_next}\n")
        #     print("+" * 80)
        #     next = next.next_sibling
        # md_content.append("".join(md_content_next))

    print("\n\n".join(md_content))


def main():
    raw_html_path = Path(f"{Path.cwd().parent}/assets/hexagrams/raw_html")
    out_md_path = Path(f"{Path.cwd().parent}/src")
    for file in raw_html_path.iterdir():
        if file.is_file():
            with open(file, "r") as f:
                html_file = f.read()
            html_to_md(
                html_file=html_file,
                out_path=out_md_path.joinpath(f"{file.stem}.md"),
            )

        # TODO: TAKE THIS BREK OUT
        break


if __name__ == "__main__":
    main()
