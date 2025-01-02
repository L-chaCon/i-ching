import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_prop_href(self):
        test_props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        text_props = HTMLNode(props=test_props).props_to_html()
        self.assertEqual(text_props, 'href="https://www.google.com" target="_blank"')

    def test_text_prop_not_valid(self):
        test_props = [
            "href: https://www.google.com",
            "target: _blank",
        ]
        node = HTMLNode(props=test_props)
        with self.assertRaises(AttributeError) as context:
            node.props_to_html()
        self.assertTrue("'list' object has no attribute 'items'", context.exception)

    def test_prop_class(self):
        test_props = {"class": "test_class"}
        text_html = HTMLNode(props=test_props).props_to_html()
        self.assertEqual(text_html, 'class="test_class"')


class TestLeafNode(unittest.TestCase):
    def test_to_html_paragraph(self):
        leaf_node = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(leaf_node.to_html(), "<p>This is a paragraph of text.</p>")

    def test_to_html_link(self):
        test_props = {"href": "https://www.google.com"}
        leaf_node = LeafNode("a", "Click me!", props=test_props)
        self.assertEqual(
            leaf_node.to_html(), '<a href="https://www.google.com">Click me!</a>'
        )

    def test_to_html_empty_tag(self):
        leaf_node = LeafNode(None, "This is plane text")
        self.assertEqual(leaf_node.to_html(), "This is plane text")


class TestParentNode(unittest.TestCase):
    def test_to_html_just_leafes(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_to_html_parent_of_parent(self):
        node = ParentNode(
            "div",
            [
                ParentNode("div", [LeafNode("p", "This is a div in a div")]),
                ParentNode(
                    "div",
                    [
                        ParentNode(
                            "p",
                            [
                                LeafNode("b", "Bold text"),
                                LeafNode(None, "Normal text"),
                            ],
                        )
                    ],
                ),
                ParentNode(
                    "p",
                    [
                        LeafNode(None, "Normal text"),
                        LeafNode("i", "italic text"),
                        LeafNode(None, "Normal text"),
                    ],
                ),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<div><div><p>This is a div in a div</p></div><div><p><b>Bold text</b>Normal text</p></div><p>Normal text<i>italic text</i>Normal text</p></div>",
        )

    def test_to_html_no_children(self):
        node = ParentNode("div", None)
        with self.assertRaises(ValueError) as context:
            node.to_html()
        self.assertTrue("There is not children", context.exception)

    def test_to_html_with_props(self):
        test_props = {"class": "test_class"}
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
            props=test_props,
        )
        self.assertEqual(
            node.to_html(),
            '<p class="test_class"><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>',
        )


if __name__ == "__main__":
    unittest.main()
