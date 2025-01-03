from pathlib import Path

from bs4 import BeautifulSoup, element


def format_html(
    html_text: element.Tag | element.NavigableString | BeautifulSoup,
    md_format: list = [],
) -> list[tuple]:
    # print(f"{html_text.name} -> {str(html_text).split('dasdasda')}")
    # print(f"{html_text.name}: {type(html_text)} -> {str(html_text).split('dasdasda')}")
    if type(html_text) is BeautifulSoup:
        for content in html_text.contents:
            md_format = format_html(content, md_format=md_format)
    if type(html_text) is element.Tag:
        # print(html_text.name)
        if html_text.name == "br" or html_text.name == "hr":
            md_format.append(("line_break", "\n"))
        elif html_text.name == "b" or html_text.name == "center":
            for content in html_text.contents:
                md_format = format_html(content, md_format=md_format)
        elif html_text.name == "i":
            format_sting = str(html_text.string).replace("\n", "").strip()
            if format_sting != "":
                md_format.append(("tag", f"> {format_sting}"))
        elif html_text.name == "h3":
            format_sting = str(html_text.string).replace("\n", "").strip()
            if format_sting != "":
                md_format.append(("tag", f"## {format_sting}"))
        elif html_text.name == "a":
            print(html_text.contents)
        else:
            print(f"{html_text.name} not suported")

    elif type(html_text) is element.NavigableString:
        format_sting = str(html_text).replace("\n", "").strip()
        if format_sting != "":
            md_format.append(("text", f"{format_sting}"))
    return md_format


def flatten_formated(formated_html: list[tuple]) -> list[str]:
    result = []
    prev_type = None
    for i, (curr_type, curr_content) in enumerate(formated_html):
        if prev_type is None:
            result.append(curr_content)
            prev_type = curr_type
        else:
            if curr_type == "tag":
                if prev_type == "tag":
                    result.append(curr_content)
                    prev_type = curr_type
                elif prev_type == "text":
                    result.append(curr_content)
                    prev_type = curr_type
                if prev_type == "line_break":
                    result.append(curr_content)
                    prev_type = curr_type
            if curr_type == "text":
                if prev_type == "tag":
                    result.append(curr_content)
                    prev_type = curr_type
                elif prev_type == "text":
                    result[-1] = f"{result[-1]}\n{curr_content}"
                    prev_type = curr_type
                elif prev_type == "line_break":
                    result[-1] = f"{result[-1]}\n{curr_content}"
                    prev_type = curr_type
            if curr_type == "line_break":
                if prev_type == "tag":
                    prev_type = curr_type
                elif prev_type == "text":
                    # result[-1] = f"{result[-1]}{curr_content}"
                    prev_type = curr_type
                elif prev_type == "line_break":
                    prev_type = curr_type
    return result


def html_to_md(html_file: str, out_path: Path, verbose: bool = False):
    file_name = out_path.stem
    soup = BeautifulSoup(html_file, "html.parser")

    md_content = []
    for h2 in soup.find_all("h2"):
        md_context_h2 = []
        if not h2.string:
            break
        title = h2.string.replace("\n", "").strip()
        md_context_h2.append(f"# {title}")

        next = h2.next_sibling
        html_raw_parts = []
        while next and next.name != "h2":
            html_raw_parts.append(next)
            next = next.next_sibling
        html_raw = "".join([str(element) for element in html_raw_parts])
        soup_raw = BeautifulSoup(html_raw, "html.parser")
        formated_next = format_html(soup_raw, md_format=[])
        flat_next = flatten_formated(formated_next)
        md_context_h2.extend(flat_next)
        md_content.append("\n\n".join(md_context_h2))
        if verbose:
            print(f"HTML CONTENT:\n{next}\n")
            print(f"Formated Next:\n{formated_next}\n")
            print(f"Flat nex:\n{flat_next}\n")
            print(f"MD list:\n{md_content}\n")
            print("+" * 80)

    with open(out_path, "w") as f:
        f.write("\n\n".join(md_content))


def main(verbose: bool = False):
    base_folder = Path(f"{Path.cwd().parent}").parent  # FIX: THIS IS HARD CODED
    raw_html_path = Path(f"{base_folder}/static/hexagrams/raw_html")
    out_md_path = Path(f"{base_folder}/content/hexagrams")
    for file in raw_html_path.iterdir():
        try:
            if file.is_file():
                with open(file, "r") as f:
                    html_file = f.read()
                html_to_md(
                    html_file=html_file,
                    out_path=out_md_path.joinpath(f"{file.stem}.md"),
                    verbose=verbose,
                )
            print(f"{file.stem} -> html to md compleated")
        except Exception as e:
            print(f"{file.stem} -> error: {e}")
        break


if __name__ == "__main__":
    main(verbose=False)
