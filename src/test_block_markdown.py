import unittest
from block_markdown import *


class TestDelimiter(unittest.TestCase):

    def text_block_separation(self):
        text = """# This is a heading

                This is a paragraph of text. It has some **bold** and *italic* words inside of it.




                * This is the first list item in a list block
                * This is a list item
                * This is another list item"""

        expected = ["# This is a heading", "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
        "* This is the first list item in a list block* This is a list item* This is another list item"]

        self.assertEqual(markdown_to_blocks(text), expected)