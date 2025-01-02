from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import text_node_to_html_node, text_to_textnodes

block_type_code = "code"
block_type_heading = "heading"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"
block_type_paragraph = "paragraph"


def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = []
    paragraphs = markdown.split("\n\n")
    for block in paragraphs:
        if block:
            lines_in_block = block.split("\n")
            filter_lines = filter(lambda x: True if x else False, lines_in_block)
            blocks.append("\n".join(list(filter_lines)))
    return blocks


def block_to_block_type(markdown: str) -> str:
    string_markdown_list = list(markdown)
    markdown_line = markdown.split("\n")
    if (
        "".join(string_markdown_list[:3]) == "```"
        and "".join(string_markdown_list[-3:]) == "```"
    ):
        return block_type_code
    elif "# " in "".join(string_markdown_list[:7]):
        return block_type_heading
    elif markdown.startswith("> "):
        return block_type_quote
    elif markdown.startswith("* "):
        for line in markdown_line:
            if not line.startswith("* "):
                return block_type_paragraph
        return block_type_unordered_list
    elif markdown.startswith("- "):
        for line in markdown_line:
            if not line.startswith("- "):
                return block_type_paragraph
        return block_type_unordered_list
    elif markdown.startswith("1. "):
        number = 1
        for line in markdown_line:
            if not line.startswith(f"{number}. "):
                return block_type_paragraph
            number += 1
        return block_type_ordered_list
    return block_type_paragraph


def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    html_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        nodes = helper_block_to_html(block, block_type)
        html_nodes.extend(nodes)
    return ParentNode(tag="div", children=html_nodes)


def text_to_children(text: str) -> list[ParentNode | LeafNode]:
    text_nodes = text_to_textnodes(text)
    html_nodes: list[ParentNode | LeafNode] = []
    for node in text_nodes:
        html_nodes.append(text_node_to_html_node(node))
    return html_nodes


def helper_block_to_html(
    block: str, block_type: str
) -> list[ParentNode | LeafNode | HTMLNode]:
    html_nodes: list[ParentNode | LeafNode | HTMLNode] = []
    if block_type == block_type_heading:
        html_nodes.append(helper_block_to_heading(block))
    elif block_type == block_type_paragraph:
        html_nodes.append(ParentNode("p", text_to_children(block)))
    elif block_type == block_type_unordered_list:
        html_nodes.append(helper_block_to_ul(block))
    elif block_type == block_type_ordered_list:
        html_nodes.append(helper_block_to_ol(block))
    elif block_type == block_type_code:
        html_nodes.append(helper_block_to_code(block))
    elif block_type == block_type_quote:
        html_nodes.append(helper_block_to_quote(block))
    else:
        raise ValueError(f"{block_type} type is not implemented")
    return html_nodes


def helper_block_to_heading(block: str) -> ParentNode:
    title = block.split(" ", 1)
    title_lev = len(list(title[0]))
    return ParentNode(f"h{title_lev}", text_to_children(title[-1]))


def helper_block_to_ul(block: str) -> ParentNode:
    list_lines = block.split("\n")
    list_html = []
    for line in list_lines:
        line = line.lstrip("* ")
        line = line.lstrip("- ")
        inline_html = text_to_children(line)
        list_html.append(ParentNode("li", inline_html))
    return ParentNode("ul", list_html)


def helper_block_to_ol(block: str) -> ParentNode:
    list_html = []
    list_lines = block.split("\n")
    i = 1
    for line in list_lines:
        line = line.lstrip(f"{i}. ")
        inline_html = text_to_children(line)
        list_html.append(ParentNode("li", inline_html))
        i += 1
    return ParentNode("ol", list_html)


def helper_block_to_quote(block: str) -> ParentNode:
    quote_block = block.split("\n")
    clean_quote = []
    for quote in quote_block:
        clean_quote.append(quote.lstrip("> "))
    quote_value = "\n".join(clean_quote)
    return ParentNode("blockquote", text_to_children(quote_value))


def helper_block_to_code(block: str) -> ParentNode:
    code_block = block.split("\n")[1:-1]
    return ParentNode("pre", [LeafNode("code", "\n".join(code_block))])


def extract_title(markdown: str) -> str:
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block_to_block_type(block) == block_type_heading and block.startswith("# "):
            title = block.lstrip("# ")
            return title
    raise ValueError("No title found")
