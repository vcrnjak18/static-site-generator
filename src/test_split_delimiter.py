import unittest
from split_delimiter import *

class TestDelimiter(unittest.TestCase):

    def test_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.NORMAL)
        node1 = TextNode("This is bold", TextType.BOLD)
        node2 = TextNode("This is **text** with a bold word", TextType.NORMAL)
        node3 = TextNode("This is *text* with a *italic* word", TextType.NORMAL)

        node4 = TextNode("This will crash `is bold", TextType.NORMAL)


        result_node = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected_node = [TextNode("This is text with a `code block` word", TextType.NORMAL)]

        self.assertListEqual(result_node, expected_node)

        result_node1 = split_nodes_delimiter([node1], "**", TextType.BOLD)
        expected_node1 = [TextNode("This is bold", TextType.BOLD)]

        self.assertListEqual(result_node1, expected_node1)

        result_node2 = split_nodes_delimiter([node2], "**", TextType.BOLD)
        expected_node2 = [TextNode("This is ", TextType.NORMAL), TextNode("text", TextType.BOLD), TextNode(" with a bold word", TextType.NORMAL)]

        self.assertListEqual(result_node2, expected_node2)

        result_node3 = split_nodes_delimiter([node3], "*", TextType.ITALIC)
        expected_node3 = [TextNode("This is ", TextType.NORMAL), TextNode("text", TextType.ITALIC), TextNode(" with a ", TextType.NORMAL), TextNode("italic", TextType.ITALIC), TextNode(" word", TextType.NORMAL)]

        self.assertListEqual(result_node3, expected_node3)


        with self.assertRaises(Exception):
            result_node4