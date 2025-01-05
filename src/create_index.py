from pathlib import Path

OUT_PATH = Path(f"{Path.cwd().parent}/content/index.md")
IN_PATH = Path(f"{Path.cwd().parent}/content")


def create_hex_table(hexagrams: list) -> str:
    result: list = []
    for hex in hexagrams:
        h_name = hex.split("_")[1]
        h_number = int(hex.split("_")[0])
        result.append(f"{h_number}. [{h_name}](/hexagrams/{hex}.html)")
    return "\n".join(result)


def create_tri_table(triagrams: list) -> str:
    return ""


def create_form() -> str:
    return ""
    # TODO: AGREGAR EL FORM EN FORMATO MD
    # return "<form>here is the form format</form>"


def create_intro() -> str:
    result = []
    result.append("# I Ching")
    result.append(
        "This is a static website for personal use and information about the I ching readding.\nIs not complete, and needs some functionalities but all the information is there"
    )
    result.append(create_form())
    return "\n\n".join(result)


def create_index(out_path: Path, source_path: Path):
    result = []
    tri: list = []
    hex: list = []
    for folder in source_path.iterdir():
        if folder.is_dir():
            for file in folder.iterdir():
                if file.parent.stem == "hexagrams":
                    hex.append(file.stem)
                elif file.parent.stem == "triagramas":
                    tri.append(file.stem)

    result.append(create_intro())
    result.append("## Hexagramas")
    hex.sort()
    result.append(create_hex_table(hex))
    result.append("## Triagrams")
    result.append(create_tri_table(tri))

    with open(out_path, "w") as f:
        f.write("\n\n".join(result))


if __name__ == "__main__":
    create_index(OUT_PATH, IN_PATH)
