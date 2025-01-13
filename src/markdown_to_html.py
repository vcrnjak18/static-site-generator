from inline_markdown import text_to_textnodes

from block_markdown import markdown_to_blocks, block_to_block_type, is_heading

from htmlnode import ParentNode, text_node_to_html_node

# popis fja:
# is_heading - vraća broj nađenih # da znamo level headinga

# markdown_to_blocks - rastavlja markdown na blokove, čisti višak praznih redova i whitespace
# block_to_block_type - uzima blok iz prethodne fje i vraća tip bloka: paragraf, heading, code, ...

# text_to_textnodes - prima text i rastavlja ga prema tipu teksta i radi TextNode objekte

# text_node_to_html_node - prima TextNode(text, text_type, url=None) tip i vraća LeafNode(tag, value, props=None)

# -------------------------------------------------------------------
# ------ helper functions:

def text_to_children(text):
    list_of_textnodes = text_to_textnodes(text)

    list_of_htmlnodes = []

    for textnode in list_of_textnodes:
        htmlnode = text_node_to_html_node(textnode)
        list_of_htmlnodes.append(htmlnode)

    return list_of_htmlnodes

# --------------

def heading_to_html_node(block, heading_level):
    cut = heading_level + 1 #makni hashove i space
    pure_text = block[cut:]
    children = text_to_children(pure_text)
    return ParentNode(tag=f"h{heading_level}", children=children)


def code_to_html_node(block):
    pure_text = block[4:-3]
    children = text_to_children(pure_text)
    code = ParentNode(tag="code", children=children)
    return ParentNode(tag="pre", children=[code])


def quote_to_html_node(block):
    lines = block.split("\n")
    string_parts = []

    #quote postaje jedan tekst, ne održava retke u html-u, zato tekst treba spojit
    for line in lines:
        string_parts.append(line.lstrip(">").strip()) #skini > i ako ima razmak; moglo je i line[2:], ali možda ima više razmaka nakon >

    pure_text = " ".join(string_parts)
    children = text_to_children(pure_text)
    return ParentNode(tag="blockquote", children=children)
        

def unord_list_to_html_node(block):
    lines = block.split("\n")
    total_children = []

    for line in lines:
            pure_text = line[2:].strip()
            children = text_to_children(pure_text)
            total_children.append(ParentNode(tag="li", children=children))
    return ParentNode(tag="ul", children=total_children)


def ord_list_to_html_node(block):
    lines = block.split("\n")
    total_children = []

    for line in lines:
            pure_text = line[3:].strip()
            children = text_to_children(pure_text)
            total_children.append(ParentNode(tag="li", children=children))
    return ParentNode(tag="ol", children=total_children)


def paragraph_to_html_node(block):
    #zbog toga što html gleda \n kao " ":
    lines = block.split("\n")
    pure_text = " ".join(lines)

    children = text_to_children(pure_text)
    return ParentNode(tag="p", children=children)



def block_to_html_node(block):
    block_type = block_to_block_type(block)

    if block_type == "paragraph":
        parent_children_html_nodes = paragraph_to_html_node(block)
        return parent_children_html_nodes
    
    if block_type == "heading":
        heading_level = is_heading(block)
        parent_children_html_nodes = heading_to_html_node(block, heading_level)
        return parent_children_html_nodes

    if block_type == "code":
        parent_children_html_nodes = code_to_html_node(block)
        return parent_children_html_nodes

    if block_type == "quote":
        parent_children_html_nodes = quote_to_html_node(block)
        return parent_children_html_nodes

    if block_type == "unordered_list":
        parent_children_html_nodes = unord_list_to_html_node(block)
        return parent_children_html_nodes

    if block_type == "ordered_list":
        parent_children_html_nodes = ord_list_to_html_node(block)
        return parent_children_html_nodes

    raise ValueError("Invalid block type") # unrecognized block pattern


# --------------------------------

# ---- main function:


def markdown_to_html_node(markdown):
    # separate markdown text into blocks
    list_of_blocks = markdown_to_blocks(markdown)

    list_of_html_blocks = []

    for block in list_of_blocks:
        html_node = block_to_html_node(block)
        list_of_html_blocks.append(html_node)

    # create final html parent block that contains all other blocks, wrapped in div tag
    final_parent = ParentNode(tag="div", children=list_of_html_blocks)

    return final_parent


# ------------------

def extract_title(markdown):
    list_of_blocks = markdown_to_blocks(markdown)

    for block in list_of_blocks:
        parts = block.split()

        if len(parts) > 1: #ako splitani blok ima samo 1 element, to nije heading
            no_of_hash = parts[0].count("#") #prebroji hashove u prvom elementu
            if no_of_hash == 1:
                title = block.lstrip("# ")
                return title
    
    raise Exception("There is no h1 header!")