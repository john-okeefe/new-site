import re

from textnode import TextNode


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    final_node_list = []
    for old_node in old_nodes:
        node_list = []
        if not isinstance(old_node, TextNode):
            node_list.append(old_node)
            return node_list
        split_list = old_node.text.split(delimiter)
        if old_node.text.count(delimiter) % 2 != 0:
            raise ValueError("No closing delimiter found")
        for i in range(len(split_list)):
            if i % 2 != 0 and len(split_list[i]) > 0:
                part = TextNode(split_list[i], text_type)
                node_list.append(part)
            elif len(split_list[i]) > 0:
                part = TextNode(split_list[i], "text")
                node_list.append(part)
        final_node_list.extend(node_list)

    return final_node_list


def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)
