import os
from pathlib import Path

from bs4 import BeautifulSoup, element


def html_to_md(file_name: str = "", html_file=""):
    h_number = int(file_name.split("_")[0])
    h_name = file_name.split("_")[1]
    soup = BeautifulSoup(html_file, "html.parser")

    for h2 in soup.find_all("h2"):
        print(h2.string.split("ss"))


def main():
    raw_html_path = Path(f"{Path.cwd().parent}/assets/hexagrams/raw_html")
    for file in raw_html_path.iterdir():
        if file.is_file():
            file_name = file.stem
            with open(file, "r") as f:
                html_file = f.read()
            html_to_md(file_name=file_name, html_file=html_file)

        # TODO: TAKE THIS BREK OUT
        break


if __name__ == "__main__":
    main()
