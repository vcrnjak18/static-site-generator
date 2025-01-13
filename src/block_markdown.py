

def markdown_to_blocks(markdown):
    block_list = markdown.split("\n\n")

    purified_list = []

    for block in block_list:
        if block:
            clean_block = block.strip()
            purified_list.append(clean_block)

    return purified_list


# ------------------------------------------------

# ------ helper functions:

def is_heading(block):
    parts = block.split()

    if len(parts) > 1: #ako splitani blok ima samo 1 element, to nije heading
        no_of_hash = parts[0].count("#") #prebroji hashove u prvom elementu
        if no_of_hash == len(parts[0]) and 1 <= no_of_hash <= 6: #broj hashova mora biti jednak duljini elementa (inače je moguće da ima drugih mixanih znakova)
            return no_of_hash
    
    return 0


def is_code(block):
    return block.startswith('```') and block.endswith('```')


def is_quote(block):
    split_block = block.split("\n") #razdvoji retke

    for line in split_block:
        if not line.startswith('>'):
            return False

    return True


def is_unordered(block):
    split_block = block.split("\n")

    for line in split_block:
        if not (line.startswith('* ') or line.startswith('- ')):
            return False

    return True


def is_ordered(block):
    split_block = block.split("\n")

    number = 0

    for line in split_block:
        number += 1

        if not line.startswith(f"{number}. "):
            return False

    return True

# ------main function:

def block_to_block_type(block):
    if is_heading(block):
        return "heading"
    
    if is_code(block):
        return "code"
    
    if is_quote(block):
        return "quote"

    if is_unordered(block):
        return "unordered_list"

    if is_ordered(block):
        return "ordered_list"

    return "paragraph"
