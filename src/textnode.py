import re

from htmlnode import LeafNode, ParentNode

text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"

markdown_type_map = {
    "**": text_type_bold,
    "*": text_type_italic,
    "`": text_type_code,
}


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __repr__(self):
        return f"<TextNode {self.text} {self.text_type} {self.url}>"

    def __eq__(self, text_node):
        if (
            self.text == text_node.text
            and self.text_type == text_node.text_type
            and self.url == text_node.url
        ):
            return True
        return False


def text_node_to_html_node(text_node: TextNode) -> LeafNode | ParentNode:
    if text_node.text_type == text_type_text:
        return LeafNode(None, text_node.text)
    elif text_node.text_type == text_type_bold:
        return LeafNode("b", text_node.text)
    elif text_node.text_type == text_type_italic:
        return LeafNode("i", text_node.text)
    elif text_node.text_type == text_type_code:
        return LeafNode("code", text_node.text)
    elif text_node.text_type == text_type_link:
        return LeafNode("a", text_node.text, props={"href": text_node.url})
    elif text_node.text_type == text_type_image:
        return LeafNode("img", "", props={"src": text_node.url, "alt": text_node.text})
    raise ValueError(f"Don't support TextNode type {text_node.text_type}")


def split_nodes_delimiter(
    old_nodes: [TextNode], delimiter: str, text_type: str
) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        new_node = []
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue
        nodes_div = node.text.split(delimiter)
        for i in range(len(nodes_div)):
            if i % 2 == 0:
                new_node.append(TextNode(nodes_div[i], node.text_type))
            else:
                new_node.append(TextNode(nodes_div[i], text_type))
        new_nodes.extend(new_node)
    return new_nodes


# # chaCon: ESTO ES LO QUE QUIERO HACER PARA QUE PERMITA HACER NESTED. QUIERO HACERLO CON STACK PERO
# # ESTOY TENIENDO PROBLEMAS PARA EL DOBLE **, TALVES HACERLO CON RECURSION SEA MEJOR.
#
# def split_nodes(old_nodes: list[TextNode]) -> list[TextNode]:
#     new_nodes = []
#     for node in old_nodes:
#         text_nodes = split_node(node)
#         new_nodes.extend(text_nodes)
#     return new_nodes
#
# def split_node(old_node: TextNode) -> list[TextNode]:
#     stack = []
#     text_before = []
#     for c in old_node.text:
#         if c in stack:
#             pass
#         if c in markdown_type_map:
#             stack.append(c)
#         else:
#             text_before.append(c)
#     raise NotImplementedError


def extract_markdown_images(text: str) -> list[tuple]:
    text_re = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return text_re


def extract_markdown_links(text: str) -> list[tuple]:
    text_re = re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)
    return text_re


def split_nodes_image(old_nodes: [TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue
        images = extract_markdown_images(node.text)
        if len(images) == 0:
            new_nodes.append(node)
            continue
        new_node = helper_create_text_node_with_links(
            node.text, images, text_type_image
        )
        new_nodes.extend(new_node)
    return new_nodes


def split_nodes_link(old_nodes: [TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue
        links = extract_markdown_links(node.text)
        if len(links) == 0:
            new_nodes.append(node)
            continue
        new_node = helper_create_text_node_with_links(node.text, links, text_type_link)
        new_nodes.extend(new_node)
    return new_nodes


def helper_create_text_node_with_links(
    text: str, links: list[tuple], text_type: str
) -> list[TextNode]:
    result = []
    for link in links:
        alt = link[0]
        url = link[1]
        if text_type == text_type_image:
            text_url = f"![{alt}]({url})"
        elif text_type == text_type_link:
            text_url = f"[{alt}]({url})"
        else:
            raise ValueError(f"{text_type} not supported")
        sections = text.split(text_url, 1)
        result.append(TextNode(sections[0], text_type_text))
        text = text.replace(sections[0], "")
        result.append(TextNode(alt, text_type, url=url))
        text = text.replace(text_url, "")
    if text:
        result.append(TextNode(text, text_type_text))
    return result


def text_to_textnodes(text: str) -> list[TextNode]:
    new_node = TextNode(text, text_type_text)
    bold_add = split_nodes_delimiter([new_node], "**", text_type_bold)
    italic_add = split_nodes_delimiter(bold_add, "*", text_type_italic)
    code_add = split_nodes_delimiter(italic_add, "`", text_type_code)
    link_add = split_nodes_link(code_add)
    image_add = split_nodes_image(link_add)
    return image_add
