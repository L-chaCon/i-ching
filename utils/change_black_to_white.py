import os
from pathlib import Path

from PIL import Image

out = Path("{}/assets/hexagrams/white".format(Path.cwd().parent))
out.mkdir(parents=True, exist_ok=True)

in_path = Path("{}/assets/hexagrams".format(Path.cwd().parent))


def change_black_to_white(in_path, out_path):
    image = Image.open(in_path).convert("RGBA")
    data = image.getdata()

    new_data = []

    for pixel in data:
        if pixel[3] > 0:
            new_data.append((225, 225, 225, pixel[3]))
        else:
            new_data.append(pixel)

    image.putdata(new_data)
    image.save(out_path)


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


def main():
    """
    This funtion was created to run from utils/
    """
    success_hexagrams = {}
    failed_hexagrams = {}

    list_files = os.listdir(in_path)
    for file in list_files:
        extension = file.split(".")[-1]
        if extension == "png":
            out_file = "{}/{}".format(out, file)
            in_file = "{}/{}".format(in_path, file)
            try:
                change_black_to_white(in_file, out_file)
                success_hexagrams[file] = "Por el Poder de la Luna!!"
            except Exception:
                failed_hexagrams[file] = "Not able to Transform"

    print_report(failed_hexagrams, success_hexagrams)


if __name__ == "__main__":
    main()
