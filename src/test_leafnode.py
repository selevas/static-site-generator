import unittest

from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_eq(self):
        node = LeafNode("p", "Hello world!")
        node2 = LeafNode("p", "Hello world!")
        self.assertEqual(node, node2)

    def test_to_html(self):
        node = LeafNode("p", "Hello world!")
        node2 = LeafNode("div", "Look at this!")
        self.assertEqual(node.to_html(), '<p>Hello world!</p>')
        self.assertEqual(node2.to_html(), '<div>Look at this!</div>')

    def test_to_html_with_props(self):
        node = LeafNode("a", "Staff Profile", {"href": "https://selevas.com"})
        node2 = LeafNode("a", "Management Profile", {"href": "https://selevas.com", "target": "_blank"})
        self.assertEqual(node.to_html(), '<a href="https://selevas.com">Staff Profile</a>')
        self.assertEqual(node2.to_html(), '<a href="https://selevas.com" target="_blank">Management Profile</a>')

