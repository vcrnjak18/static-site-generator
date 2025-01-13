from textnode import *
from web_build import *




# -------------------------------------------         

def main():
    
    #text_node_obj = TextNode("neki text", TextType.ITALIC)
    #print(text_node_obj)

    copy_static_public("static", "public")
    generate_page("content/index.md", "template.html", "public/index.html")

main()