import unittest

from parsers import split_nodes_delimiter
from textnode import TextType, TextNode

class TestParsers(unittest.TestCase):
    def test_plain(self):
        nodes = [TextNode("Hello world!", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(nodes, '`', TextType.CODE)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "Hello world!")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)

    def test_ignore_non_text(self):
        nodes = [TextNode("Hello _world_!", TextType.BOLD)]
        new_nodes = split_nodes_delimiter(nodes, '_', TextType.ITALIC)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "Hello _world_!")
        self.assertEqual(new_nodes[0].text_type, TextType.BOLD)

    def test_long_delimiter(self):
        nodes = [TextNode("Hello ~!~world~!~!", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(nodes, '~!~', TextType.BOLD)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "Hello ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "world")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[2].text, "!")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)

    def test_multiple_splits(self):
        nodes = [TextNode("He_llo_ _world_!", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(nodes, '_', TextType.ITALIC)
        self.assertEqual(len(new_nodes), 5)
        self.assertEqual(new_nodes[0].text, "He")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "llo")
        self.assertEqual(new_nodes[1].text_type, TextType.ITALIC)
        self.assertEqual(new_nodes[2].text, " ")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[3].text, "world")
        self.assertEqual(new_nodes[3].text_type, TextType.ITALIC)
        self.assertEqual(new_nodes[4].text, "!")
        self.assertEqual(new_nodes[4].text_type, TextType.TEXT)

    def test_multiple_nodes(self):
        nodes = [TextNode("Hello *world*!", TextType.TEXT), TextNode("Good*bye* *galaxy!*", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(nodes, '*', TextType.BOLD)
        self.assertEqual(len(new_nodes), 7)
        self.assertEqual(new_nodes[0].text, "Hello ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "world")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[2].text, "!")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[3].text, "Good")
        self.assertEqual(new_nodes[3].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[4].text, "bye")
        self.assertEqual(new_nodes[4].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[5].text, " ")
        self.assertEqual(new_nodes[5].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[6].text, "galaxy!")
        self.assertEqual(new_nodes[6].text_type, TextType.BOLD)

    def test_ignore_empty_strings_at_end(self):
        nodes = [TextNode("*Hello world!*", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(nodes, '*', TextType.BOLD)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "Hello world!")
        self.assertEqual(new_nodes[0].text_type, TextType.BOLD)

    def test_ignore_empty_strings_in_middle(self):
        # TODO: Change the algorithm to combine both resulting halves in a single TextNode
        nodes = [TextNode("Hello **world!", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(nodes, '*', TextType.BOLD)
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[0].text, "Hello ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "world!")
        self.assertEqual(new_nodes[1].text_type, TextType.TEXT)

