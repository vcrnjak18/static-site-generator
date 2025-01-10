

def markdown_to_blocks(markdown):
    block_list = markdown.split("\n\n")

    purified_list = []

    for block in block_list:
        if block:
            clean_block = block.strip()
            purified_list.append(clean_block)

    return purified_list