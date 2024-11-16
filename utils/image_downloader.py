import os
from http import HTTPStatus
from pathlib import Path
from time import sleep

# TODO: REVISAR EL PROBLEMA CON EL IMPORT Y NVIM
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

out = Path("{}/assets/hexagrams".format(Path.cwd().parent))
out.mkdir(parents=True, exist_ok=True)
base_url = "https://en.m.wikipedia.org/wiki/File:Iching-hexagram-{}.png"

load_dotenv("{}/.env".format(Path.cwd().parent))

headers = {
    "user-agent": os.getenv("USERAGENT"),
    "cookie": os.getenv("COOKIE"),
    "accept": os.getenv("ACCEPT"),
}


def print_report(failed, success):
    report = {}

    for key, value in success.items():
        if value not in report:
            report[value] = []
        report[value].append(key)

    for key, value in failed.items():
        if value not in report:
            report[value] = []
        report[value].append(key)

    for key, value in report.items():
        print("{}: {}".format(key, value))


def main(verbose=False):
    """
    This funtion is build to be run from the `utils/` folder
    """
    success_hexagrams = {}
    failed_hexagrams = {}

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
                    download_url = "{}".format(img_tag.get("src"))
                    out_path = "{}/{}.png".format(out, str(i).zfill(2))
                    try:
                        img_r = session.get(download_url)
                        if img_r.status_code == 200:
                            with open(out_path, "wb") as f:
                                f.write(img_r.content)
                            downlaoded = True
                        else:
                            failed_hexagrams[i] = "HTTPStatus {}".format(
                                img_r.status_code
                            )
                    except Exception as e:
                        print(e)
                        failed_hexagrams[i] = "Download Failed"

                    if verbose:
                        print(
                            "Hexagram: {} - downloaded: {} - url: {}".format(
                                i, downlaoded, download_url
                            )
                        )
                    sleep(0.1)

            if downlaoded:
                success_hexagrams[i] = "Download success"

        else:
            failed_hexagrams[i] = "HTTPStatus error"

    print_report(failed_hexagrams, success_hexagrams)


if __name__ == "__main__":
    main()
