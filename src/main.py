import logging
import os
import shutil

from markdown import extract_title, markdown_to_html_node

SOURCE_PATH = os.getenv("SOURCE_PATH", "static")
CONTENT_PATH = os.getenv("CONTENT_PATH", "content")

logger = logging.getLogger(__name__)


def main():
    logging.basicConfig(filename=".log", level=logging.INFO)
    logger.info("Starting")
    clean_files_in_public()
    copy_content_from_source()
    generate_pages_recursive(CONTENT_PATH, "template.html", "public")
    logger.info("Finished")


def clean_files_in_public(verbose=True) -> None:
    if not os.path.exists("public"):
        os.makedirs("public")

    shutil.rmtree("public")
    if verbose:
        print("public has been delated")
    logger.info("public has been delated")
    os.makedirs("public")
    if verbose:
        print("public has been created")
    logger.info("public has been created")


def copy_content_from_source(source_folder=SOURCE_PATH, verbose=True) -> None:
    if not os.path.exists(source_folder):
        logger.error("no folder in source path")
        raise OSError("no folder in source path")

    def recursion_copy(path, verbose=verbose):
        if os.path.isfile(path):
            des_path = path.replace(source_folder, "public")
            shutil.copy(path, des_path)
            logger.info(f"{des_path} has been created")
            if verbose:
                print(f"{des_path} has been created")
            return
        files = os.listdir(path)
        for file in files:
            src_path = os.path.join(path, file)
            des_path = os.path.join(path.replace(source_folder, "public"), file)
            if os.path.isdir(src_path):
                if not os.path.exists(des_path):
                    os.mkdir(des_path)
                    logger.info(f"{des_path} has been created")
                    if verbose:
                        print(f"{des_path} has been created")
            recursion_copy(src_path)

    recursion_copy(source_folder)


def generate_page(
    from_path: str, template_path: str, dest_path: str, verbose=True
) -> None:
    logger.info(
        f"Generating page from {from_path} to {dest_path} using {template_path}"
    )
    if verbose:
        print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, encoding="utf-8") as f:
        markdown_content = f.read()

    with open(template_path, encoding="utf-8") as f:
        template = f.read()

    title = extract_title(markdown_content)
    content = markdown_to_html_node(markdown_content).to_html()
    folders = os.path.dirname(dest_path)
    if not os.path.exists(folders):
        os.makedirs(folders)
    html_content = template.replace("{{ Title }}", title).replace(
        "{{ Content }}", content
    )
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    f.close()
    logger.info(f"{dest_path} Created")
    if verbose:
        print(f"{dest_path} Created")


def generate_pages_recursive(
    dir_path_content: str, template_path: str, dest_dir_path: str, verbose=True
) -> None:
    if not os.path.exists(dir_path_content):
        logger.error("no folder in source path")
        raise OSError("no folder in source path")

    def recursion_copy(path, verbose=verbose):
        if os.path.isfile(path):
            des_path = path.replace(dir_path_content, dest_dir_path)
            path_no_extencion = des_path.split(".")[:-1]
            path_no_extencion.append("html")
            html_path = ".".join(path_no_extencion)
            generate_page(path, template_path, html_path)
            return
        files = os.listdir(path)
        for file in files:
            src_path = os.path.join(path, file)
            recursion_copy(src_path)

    recursion_copy(dir_path_content)


if __name__ == "__main__":
    main()
