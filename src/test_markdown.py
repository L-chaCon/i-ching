import textwrap
import unittest

from markdown import (
    block_to_block_type,
    block_type_code,
    block_type_heading,
    block_type_ordered_list,
    block_type_paragraph,
    block_type_quote,
    block_type_unordered_list,
    extract_title,
    markdown_to_blocks,
    markdown_to_html_node,
)


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks_boot(self):
        text = textwrap.dedent("""\
        # This is a heading

        This is a paragraph of text. It has some **bold** and *italic* words inside of it.

        * This is the first list item in a list block
        * This is a list item
        * This is another list item""")
        blocks = markdown_to_blocks(text)
        result = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            textwrap.dedent("""\
            * This is the first list item in a list block
            * This is a list item
            * This is another list item"""),
        ]
        self.assertEqual(blocks, result)

    def test_markdown_to_block_more_than_one(self):
        text = textwrap.dedent("""\
        # This is a heading




        This is a paragraph of text. It has some **bold** and *italic* words inside of it.




        * This is the first list item in a list block
        * This is a list item
        * This is another list item""")
        blocks = markdown_to_blocks(text)
        result = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            textwrap.dedent("""\
            * This is the first list item in a list block
            * This is a list item
            * This is another list item"""),
        ]
        self.assertEqual(blocks, result)

    def test_block_to_block_type_code(self):
        code_block = textwrap.dedent("""\
        ```python
            def main():
                return this_is_a_test_code block
        ```""")
        block_type = block_to_block_type(code_block)
        self.assertEqual(block_type, block_type_code)

    def test_block_to_block_type_heading_1(self):
        heading_block = "# Heading1"
        block_type = block_to_block_type(heading_block)
        self.assertEqual(block_type, block_type_heading)

    def test_block_to_block_type_heading_2(self):
        heading_block = "## Heading2"
        block_type = block_to_block_type(heading_block)
        self.assertEqual(block_type, block_type_heading)

    def test_block_to_block_type_heading_3(self):
        heading_block = "### Heading3"
        block_type = block_to_block_type(heading_block)
        self.assertEqual(block_type, block_type_heading)

    def test_block_to_block_type_heading_4(self):
        heading_block = "#### Heading4"
        block_type = block_to_block_type(heading_block)
        self.assertEqual(block_type, block_type_heading)

    def test_block_to_block_type_heading_5(self):
        heading_block = "##### Heading5"
        block_type = block_to_block_type(heading_block)
        self.assertEqual(block_type, block_type_heading)

    def test_block_to_block_type_heading_6(self):
        heading_block = "###### Heading7"
        block_type = block_to_block_type(heading_block)
        self.assertEqual(block_type, block_type_heading)

    def test_block_to_block_type_comment(self):
        quote_block = """> This is a quote
        > multi-line"""
        block_type = block_to_block_type(quote_block)
        self.assertEqual(block_type, block_type_quote)

    def test_block_to_block_type_unorder_star(self):
        unorder_block = textwrap.dedent("""\
        * first
        * second
        * third""")
        block_type = block_to_block_type(unorder_block)
        self.assertEqual(block_type, block_type_unordered_list)

    def test_block_to_block_type_unorder_line(self):
        unorder_block = textwrap.dedent("""\
        - first
        - second
        - third""")
        block_type = block_to_block_type(unorder_block)
        self.assertEqual(block_type, block_type_unordered_list)

    def test_block_to_block_type_order(self):
        unorder_block = textwrap.dedent("""\
        1. first
        2. second
        3. third""")
        block_type = block_to_block_type(unorder_block)
        self.assertEqual(block_type, block_type_ordered_list)

    def test_block_to_block_type_paragraph(self):
        paragraph = "this is a pharagraf"
        block_type = block_to_block_type(paragraph)
        self.assertEqual(block_type, block_type_paragraph)

    def test_block_to_block_type_paragraph_bad_list(self):
        paragraph = textwrap.dedent("""\
        * this is a pharagraf
        - list""")
        block_type = block_to_block_type(paragraph)
        self.assertEqual(block_type, block_type_paragraph)

    def test_block_to_block_type_paragraph_order_list(self):
        paragraph = textwrap.dedent("""\
        1. this is a pharagraf
        3. not order""")
        block_type = block_to_block_type(paragraph)
        self.assertEqual(block_type, block_type_paragraph)


class TestMarkdownToHTML(unittest.TestCase):
    def test_markdown_to_html(self):
        markdown = textwrap.dedent("""\
        # Title
        
        this is a text that is part of the markdown

        * list1
        * list2
        * list3

        ```
        def this_is_code():
            return "Hi"
        ```
        """)
        html_node = markdown_to_html_node(markdown)
        result = '<ParentNode div [<ParentNode h1 [<LeafNode None Title None>] None>, <ParentNode p [<LeafNode None this is a text that is part of the markdown None>] None>, <ParentNode ul [<ParentNode li [<LeafNode None list1 None>] None>, <ParentNode li [<LeafNode None list2 None>] None>, <ParentNode li [<LeafNode None list3 None>] None>] None>, <ParentNode pre [<LeafNode code def this_is_code():\n    return "Hi" None>] None>] None>'
        self.assertEqual(repr(html_node), result)


class TestTransformMarkdownToHTML(unittest.TestCase):
    def test_extract_title(self):
        markdown = textwrap.dedent("""\
        # Title
        
        this is a text that is part of the markdown

        * list1
        * list2
        * list3

        ```
        def this_is_code():
            return "Hi"
        ```
        """)
        title = extract_title(markdown)
        self.assertEqual(title, "Title")


if __name__ == "__main__":
    unittest.main()
