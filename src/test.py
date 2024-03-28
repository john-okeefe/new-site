from inline_markdown import split_nodes_delimiter
from textnode import (TextNode, text_type_bold, text_type_code,
                      text_type_italic, text_type_text)

node = TextNode("This is text with a `code block` word", text_type_text)
new_nodes = split_nodes_delimiter([node], "`", text_type_code)
print(new_nodes)
