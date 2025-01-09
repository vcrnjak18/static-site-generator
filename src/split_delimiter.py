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