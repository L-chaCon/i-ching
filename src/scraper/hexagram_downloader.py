import os
from http import HTTPStatus
from pathlib import Path
from time import sleep

import requests
from bs4 import BeautifulSoup, element
from dotenv import load_dotenv

load_dotenv(f"{Path.cwd().parent}/.env")

IMAGE_WIKI = os.getenv("IMAGE_WIKI", "0")
IMAGE_FROM_HEXAGRAM = os.getenv("IMAGE_FROM_HEXAGRAM", "0")
DOWNLOAD_RAW = os.getenv("DOWNLOAD_RAW", "0")
VERBOSE = os.getenv("VERBOSE", "0")

if IMAGE_WIKI == "0":
    wiki = False
elif IMAGE_WIKI == "1":
    wiki = True
else:
    raise ValueError("IMAGE_WIKI is not a good value")

if IMAGE_FROM_HEXAGRAM == "0":
    img_hex = False
elif IMAGE_FROM_HEXAGRAM == "1":
    img_hex = True
else:
    raise ValueError("IMAGE_FROM_HEXAGRAM is not a good value")

if DOWNLOAD_RAW == "0":
    raw_html = False
elif DOWNLOAD_RAW == "1":
    raw_html = True
else:
    raise ValueError("DOWNLOAD_RAW is not a good value")

if VERBOSE == "0":
    verbose = False
elif VERBOSE == "1":
    verbose = True
else:
    raise ValueError("verbose is not a good value")


def print_report(failed: dict, success: dict):
    report: dict = {}

    for key, value in success.items():
        if value not in report:
            report[value] = []
        report[value].append(key)

    for key, value in failed.items():
        if value not in report:
            report[value] = []
        report[value].append(key)

    for key, value in report.items():
        print(f"{key}: {value}")


def image_download_from_wiki(out: Path, verbose: bool = False):
    """
    This funtion is build to be run from the `utils/` folder
    """
    base_url = "https://en.m.wikipedia.org/wiki/File:Iching-hexagram-{}.png"

    success_hexagrams = {}
    failed_hexagrams = {}

    headers: dict = {
        "user-agent": os.getenv("USERAGENT"),
        "cookie": os.getenv("COOKIE"),
        "accept": os.getenv("ACCEPT"),
    }
    session = requests.Session()
    session.headers.update(headers)

    for i in range(1, 65):
        hexagram_url = base_url.format(str(i).zfill(2))
        r = session.get(hexagram_url)
        if r.status_code == HTTPStatus.OK:
            downlaoded = False
            soup = BeautifulSoup(r.text, "html.parser")
            for img_tag in soup.find_all("img"):
                if "New SVG image" in img_tag.get("alt", []):
                    download_url = f"{img_tag.get("src")}"
                    out_path = f"{out}/{str(i).zfill(2)}.png"
                    try:
                        img_r = session.get(download_url)
                        if img_r.status_code == 200:
                            with open(out_path, "wb") as f:
                                f.write(img_r.content)
                            downlaoded = True
                        else:
                            failed_hexagrams[i] = f"HTTPStatus {img_r.status_code}"
                    except Exception as e:
                        print(e)
                        failed_hexagrams[i] = "Download Failed"

                    if verbose:
                        print(
                            f"Hexagram: {i} - downloaded: {downlaoded} - url: {download_url}"
                        )
                    sleep(0.1)

            if downlaoded:
                success_hexagrams[i] = "Download success"

        else:
            failed_hexagrams[i] = "HTTPStatus error"

    print_report(failed_hexagrams, success_hexagrams)


def download_raw_html(
    hexagram_a_element: element.Tag,
    session: requests.Session,
    download_image: bool = False,
    image_out: Path | str = "",
    raw_html_out: Path | str = "",
    download_raw: bool = False,
) -> str:
    message = []
    base_url = "https://www.iching-online.com"
    text = hexagram_a_element.find("h5").get_text(separator=" ")
    h_number, h_name = int(text.split(" ")[0]), text.split(" ")[1]
    href = hexagram_a_element.get("href")
    r = session.get(f"{base_url}{href}")
    if r.status_code == HTTPStatus.OK:
        soup = BeautifulSoup(r.text, "html.parser")
        # Image Dowload
        if download_image:
            img = soup.find("img")
            image_url = f"{img.get('src').replace("..",base_url)}"
            img_r = session.get(image_url)
            image_out_path = f"{image_out}/{str(h_number).zfill(2)}_{h_name}.png"
            image_out_path_class = Path(image_out_path)
            if image_out_path_class.exists():
                if verbose:
                    print(f"Hexagram: {h_number} - Image already exist")
                message.append("Image already exist")
            else:
                if img_r.status_code == 200:
                    with open(image_out_path, "wb") as f:
                        f.write(img_r.content)
                    if verbose:
                        print(
                            f"Hexagram: {h_number} - Image Downloaded - url: {image_url}"
                        )
                    message.append("Image Downloaded")
                else:
                    if verbose:
                        print(f"Hexagram: {h_number} - Image Error")
                    message.append("Error in geting image")
        # Hexagram data
        main_div = soup.find_all("div", {"class": "txt"})[0]
        for p in main_div.find_all("p"):
            p.unwrap()
        table = main_div.table
        table.decompose()
        raw_path = Path(f"{raw_html_out}/{str(h_number).zfill(2)}_{h_name}.html")
        if download_raw:
            if raw_path.exists():
                if verbose:
                    print(f"Hexagram: {h_number} - Raw HTML already exist")
                message.append("Raw HTML already Exist")
            else:
                if download_raw:
                    # formatter = HTMLFormatter(indent=4)
                    with open(
                        f"{raw_html_out}/{str(h_number).zfill(2)}_{h_name}.html",
                        "wb",
                    ) as f:
                        # f.write(main_div.prettify(formatter=formatter).encode("utf-8"))
                        f.write(main_div.prettify().encode("utf-8"))
                    if verbose:
                        print(
                            f"Hexagram: {h_number} - Raw HTML Downloaded - url: {image_url}"
                        )
                    message.append("Raw HTML Downlaoded")

        if message:
            return " ; ".join(message)
        else:
            return "All options are deactivated, try setting to True"
    else:
        if verbose:
            print(f"Hexagram: {h_number} - Error")
        return "No request found for Hexagram"


def download_hexagram(
    image: bool = False,
    image_out: Path | str = "",
    raw_html_out: Path | str = "",
    download_raw: bool = False,
    verbose: bool = False,
) -> None:
    base_url = "https://www.iching-online.com/hexagrams"

    success_hexagrams: dict = {}
    failed_hexagrams: dict = {}

    headers: dict = {}
    session = requests.Session()
    session.headers.update(headers)

    r = session.get(base_url)
    if verbose:
        print("-" * 80)
        print(r.status_code)
    if r.status_code == HTTPStatus.OK:
        soup = BeautifulSoup(r.text, "html.parser")
        div = soup.find("div", {"class": "mrg"})
        if div is not None:
            table = div.find("table")
        else:
            raise ValueError("<div> was not found in Soup")
        if table is not None:
            for element in table.find_all("center"):
                hexagram = element.find("a")
                if hexagram is not None:
                    text = hexagram.find("h5").get_text(separator=" ")
                    h_number = int(text.split(" ")[0])
                    try:
                        success_message = download_raw_html(
                            hexagram_a_element=hexagram,
                            session=session,
                            download_image=image,
                            image_out=image_out,
                            raw_html_out=raw_html_out,
                            download_raw=download_raw,
                        )
                        success_hexagrams[str(h_number).zfill(2)] = f"{success_message}"
                    except Exception as e:
                        failed_hexagrams[str(h_number).zfill(2)] = (
                            f"Faild to create hexagram - {type(e)}"
                        )
                else:
                    ValueError("<a> was not found in Soup")
        else:
            raise ValueError("<table> was not found in Soup")

    print_report(failed_hexagrams, success_hexagrams)


def main(
    image_wiki: bool = False,
    image_from_hexagram: bool = False,
    download_raw: bool = False,
    verbose: bool = False,
):
    base_folder = Path.cwd()
    image_out_mini = Path(f"{base_folder}/static/images/hexagrams/mini")
    image_out_mini.mkdir(parents=True, exist_ok=True)

    image_out_main = Path(f"{base_folder}/static/images/hexagrams/main")
    image_out_main.mkdir(parents=True, exist_ok=True)

    hexagram_raw_out = Path(f"{base_folder}/.raw_html")
    hexagram_raw_out.mkdir(parents=True, exist_ok=True)

    if verbose:
        print(f"Image Out Mini: {image_out_mini}")
        print(f"Image Out Main: {image_out_main}")
        print(f"Raw HTML Out: {hexagram_raw_out}")

    if image_wiki:
        image_download_from_wiki(out=image_out_mini, verbose=verbose)
    if image_from_hexagram or download_raw:
        download_hexagram(
            image=image_from_hexagram,
            image_out=image_out_main,
            raw_html_out=hexagram_raw_out,
            download_raw=download_raw,
            verbose=verbose,
        )


if __name__ == "__main__":
    main(
        image_wiki=wiki,
        image_from_hexagram=img_hex,
        download_raw=raw_html,
        verbose=verbose,
    )
