import os, shutil
from markdown_to_html import markdown_to_html_node, extract_title

def copy_static_public(static_path, public_path):
    # if public exists, delete it
    if os.path.exists(public_path):
        shutil.rmtree(public_path)
    # create new public directory
    os.mkdir(public_path)

    # get list of all items/directories in the static directory
    static_list = os.listdir(static_path)

    for item in static_list:
        source_item_path = os.path.join(static_path, item)
        dest_item_path = os.path.join(public_path, item)
        
        # if item is file
        if os.path.isfile(source_item_path):
            shutil.copy(source_item_path, dest_item_path)

        # if item is folder
        if os.path.isdir(source_item_path):
            os.mkdir(dest_item_path) # create that folder in destination
            copy_static_public(source_item_path, dest_item_path) # call function again on the folder
            # to check all subfolder

# -------------------------------------------

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    try:
        with open(from_path, 'r') as md:
            markdown_content = md.read()
    
        with open(template_path, 'r') as temp:
            template_content = temp.read()
        

        html_node = markdown_to_html_node(markdown_content)
        html_content = html_node.to_html()

        title = extract_title(markdown_content)

        full_html = template_content.replace("{{ Content }}", html_content)
        full_html = full_html.replace("{{ Title }}", title)


        with open(dest_path, 'w') as output:
            output.write(full_html)

    except Exception as e:
        print(f"Error during page generation: {e}")
        raise e


# --------------------------------------------


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    content_items = os.listdir(dir_path_content)

    for item in content_items:
        item_path = os.path.join(dir_path_content, item)
        if os.path.isfile(item_path) and item.endswith(".md"):

            # get relative path to perserve the structure; if item is in content/majesty/item.md, then relative is majesty/item.md
            rel_item_path = os.path.relpath(item_path, dir_path_content) # kreće od contenta (to ignorira) i ide dalje
            
            # this has item.md file, we need item.html file, so:
            rel_item_path_html = rel_item_path.replace(".md", ".html")
         
            # destination path is now dest path + inner structure of starting folder
            dest_item_path = os.path.join(dest_dir_path, rel_item_path_html)
        
            folder_names = os.path.dirname(dest_item_path) # gets the name of the folder where .md item is including parent folders i.e. public/majesty
            os.makedirs(folder_names, exist_ok=True) # ako ne postoje na destinaciji, kreiraj sve te foldere; ako postoje, ok
            
            generate_page(item_path, template_path, dest_item_path)
        
        if os.path.isdir(item_path):
            new_dest_dir = os.path.join(dest_dir_path, item) # perserve last location
            generate_pages_recursive(item_path, template_path, new_dest_dir)