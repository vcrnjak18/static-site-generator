import unittest

from htmlnode import *


class TestHTMLNode(unittest.TestCase):

    def test_props(self):
            # za komplicirane slučajeve kao što je dict,
            # možeš postavit dict vani:

        props = {
            "href": "https://www.google.com", 
            "target": "_blank",
            "class": "link"
        }

        # atribut props = ime dicta (props)
        node = HTMLNode(props=props)

        # zoveš metodu na svoj node, koja daje rezultat
        result = node.props_to_html()

        # provjeri daje li rezultat ono što ti želiš
        self.assertEqual(result,  ' href="https://www.google.com" target="_blank" class="link"')

    def test_props_none(self):
        node = HTMLNode(props=None)
        result = node.props_to_html()
        self.assertEqual(result, "")

    def test_tag(self):
        node = HTMLNode("p")
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, None)

    def test_values(self):
        node = HTMLNode(
            "div",
            "I wish I could read",
        )
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.value,
            "I wish I could read",
        )
        self.assertEqual(
            node.children,
            None,
        )
        self.assertEqual(
            node.props,
            None,
        )

    def test_repr(self):
        node = HTMLNode(
            "p",
            "What a strange world",
            None,
            {"class": "primary"},
        )
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(p, What a strange world, children: None, {'class': 'primary'})",
        )

    
    def test_to_html(self):
        node1 = LeafNode("p", "This is a paragraph of text.")
        node2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        node4 = LeafNode(None, "Some text")
        node5 = LeafNode(None, None, None)

        self.assertEqual(node1.to_html(), "<p>This is a paragraph of text.</p>")
        self.assertEqual(node2.to_html(), '<a href="https://www.google.com">Click me!</a>')
        self.assertEqual(node4.to_html(), "Some text")
        
        with self.assertRaises(ValueError):
            node5.to_html()


    def test_parent(self):
        node1 = ParentNode("p", None)
        node2 = ParentNode("div", "")
        node3 = ParentNode(None, LeafNode("p", "some text"))
        node4 = ParentNode(None, LeafNode(None, "neki tekst"))

        node5 = ParentNode("p", [LeafNode("b", "boldaj text"), LeafNode("i", "italic text")])
        node6 = ParentNode("p", [LeafNode("h1", "header")])

        node6a = ParentNode("p", [LeafNode("h1", "header", {"html": "some value"})])
        node6b = ParentNode("p", [LeafNode("h1", "header", {"html": "some value"})], {"css": "some list"})

        node7 = ParentNode("div", [ParentNode("p", [LeafNode("b", "nested text")])])

        with self.assertRaises(ValueError):
            node1.to_html()

        with self.assertRaises(ValueError):
            node2.to_html()

        with self.assertRaises(ValueError):
            node3.to_html()

        with self.assertRaises(ValueError):
            node4.to_html()

        self.assertEqual(node5.to_html(), "<p><b>boldaj text</b><i>italic text</i></p>")
        self.assertEqual(node6.to_html(), "<p><h1>header</h1></p>")

        self.assertEqual(node6a.to_html(), '<p><h1 html="some value">header</h1></p>')
        self.assertEqual(node6b.to_html(), '<p css="some list"><h1 html="some value">header</h1></p>')
        self.assertEqual(node7.to_html(), '<div><p><b>nested text</b></p></div>')

    def test_text_to_html(self):
        text_normal = TextNode("classic text", TextType.NORMAL)
        text_bold = TextNode("bold text", TextType.BOLD)
        text_italic = TextNode("italic text", TextType.ITALIC)
        text_code = TextNode("code text", TextType.CODE)
        text_link = TextNode("link text", TextType.LINK, "www.google.com")
        text_image = TextNode("alt image text", TextType.IMAGE, "img/my_image/frodo.png")

        text_to_html = text_node_to_html_node(text_normal)
        self.assertEqual(text_to_html.to_html(), "classic text")

        text_to_html = text_node_to_html_node(text_bold)
        self.assertEqual(text_to_html.to_html(), "<b>bold text</b>")

        text_to_html = text_node_to_html_node(text_italic)
        self.assertEqual(text_to_html.to_html(), "<i>italic text</i>")

        text_to_html = text_node_to_html_node(text_code)
        self.assertEqual(text_to_html.to_html(), "<code>code text</code>")

        text_to_html = text_node_to_html_node(text_link)
        self.assertEqual(text_to_html.to_html(), '<a href="www.google.com">link text</a>')

        text_to_html = text_node_to_html_node(text_image)
        self.assertEqual(text_to_html.to_html(), '<img src="img/my_image/frodo.png" alt="alt image text">')


if __name__ == "__main__":
    unittest.main()