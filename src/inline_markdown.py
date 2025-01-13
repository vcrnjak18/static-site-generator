import re
from textnode import *

def split_nodes_delimiter(old_nodes, delimiter, text_type):

# node = TextNode("This is text with a `code block` word", TextType.NORMAL)
    final_list = []

    for node in old_nodes:
        if node.text.count(delimiter) % 2 != 0:
            raise Exception("This is not proper Markdown syntax!")

        if node.text_type == TextType.NORMAL:
            split_list = node.text.split(delimiter)

            if delimiter == "**":
                special_type = TextType.BOLD
            if delimiter == "*":
                special_type = TextType.ITALIC
            if delimiter == "`":
                special_type = TextType.CODE

            for i in range(len(split_list)):
                if split_list[i]:
                    if i % 2 == 0:
                        final_list.append(TextNode(split_list[i], TextType.NORMAL))
                    else:
                        final_list.append(TextNode(split_list[i], special_type))
        
        else:
            final_list.append(node)

    return final_list


# -------------------------------------------------------

# ---- helper functions:

def extract_markdown_images(text):
    # takes text, returns list of tuples(alt text, path/url)
    return re.findall(r"\!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    # takes text, returns list of tuples(anchor text, url)  
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


# ----- main function 1:

def split_nodes_image(old_nodes):
        final_list = []

        for node in old_nodes:
            if node.text_type == TextType.NORMAL:
                extract_image = extract_markdown_images(node.text) #vraća listu tuplova (alt, url) za svaku sliku koju nađe
                
                if not extract_image: #ako nema slike, samo appendaj početni string
                    final_list.append(node)

                else:
                    text_to_extract = node.text

                    for tuple in extract_image: #prođi kroz svaki tuple
                        markdown_image = f"![{tuple[0]}]({tuple[1]})" #pa od tupla napravi image markdown
                        sections = text_to_extract.split(markdown_image, 1) #pa input rečenicu podijeli koristeći sliku kao delimiter
                        # tu će se desiti: "neki text", (tu je bila slika delimiter, pa je prazno), "ostatak teksta, druga slika itd."
                        if len(sections) != 2: #provjera za svaki slučaj je li dobro odvojeno
                            raise ValueError("Invalid markdown, image section not closed!")
                        # znači uvijek se dobiju 2 komada:
                        if sections[0]: #ako prvi komad nije prazan, dodaj ga u listu, sigurno je NORMAL
                            final_list.append(TextNode(sections[0], TextType.NORMAL)) #prvi dio
                            final_list.append(TextNode(tuple[0], TextType.IMAGE, tuple[1])) #dodaj delimiter sliku
                        else:
                            final_list.append(TextNode(tuple[0], TextType.IMAGE, tuple[1])) #dodaj delimiter sliku

                        text_to_extract = sections[1]

                    if text_to_extract: #dodaj ono što je ostalo nakon zadnjeg splita, sigurno je NORMAL
                        final_list.append(TextNode(text_to_extract, TextType.NORMAL))

            else:
                final_list.append(node)

        return final_list


# ----- main function 2:

# ovo je ista funkcija kao image, samo drugačiji stil
def split_nodes_link(old_nodes):
    final_list = []

    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            final_list.append(node)
            continue

        extract_link = extract_markdown_links(node.text)

        if not extract_link:
            final_list.append(node)
            continue

        text_to_extract = node.text

        for tuple in extract_link: 
            markdown_link = f"[{tuple[0]}]({tuple[1]})" 
            sections = text_to_extract.split(markdown_link, 1)

            if len(sections) != 2:
                raise ValueError("Invalid markdown, link section not closed!")

            if sections[0]:
                final_list.append(TextNode(sections[0], TextType.NORMAL))

            final_list.append(TextNode(tuple[0], TextType.LINK, tuple[1]))

            text_to_extract = sections[1]

        if text_to_extract:
            final_list.append(TextNode(text_to_extract, TextType.NORMAL))
                
    return final_list



# -------------------------------------------


def text_to_textnodes(text):
    node = [TextNode(text, TextType.NORMAL)] #kreiraj TextNode od običnog teksta, postavi na normal

    node = split_nodes_delimiter(node, "**", TextType.BOLD) #prebriši node pod ovim uvjetima
    node = split_nodes_delimiter(node, "*", TextType.ITALIC) #...
    node = split_nodes_delimiter(node, "`", TextType.CODE)
    node = split_nodes_image(node)
    node = split_nodes_link(node)

    return node