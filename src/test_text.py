import unittest

from textnode import TextType, TextNode, text_node_to_html_node

class TestText(unittest.TestCase):
    def test_text_plain(self):
        node = TextNode("Hello world!", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "Hello world!")
        self.assertEqual(html_node.props, None)

    def test_text_bold(self):
        node = TextNode("Hello world!", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Hello world!")
        self.assertEqual(html_node.props, None)

    def test_text_italic(self):
        node = TextNode("Hello world!", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Hello world!")
        self.assertEqual(html_node.props, None)

    def test_text_code(self):
        node = TextNode("Hello world!", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "Hello world!")
        self.assertEqual(html_node.props, None)

    def test_text_link(self):
        node = TextNode("Hello world!", TextType.LINK, "https://selevas.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Hello world!")
        self.assertEqual(html_node.props, {"href": "https://selevas.com"})

    def test_text_image(self):
        node = TextNode("Hello world!", TextType.IMAGE, "https://selevas.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://selevas.com", "alt": "Hello world!"})


