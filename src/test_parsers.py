import unittest

from parsers import split_nodes_delimiter, extract_markdown_images, extract_markdown_links
from textnode import TextType, TextNode

class TestSplitNodesDelimiter(unittest.TestCase):
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


class TestExtractMarkdownImages(unittest.TestCase):
    def test_extract_images_none(self):
        text = "No images here, sorry! :("
        self.assertListEqual(extract_markdown_images(text), [])

    def test_extract_images_simple(self):
        text = "My cat... ![my cat, Fluffers!](https://coolcats.com/fluffers) ...Fluffers!"
        self.assertListEqual(extract_markdown_images(text), [
            ("my cat, Fluffers!", "https://coolcats.com/fluffers"),
        ])

    def test_extract_images_multiple(self):
        text = "My pets... ![my cat, Fluffers!](https://coolcats.com/fluffers) Fluffers and ![my dog, Tony!](https://cooldogs.com/tony) Tony!"
        self.assertListEqual(extract_markdown_images(text), [
            ("my cat, Fluffers!", "https://coolcats.com/fluffers"),
            ("my dog, Tony!", "https://cooldogs.com/tony"),
        ])

    def test_extract_images_malformed(self):
        text1 = "My cat... !(my cat, Fluffers!)[https://coolcats.com/fluffers] ...Fluffers!"
        text2 = "My cat... ![my cat, Fluffers!](https://coolcats.com/fluffers] ...Fluffers!"
        text3 = "My cat... ![my cat, Fluffers!(https://coolcats.com/fluffers)] ...Fluffers!"
        text4 = "My cat... [my cat, Fluffers!(https://coolcats.com/fluffers)] ...Fluffers!"
        self.assertListEqual(extract_markdown_images(text1), [])
        self.assertListEqual(extract_markdown_images(text2), [])
        self.assertListEqual(extract_markdown_images(text3), [])
        self.assertListEqual(extract_markdown_images(text4), [])


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_extract_links_none(self):
        text = "No links here, sorry! :("
        self.assertListEqual(extract_markdown_links(text), [])

    def test_extract_links_simple(self):
        text = "[Click here](https://coolcats.com/fluffers) to go to the blog for my cat, Fluffers!"
        self.assertListEqual(extract_markdown_links(text), [
            ("Click here", "https://coolcats.com/fluffers"),
        ])

    def test_extract_links_multiple(self):
        text = "Check out the blogs for [my cat, Fluffers](https://coolcats.com/fluffers) and [my dog, Tony](https://cooldogs.com/tony)!"
        self.assertListEqual(extract_markdown_links(text), [
            ("my cat, Fluffers", "https://coolcats.com/fluffers"),
            ("my dog, Tony", "https://cooldogs.com/tony"),
        ])

    def test_extract_links_malformed(self):
        text1 = "(Click here)[https://coolcats.com/fluffers] to go to the blog for my cat, Fluffers!"
        text2 = "[Click here](https://coolcats.com/fluffers] to go to the blog for my cat, Fluffers!"
        text3 = "[Click here(https://coolcats.com/fluffers)] to go to the blog for my cat, Fluffers!"
        self.assertListEqual(extract_markdown_links(text1), [])
        self.assertListEqual(extract_markdown_links(text2), [])
        self.assertListEqual(extract_markdown_links(text3), [])

