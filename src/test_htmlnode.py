import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("p", "Hello world!")
        # node2 = HTMLNode("p", "Hello world!")
        node2 = HTMLNode("p", "Hello world!")
        self.assertEqual(node, node2)
    def test_tag_not_eq(self):
        node = HTMLNode("p", "Hello world!")
        node2 = HTMLNode("div", "Hello world!")
        self.assertNotEqual(node, node2)
    def test_value_not_eq(self):
        node = HTMLNode("p", "Hello world!")
        node2 = HTMLNode("p", "Hello universe!")
        self.assertNotEqual(node, node2)
    def test_props_not_eq(self):
        node = HTMLNode("a", "Hello world!", props={"href": "https://selevas.com"})
        node2 = HTMLNode("a", "Hello world!", props={"href": "https://google.com"})
        node3 = HTMLNode("a", "Hello world!", props={"href": "https://selevas.com", "target": "_blank"})
        self.assertNotEqual(node, node2)
        self.assertNotEqual(node, node3)
        self.assertNotEqual(node2, node3)
    def test_to_html(self):
        node = HTMLNode("a", "Hello world!")
        node2 = HTMLNode("a", "Hello world!", props={"href": "https://selevas.com"})
        node3 = HTMLNode("a", "Hello world!", props={"href": "https://selevas.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), "")
        self.assertEqual(node2.props_to_html(), ' href="https://selevas.com"')
        self.assertEqual(node3.props_to_html(), ' href="https://selevas.com" target="_blank"')


if __name__ == "__main__":
    unittest.main()
