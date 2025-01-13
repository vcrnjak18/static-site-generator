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


def test_block_to_block_type():
    # Test heading
    assert block_to_block_type("# Heading 1") == "heading"
    assert block_to_block_type("###### Heading 6") == "heading"
    assert block_to_block_type("####### Not a heading") == "paragraph"

    # Test code blocks
    assert block_to_block_type("```\nsome code\n```") == "code"
    assert block_to_block_type("```python\ndef hello():\n    print('hi')\n```") == "code"

    # Test quotes
    assert block_to_block_type("> This is a quote") == "quote"
    assert block_to_block_type("> Line 1\n> Line 2") == "quote"
    assert block_to_block_type("> Line 1\nNot a quote") == "paragraph"

    # Test unordered lists
    assert block_to_block_type("* Item 1\n* Item 2") == "unordered_list"
    assert block_to_block_type("- Item 1\n- Item 2") == "unordered_list"
    assert block_to_block_type("* Item 1\n- Item 2") == "unordered_list"

    # Test ordered lists
    assert block_to_block_type("1. First\n2. Second") == "ordered_list"
    assert block_to_block_type("1. Only one") == "ordered_list"
    assert block_to_block_type("1. First\n3. Third") == "paragraph"

    # Test paragraphs
    assert block_to_block_type("Just a normal paragraph") == "paragraph"
    assert block_to_block_type("Line 1\nLine 2") == "paragraph"

    # Edge cases
    assert block_to_block_type("####### Too many hashes") == "paragraph"
    assert block_to_block_type("#Not a heading") == "paragraph"  # no space after #
    assert block_to_block_type("1. First\n3. Skipped number") == "paragraph"
    assert block_to_block_type("* No space*after asterisk") == "paragraph"



if __name__ == "__main__":
    unittest.main()