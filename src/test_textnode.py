import unittest

from textnode import (
    TextNode,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_node_to_html_node,
    text_to_textnodes,
    text_type_bold,
    text_type_code,
    text_type_image,
    text_type_italic,
    text_type_link,
    text_type_text,
)


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", text_type_bold)
        node2 = TextNode("This is a text node", text_type_bold)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", text_type_text)
        node2 = TextNode("This is a text node", text_type_italic)
        self.assertNotEqual(node, node2)

    def test_url_none(self):
        node = TextNode("This is a text node", text_type_code, url=None)
        node2 = TextNode("This is a text node", text_type_code)
        self.assertEqual(node, node2)

    def test_url_empty_value_text(self):
        node = TextNode("", text_type_image, url="url to image")
        self.assertEqual(repr(node), f"<TextNode  {text_type_image} url to image>")

    def test_link_value(self):
        node = TextNode("Click here", text_type_link, url="google.com")
        self.assertEqual(
            repr(node), f"<TextNode Click here {text_type_link} google.com>"
        )


class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", text_type_text)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.tag, None)


class TestSplitNodes(unittest.TestCase):
    def test_split_nodes_delimiter_boot_case(self):
        node = TextNode("This is text with a `code block` word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "`", text_type_code)
        result = [
            TextNode("This is text with a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" word", text_type_text),
        ]
        self.assertEqual(new_nodes, result)

    def test_split_nodes_link_boot_1(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            text_type_text,
        )
        new_nodes = split_nodes_link([node])
        result = [
            TextNode("This is text with a link ", text_type_text),
            TextNode("to boot dev", text_type_link, "https://www.boot.dev"),
            TextNode(" and ", text_type_text),
            TextNode(
                "to youtube", text_type_link, "https://www.youtube.com/@bootdotdev"
            ),
        ]
        self.assertEqual(new_nodes, result)

    def test_split_nodes_image_base(self):
        node = TextNode(
            "This is text with image links ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)",
            text_type_text,
        )
        new_nodes = split_nodes_image([node])
        result = [
            TextNode("This is text with image links ", text_type_text),
            TextNode("to boot dev", text_type_image, "https://www.boot.dev"),
            TextNode(" and ", text_type_text),
            TextNode(
                "to youtube", text_type_image, "https://www.youtube.com/@bootdotdev"
            ),
        ]
        self.assertEqual(new_nodes, result)


class TestExtractMarkdown(unittest.TestCase):
    def test_extract_markdown_images_boots_1(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        new_text = extract_markdown_images(text)
        result = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
        ]
        self.assertEqual(new_text, result)

    def test_extract_markdown_links_boots_1(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        new_text = extract_markdown_links(text)
        result = [
            ("to boot dev", "https://www.boot.dev"),
            ("to youtube", "https://www.youtube.com/@bootdotdev"),
        ]
        self.assertEqual(new_text, result)

        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        new_text = extract_markdown_links(text)
        result = [
            ("to boot dev", "https://www.boot.dev"),
            ("to youtube", "https://www.youtube.com/@bootdotdev"),
        ]
        self.assertEqual(new_text, result)


class TestTextToTextNodes(unittest.TestCase):
    def test_text_to_textnodes_boots(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        result = [
            TextNode("This is ", text_type_text),
            TextNode("text", text_type_bold),
            TextNode(" with an ", text_type_text),
            TextNode("italic", text_type_italic),
            TextNode(" word and a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" and an ", text_type_text),
            TextNode(
                "obi wan image", text_type_image, "https://i.imgur.com/fJRm4Vk.jpeg"
            ),
            TextNode(" and a ", text_type_text),
            TextNode("link", text_type_link, "https://boot.dev"),
        ]
        self.assertEqual(new_nodes, result)


if __name__ == "__main__":
    unittest.main()
