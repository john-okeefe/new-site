import unittest

from htmlnode import LeafNode, ParentNode
from markdown_blocks import (block_to_block_type, code_to_html_node, heading_to_html_node, markdown_to_blocks, 
                             block_type_heading, block_type_code, block_type_paragraph,
                             block_type_ordered_list, block_type_unordered_list, block_type_quote, ordered_list_to_html_node, paragraph_to_html_node, quote_to_html_node, unordered_list_to_html_node)

class TestMarkdownToHTML(unittest.TestCase):
    def test_markdown_to_blocks(self):
        markdown = """
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line




* This is a list
* with items
"""
        blocks = markdown_to_blocks(markdown)
        self.assertEqual([
"This is **bolded** paragraph",
"""This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line""",
"""* This is a list
* with items""",
        ], blocks)
        
    def test_block_to_block_type_heading(self):
        heading_block = "### This is a 3rd heading"
        run = block_to_block_type(heading_block)
        self.assertEqual(block_type_heading, run)

    def test_block_to_block_type_code(self):
        code_block = "```code_block```"
        run = block_to_block_type(code_block)
        self.assertEqual(block_type_code, run)

    def test_block_to_block_type_quote(self):
        quote_block = "> quote first line\n> quote second line"
        run = block_to_block_type(quote_block)
        self.assertEqual(block_type_quote, run)

    def test_block_to_block_type_unordered_list(self):
        unordered_block = "* list first line\n* list second line"
        run = block_to_block_type(unordered_block)
        self.assertEqual(block_type_unordered_list, run)

    def test_block_to_block_type_ordered_list(self):
        ordered_block = "1. list first line\n2. list second line"
        run = block_to_block_type(ordered_block)
        self.assertEqual(block_type_ordered_list, run)

    def test_block_to_block_type_paragraph(self):
        paragraph_block = "This is a general paragraph.\nJust another general  paragraph."
        run = block_to_block_type(paragraph_block)
        self.assertEqual(block_type_paragraph, run)



    def test_heading_to_html_node(self):
        heading_block = "### This is a 3rd heading"
        run = heading_to_html_node(heading_block)
        self.assertEqual(LeafNode("h3", "This is a 3rd heading"), run)

    def test_code_to_html_node(self):
        code_block = "```code_block```"
        run = code_to_html_node(code_block)
        self.assertEqual(
            ParentNode("pre", [
                LeafNode("code", "code_block")
            ]), run)

    def test_quote_to_html_node(self):
        quote_block = "> quote first line\n> quote second line"
        run = quote_to_html_node(quote_block)
        self.assertEqual(LeafNode("blockquote", "quote first line\nquote second line"), run)

    def test_unordered_list_to_html_node(self):
        unordered_block = "* list first line\n* list second line"
        run = unordered_list_to_html_node(unordered_block)
        self.assertEqual(ParentNode("ul", [
            LeafNode("li", "list first line"),
            LeafNode("li", "list second line"),
        ]), run)

    def test_ordered_list_to_html_node(self):
        ordered_block = "1. list first line\n2. list second line"
        run = ordered_list_to_html_node(ordered_block)
        self.assertEqual(ParentNode("ol", [
            LeafNode("li", "list first line"),
            LeafNode("li", "list second line"),
        ]), run)

    def test_paragraph_to_html_node(self):
        paragraph_block = "This is a general paragraph.\nJust another general paragraph."
        run = paragraph_to_html_node(paragraph_block)
        self.assertEqual(LeafNode("p", "This is a general paragraph.\nJust another general paragraph."),
                         run)