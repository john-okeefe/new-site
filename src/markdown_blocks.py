import re

from htmlnode import LeafNode, ParentNode

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"

def markdown_to_blocks(markdown):
    blocks = re.split("\n\n", markdown)
    final = []
    for block in blocks:
        if block != "":
            final.append(block.strip())
    return final

def block_to_block_type(block):
    heading_regex = "^#{1,6} "
    code_regex = "^```.*```$"
    quote_regex = "^>"
    unordered_regex = "^[-,*] "
    ordered_regex = "^[0-9]{1,10}\\. "
    if re.search(heading_regex, block):
        return block_type_heading
    elif re.search(code_regex, block):
        return block_type_code
    elif re.search(quote_regex, block):
        is_true = True
        lines = re.split("\n", block)
        for line in lines:
            if re.search(quote_regex, line):
                is_true = True
            else:
                is_true = False
        if is_true:
            return block_type_quote
    elif re.search(unordered_regex, block):
        is_true = True
        lines = re.split("\n", block)
        for line in lines:
            if re.search(unordered_regex, line):
                is_true = True
            else:
                is_true = False
        if is_true:
            return block_type_unordered_list
    elif re.search(ordered_regex, block):
        is_true = True
        lines = re.split("\n", block)
        for i in range(len(lines)):
            if re.search(ordered_regex, lines[i]) and int(re.search("^[0-9]{1,10}", lines[i]).group()) == (i+1):
                is_true = True
            else:
                is_true = False
        if is_true:
            return block_type_ordered_list
    else:
        return block_type_paragraph
    
def paragraph_to_html_node(block):
    return LeafNode("p", block)

def heading_to_html_node(block):
    regexed_block = re.search("(^#{1,6}) (.*)", block)
    count = len(regexed_block.groups(1))
    data = regexed_block.groups(2)
    return LeafNode(f"h{count}", data)

def code_to_html_node(block):
    code_data = re.search("^```(.*)```$", block).groups(1)[0]
    return ParentNode(
        "pre",
        [
            LeafNode("code", code_data)
        ]
    )

def quote_to_html_node(block):
    quote_lines = re.split("\n?> ", block)
    if quote_lines[0] == "":
        quote_lines = quote_lines[1:]
    quote = []
    for quote_line in quote_lines:
        quote.append(quote_line.strip())
    data = "\n".join(quote)
    return LeafNode("blockquote", data)

def unordered_list_to_html_node(block):
    nodes = []
    bullets = re.split("\n?[*,-] ", block)
    for bullet in bullets:
        if bullet != "":
            nodes.append(LeafNode("li", bullet))
    return ParentNode("ul", nodes)

def ordered_list_to_html_node(block):
    nodes = []
    bullets = re.split("\n?[0-9]{1,10}\\. ", block)
    for bullet in bullets:
        if bullet != "":
            nodes.append(LeafNode("li", bullet))
    return ParentNode("ol", nodes)
    
def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case "paragraph":
                nodes.append(paragraph_to_html_node(block))
            case "code":
                nodes.append(code_to_html_node(block))
            case "heading":
                nodes.append(heading_to_html_node(block))
            case "quote":
                nodes.append(quote_to_html_node(block))
            case "unordered_list":
                nodes.append(unordered_list_to_html_node(block))
            case "ordered_list":
                nodes.append(ordered_list_to_html_node(block))
    return ParentNode("div", nodes)


quote_block = "> quote first line\n> quote second line"
print(quote_to_html_node(quote_block))