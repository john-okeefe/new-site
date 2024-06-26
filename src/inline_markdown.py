import re

from textnode import (TextNode, text_type_bold, text_type_code,
                      text_type_italic, text_type_text, text_type_image, text_type_link)


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], text_type_text))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        images = extract_markdown_images(old_node.text)
        if old_node.text_type != text_type_text or len(images) == 0:
            new_nodes.append(old_node)
            continue
        if len(old_node.text) == 0:
            continue
        split_nodes = []
        original_text = old_node.text
        sections = []
        for i in range(len(images)):
            section = original_text.split(f"![{images[i][0]}]({images[i][1]})", 1)
            if len(section) != 2:
                raise ValueError("Invalid markdown, image section not closed")
            sections.append(section[0])
            sections.append(images[i])
            if i+1 is len(images):
                sections.append(section[1])
            else:
                original_text = section[1]
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if isinstance(sections[i], str):
                split_nodes.append(TextNode(sections[i], text_type_text))
            else:
                split_nodes.append(TextNode(sections[i][0], text_type_image, sections[i][1]))
        new_nodes.extend(split_nodes)
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        links = extract_markdown_links(old_node.text)
        if old_node.text_type != text_type_text or len(links) == 0:
            new_nodes.append(old_node)
            continue
        if len(old_node.text) == 0:
            continue
        split_nodes = []
        original_text = old_node.text
        sections = []
        for i in range(len(links)):
            section = original_text.split(f"[{links[i][0]}]({links[i][1]})", 1)
            if len(section) != 2:
                raise ValueError("Invalid markdown, link section not closed")
            sections.append(section[0])
            sections.append(links[i])
            if i+1 is len(links):
                sections.append(section[1])
            else:
                original_text = section[1]
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if isinstance(sections[i], str):
                split_nodes.append(TextNode(sections[i], text_type_text))
            else:
                split_nodes.append(TextNode(sections[i][0], text_type_link, sections[i][1]))
        new_nodes.extend(split_nodes)
    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)

def text_to_textnodes(text):
    nodes = [TextNode(text, text_type_text)]
    nodes = split_nodes_delimiter(nodes, "**", text_type_bold)
    nodes = split_nodes_delimiter(nodes, "*", text_type_italic)
    nodes = split_nodes_delimiter(nodes, "`", text_type_code)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes