from htmlnode import LeafNode

text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"


class TextNode:
    def __init__(self, text, text_type, url=None) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other_node) -> bool:
        return (
            self.text == other_node.text
            and self.text_type == other_node.text_type
            and self.url == other_node.url
        )

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


def text_node_to_html_node(text_node):
    text = text_node.text
    match text_node.text_type:
        case "text":
            return LeafNode(None, text)
        case "bold":
            return LeafNode("b", text)
        case "italic":
            return LeafNode("i", text)
        case "code":
            return LeafNode("code", text)
        case "link":
            return LeafNode("a", text, {"href": text_node.url})
        case "image":
            return LeafNode("img", "", {"src": text_node.url, "alt": text})
        case _:
            raise ValueError(f"Invalid text type: {text_node.text_type}")
