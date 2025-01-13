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

        with open(dest_path, 'r') as check_file:
            print("Contents of the saved file:")
            print(check_file.read())

    except Exception as e:
        print(f"Error during page generation: {e}")
        raise e
