import unittest

from leafnode import LeafNode
from parentnode import ParentNode

class TestParentNode(unittest.TestCase):
    def test_eq_single_child(self):
        child = LeafNode("p", "Hello world!")
        node = ParentNode("div", [child])
        node2 = ParentNode("div", [child])
        self.assertEqual(node, node2)

    def test_eq_separate_children(self):
        node = ParentNode("div", [LeafNode("p", "Hello World!")])
        node2 = ParentNode("div", [LeafNode("p", "Hello World!")])
        self.assertEqual(node, node2)

    def test_eq_multiple_children(self):
        node = ParentNode("div", [
            LeafNode("p", "Hello World!"),
            LeafNode("p", "Hello World!"),
        ])
        node2 = ParentNode("div", [
            LeafNode("p", "Hello World!"),
            LeafNode("p", "Hello World!"),
        ])
        self.assertEqual(node, node2)

    def test_eq_with_tagless_children(self):
        node = ParentNode("div", [
            LeafNode(None, "Someone close that window!"),
        ])
        node2 = ParentNode("div", [
            LeafNode(None, "Someone close that window!"),
        ])
        self.assertEqual(node, node2)

    def test_eq_with_children_props(self):
        node = ParentNode("div", [
            LeafNode("p", "Hello World!", {"style": "color: red;"}),
            LeafNode("p", "Hello World!", {"style": "color: red;"}),
        ])
        node2 = ParentNode("div", [
            LeafNode("p", "Hello World!", {"style": "color: red;"}),
            LeafNode("p", "Hello World!", {"style": "color: red;"}),
        ])
        self.assertEqual(node, node2)

    def test_to_html(self):
        node = ParentNode("div", [LeafNode("p", "Hello world!")])
        self.assertEqual(node.to_html(), '<div><p>Hello world!</p></div>')

    def test_to_html_multiple_children(self):
        node = ParentNode("div", [
            LeafNode("p", "Hello world!"),
            LeafNode("em", "Goodbye galaxy!"),
        ])
        self.assertEqual(node.to_html(), '<div><p>Hello world!</p><em>Goodbye galaxy!</em></div>')

    def test_to_html_with_grandchildren(self):
        node = ParentNode("section", [
            ParentNode("div", [
                LeafNode("p", "Hello from down here!"),
            ])
        ])
        self.assertEqual(node.to_html(), '<section><div><p>Hello from down here!</p></div></section>')

    def test_to_html_with_tagless_children(self):
        node = ParentNode("div", [
            LeafNode(None, "I think we are "),
            LeafNode(None, "stuck together!"),
        ])
        self.assertEqual(node.to_html(), '<div>I think we are stuck together!</div>')

    def test_to_html_with_mixed_tag_children(self):
        node = ParentNode("div", [
            LeafNode(None, "Someone "),
            LeafNode("em", "really"),
            LeafNode(None, " needs to do something about that "),
            LeafNode("strong", "zergling running around in my base!!"),
        ])
        self.assertEqual(node.to_html(), '<div>Someone <em>really</em> needs to do something about that <strong>zergling running around in my base!!</strong></div>')

    def test_to_html_with_mix_of_descendants(self):
        node = ParentNode("article", [
            LeafNode("h1", "Chapter 1"),
            ParentNode("section", [
                ParentNode("p", [
                    LeafNode(None, "Once upon a time, humans and monsters lived in "),
                    LeafNode("em", "peace."),
                ]),
                LeafNode("aside", "You wanna have a bad time?"),
            ]),
            ParentNode("h1", [
                LeafNode("a", "Chapter 2", {"href": "https://en.wikipedia.org/wiki/Undertale", "target": "_blank"})
            ]),
            ParentNode("section", [
                LeafNode(None, "One day, "),
                ParentNode("em", [
                    LeafNode("strong", "they all disappeared without a trace."),
                ]),
            ])
        ])
        self.assertEqual(node.to_html(), '<article><h1>Chapter 1</h1><section><p>Once upon a time, humans and monsters lived in <em>peace.</em></p><aside>You wanna have a bad time?</aside></section><h1><a href="https://en.wikipedia.org/wiki/Undertale" target="_blank">Chapter 2</a></h1><section>One day, <em><strong>they all disappeared without a trace.</strong></em></section></article>')

