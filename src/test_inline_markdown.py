import unittest
from inline_markdown import *

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



    def test_extracting_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        expected = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]

        self.assertListEqual(extract_markdown_images(text), expected)



    def test_extracting_links(self):
        text = "This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        expected = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]

        text_empty = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        expected_empty = []

        self.assertListEqual(extract_markdown_links(text), expected)

        self.assertListEqual(extract_markdown_links(text_empty), expected_empty)

def test_splitting_images(self):
    tex = "Some text"
    tex_im = "Some text with some ![image](image_url)"
    tex_im_tex = "some text ![image](image_url) in some text"
    tex_im_im_tex_im = "some text ![image](image_url)![img2](img2_url) then text and ![image3](image3_url)"
    im_tex = "![image](img_url) after text"
    im = "![image](img_url)"
    im_tex_im = "![image](img_url) then text then ![image2](img_url2)"
    tex_im_tex_im = "tekst then ![image](img_url) then ![image2](img2_url)"

    tex_expected = [TextNode("Some text", TextType.NORMAL)]
    tex_im_expected = [TextNode("Some text with some ", TextType.NORMAL), TextNode("image", TextType.IMAGE, "image_url")]

    self.assertListEqual(split_nodes_image(tex), tex_expected)
    self.assertListEqual(split_nodes_image(tex_im), tex_im_expected)

def test_splitting_links(self):
    tex = "Some text"
    tex_lin = "Some text with some [link name](url)"
    lin_tex = "[link name](url) after text"

    tex_expected = [TextNode("Some text", TextType.NORMAL)]
    tex_lin_expected = [TextNode("Some text with some ", TextType.NORMAL), TextNode("link name", TextType.LINK, "url")]
    lin_tex_expected = [TextNode("link name", TextType.LINK, "url"), TextNode(" after text", TextType.NORMAL)]

    self.assertListEqual(split_nodes_link(tex), tex_expected)
    self.assertListEqual(split_nodes_link(tex_lin), tex_lin_expected)
    self.assertListEqual(split_nodes_link(lin_tex), lin_tex_expected)


def test_text_to_textnode(self):
    text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
    text_expected = [
    TextNode("This is ", TextType.TEXT),
    TextNode("text", TextType.BOLD),
    TextNode(" with an ", TextType.TEXT),
    TextNode("italic", TextType.ITALIC),
    TextNode(" word and a ", TextType.TEXT),
    TextNode("code block", TextType.CODE),
    TextNode(" and an ", TextType.TEXT),
    TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
    TextNode(" and a ", TextType.TEXT),
    TextNode("link", TextType.LINK, "https://boot.dev"),
    ]

    self.assertListEqual(text_to_textnodes(text), text_expected)