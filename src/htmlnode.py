
from textnode import *

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        construct = ""
        if self.props != None:
            for key, value in self.props.items():
                construct += " " + key + '="' + value + '"'

        return construct

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.tag in ["img"]:
            # self.tag in ["img"] je složen da provjeri da li je tag img
            # i po mogućnosti jer je lista, mogu se dodati različiti još
            # inače da postoji samo jedan, može i self.tag == "img"
            if self.props is None:
                return f"<{self.tag}>"
            else:
                return f"<{self.tag}{self.props_to_html()}>"

        elif self.value is not None:             
            if self.tag is None:
                return self.value

            if self.props is None:
                return f"<{self.tag}>{self.value}</{self.tag}>"
            else:
                return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
        else:
            raise ValueError("A leaf node must have value!")

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        # if self.tag is None: - ovo je ok ako se baš očekuje samo None
        # da krši, ali
        if not self.tag: # ovo pazi da nije None, empty str ili neš, kao 0
            raise ValueError("There is no tag!")
        if not self.children: # ovo provjerava da li je dijete None ili prazan
            raise ValueError("There are no children!")

        if self.props is None:
            html_string = f"<{self.tag}>"
        else:
            html_string = f"<{self.tag}{self.props_to_html()}>"

        for child in self.children:
            html_string += child.to_html()
            
        html_string += f"</{self.tag}>"
        return html_string

    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"



# ---------------------------------------------------------------



# izgled text_node = TextNode(text, text_type, url=None)    
def text_node_to_html_node(text_node):
    match(text_node.text_type):
        case TextType.NORMAL:
            return LeafNode(None, text_node.text)

        case TextType.BOLD:
            return LeafNode("b", text_node.text)

        case TextType.ITALIC:
            return LeafNode("i", text_node.text)

        case TextType.CODE:
            return LeafNode("code", text_node.text)

        case TextType.LINK:
            props = {}
            props["href"] = text_node.url
            return LeafNode("a", text_node.text, props)

        case TextType.IMAGE:
            props = {}
            props["src"] = text_node.url
            props["alt"] = text_node.text
            return LeafNode("img", None, props)

        case _:
            raise ValueError("Unrecognized text type")