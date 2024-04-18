import unittest

from inline_markdown import (extract_markdown_images, extract_markdown_links,
                             split_nodes_delimiter, split_nodes_image, split_nodes_link)
from textnode import (TextNode, text_type_bold, text_type_code,
                      text_type_italic, text_type_text, text_type_image, text_type_link)


class TestInlineMarkdown(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("bolded", text_type_bold),
                TextNode(" word", text_type_text),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", text_type_text
        )
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("bolded", text_type_bold),
                TextNode(" word and ", text_type_text),
                TextNode("another", text_type_bold),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", text_type_text
        )
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("bolded word", text_type_bold),
                TextNode(" and ", text_type_text),
                TextNode("another", text_type_bold),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an *italic* word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "*", text_type_italic)
        self.assertListEqual(
            [
                TextNode("This is text with an ", text_type_text),
                TextNode("italic", text_type_italic),
                TextNode(" word", text_type_text),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "`", text_type_code)
        self.assertListEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("code block", text_type_code),
                TextNode(" word", text_type_text),
            ],
            new_nodes,
        )

    def test_delim_images(self):
        no_images = TextNode("There are no images in this text", text_type_text)
        no_images_answer = split_nodes_image([no_images])
        self.assertEqual(
            [
                TextNode("There are no images in this text", text_type_text)
            ],
            no_images_answer
        )

        node = TextNode(
            "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
            text_type_text,
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            [
                TextNode("This is text with an ", text_type_text),
                TextNode("image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
                TextNode(" and another ", text_type_text),
                TextNode(
                    "second image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

        node_with_extra_content = TextNode(
            "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png). Isn't this awesome!",
            text_type_text,
        )

        new_nodes_extra = split_nodes_image([node_with_extra_content])
        self.assertEqual(
            [
                TextNode("This is text with an ", text_type_text),
                TextNode("image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
                TextNode(" and another ", text_type_text),
                TextNode(
                    "second image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png"
                ),
                TextNode(". Isn't this awesome!", text_type_text),
            ],
            new_nodes_extra,
        )

        node_image_first = TextNode(
            "![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png). Isn't this awesome!",
            text_type_text
        )
        new_node_image_first = split_nodes_image([node_image_first])
        self.assertEqual(
            [
                TextNode("image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
                TextNode(" and another ", text_type_text),
                TextNode(
                    "second image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png"
                ),
                TextNode(". Isn't this awesome!", text_type_text),
            ],
            new_node_image_first,
        )

    def test_delim_links(self):
        node = TextNode(
            "This is a website with [Google](https://www.google.com) and another [Games Database](https://games.linuxhg.com)",
            text_type_text,
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            [
                TextNode("This is a website with ", text_type_text),
                TextNode("Google", text_type_link, "https://www.google.com"),
                TextNode(" and another ", text_type_text),
                TextNode("Games Database", text_type_link, "https://games.linuxhg.com"),
            ],
            new_nodes,
        )

        node_with_extra_content = TextNode(
            "This is a website with [Google](https://www.google.com) and another [Games Database](https://games.linuxhg.com). Isn't this awesome!",
            text_type_text,
        )

        new_nodes_extra = split_nodes_link([node_with_extra_content])
        self.assertEqual(
            [
                TextNode("This is a website with ", text_type_text),
                TextNode("Google", text_type_link, "https://www.google.com"),
                TextNode(" and another ", text_type_text),
                TextNode("Games Database", text_type_link, "https://games.linuxhg.com"),
                TextNode(". Isn't this awesome!", text_type_text),
            ],
            new_nodes_extra,
        )



def test_extract_markdown_images(self):
    matches = extract_markdown_images(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
    )
    self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)


def test_extract_markdown_links(self):
    matches = extract_markdown_links(
        "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev)"
    )
    self.assertListEqual(
        [
            ("link", "https://boot.dev"),
            ("another link", "https://blog.boot.dev"),
        ],
        matches,
    )


if __name__ == "__main__":
    unittest.main()
