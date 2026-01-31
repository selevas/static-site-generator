import unittest

from parsers import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_text_nodes
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


class TestSplitMarkdownImages(unittest.TestCase):
    def test_split_images_none(self):
        nodes = [TextNode("No images here, sorry! :(", TextType.TEXT)]
        self.assertListEqual(split_nodes_image(nodes), [
            TextNode("No images here, sorry! :(", TextType.TEXT),
        ])

    def test_split_images_simple(self):
        nodes = [TextNode("My cat... ![my cat, Fluffers!](https://coolcats.com/fluffers) ...Fluffers!", TextType.TEXT)]
        self.assertListEqual(split_nodes_image(nodes), [
            TextNode("My cat... ", TextType.TEXT),
            TextNode("my cat, Fluffers!", TextType.IMAGE, "https://coolcats.com/fluffers"),
            TextNode(" ...Fluffers!", TextType.TEXT),
        ])

    def test_split_links_multiple(self):
        nodes = [TextNode("My pets... ![my cat, Fluffers!](https://coolcats.com/fluffers) Fluffers and ![my dog, Tony!](https://cooldogs.com/tony) Tony!", TextType.TEXT)]
        self.assertListEqual(split_nodes_image(nodes), [
            TextNode("My pets... ", TextType.TEXT),
            TextNode("my cat, Fluffers!", TextType.IMAGE, "https://coolcats.com/fluffers"),
            TextNode(" Fluffers and ", TextType.TEXT),
            TextNode("my dog, Tony!", TextType.IMAGE, "https://cooldogs.com/tony"),
            TextNode(" Tony!", TextType.TEXT),
        ])

    def test_split_links_malformed(self):
        nodes1 = [TextNode("My cat... !(my cat, Fluffers!)[https://coolcats.com/fluffers] ...Fluffers!", TextType.TEXT)]
        nodes2 = [TextNode("My cat... ![my cat, Fluffers!](https://coolcats.com/fluffers] ...Fluffers!", TextType.TEXT)]
        nodes3 = [TextNode("My cat... ![my cat, Fluffers!(https://coolcats.com/fluffers)] ...Fluffers!", TextType.TEXT)]
        nodes4 = [TextNode("My cat... [my cat, Fluffers!(https://coolcats.com/fluffers)] ...Fluffers!", TextType.TEXT)]
        self.assertListEqual(split_nodes_image(nodes1), [TextNode("My cat... !(my cat, Fluffers!)[https://coolcats.com/fluffers] ...Fluffers!", TextType.TEXT)])
        self.assertListEqual(split_nodes_image(nodes2), [TextNode("My cat... ![my cat, Fluffers!](https://coolcats.com/fluffers] ...Fluffers!", TextType.TEXT)])
        self.assertListEqual(split_nodes_image(nodes3), [TextNode("My cat... ![my cat, Fluffers!(https://coolcats.com/fluffers)] ...Fluffers!", TextType.TEXT)])
        self.assertListEqual(split_nodes_image(nodes4), [TextNode("My cat... [my cat, Fluffers!(https://coolcats.com/fluffers)] ...Fluffers!", TextType.TEXT)])

class TestSplitMarkdownLinks(unittest.TestCase):
    def test_split_links_none(self):
        nodes = [TextNode("No links here, sorry! :(", TextType.TEXT)]
        self.assertListEqual(split_nodes_link(nodes), [
            TextNode("No links here, sorry! :(", TextType.TEXT),
        ])

    def test_split_links_simple(self):
        nodes = [TextNode("[Click here](https://coolcats.com/fluffers) to go to the blog for my cat, Fluffers!", TextType.TEXT)]
        self.assertListEqual(split_nodes_link(nodes), [
            TextNode("Click here", TextType.LINK, "https://coolcats.com/fluffers"),
            TextNode(" to go to the blog for my cat, Fluffers!", TextType.TEXT),
        ])

    def test_split_links_multiple(self):
        nodes = [TextNode("Check out the blogs for [my cat, Fluffers](https://coolcats.com/fluffers) and [my dog, Tony](https://cooldogs.com/tony)!", TextType.TEXT)]
        self.assertListEqual(split_nodes_link(nodes), [
            TextNode("Check out the blogs for ", TextType.TEXT),
            TextNode("my cat, Fluffers", TextType.LINK, "https://coolcats.com/fluffers"),
            TextNode(" and ", TextType.TEXT),
            TextNode("my dog, Tony", TextType.LINK, "https://cooldogs.com/tony"),
            TextNode("!", TextType.TEXT),
        ])

    def test_split_links_malformed(self):
        nodes1 = [TextNode("(Click here)[https://coolcats.com/fluffers] to go to the blog for my cat, Fluffers!", TextType.TEXT)]
        nodes2 = [TextNode("[Click here](https://coolcats.com/fluffers] to go to the blog for my cat, Fluffers!", TextType.TEXT)]
        nodes3 = [TextNode("[Click here(https://coolcats.com/fluffers)] to go to the blog for my cat, Fluffers!", TextType.TEXT)]
        self.assertListEqual(split_nodes_link(nodes1), [TextNode("(Click here)[https://coolcats.com/fluffers] to go to the blog for my cat, Fluffers!", TextType.TEXT)])
        self.assertListEqual(split_nodes_link(nodes2), [TextNode("[Click here](https://coolcats.com/fluffers] to go to the blog for my cat, Fluffers!", TextType.TEXT)])
        self.assertListEqual(split_nodes_link(nodes3), [TextNode("[Click here(https://coolcats.com/fluffers)] to go to the blog for my cat, Fluffers!", TextType.TEXT)])


class TestTextToTextNodes(unittest.TestCase):
    def test_empty(self):
        self.assertListEqual(text_to_text_nodes(""), [])

    def test_no_markdown(self):
        self.assertListEqual(text_to_text_nodes("Hello world!"), [TextNode("Hello world!", TextType.TEXT)])

    def test_only_italic(self):
        self.assertListEqual(text_to_text_nodes("I have a _big_ dog."), [
            TextNode("I have a ", TextType.TEXT),
            TextNode("big", TextType.ITALIC),
            TextNode(" dog.", TextType.TEXT),
        ])

    def test_only_bold(self):
        self.assertListEqual(text_to_text_nodes("I have a *big* dog."), [
            TextNode("I have a ", TextType.TEXT),
            TextNode("big", TextType.BOLD),
            TextNode(" dog.", TextType.TEXT),
        ])

    def test_only_code(self):
        self.assertListEqual(text_to_text_nodes("I have a `big` dog."), [
            TextNode("I have a ", TextType.TEXT),
            TextNode("big", TextType.CODE),
            TextNode(" dog.", TextType.TEXT),
        ])

    def test_only_image(self):
        self.assertListEqual(text_to_text_nodes("I have a ![big dog](https://selevas.com)."), [
            TextNode("I have a ", TextType.TEXT),
            TextNode("big dog", TextType.IMAGE, "https://selevas.com"),
            TextNode(".", TextType.TEXT),
        ])

    def test_only_image(self):
        self.assertListEqual(text_to_text_nodes("I have a [website](https://selevas.com) for my dog!"), [
            TextNode("I have a ", TextType.TEXT),
            TextNode("website", TextType.LINK, "https://selevas.com"),
            TextNode(" for my dog!", TextType.TEXT),
        ])

    def test_all_conversions(self):
        self.assertListEqual(text_to_text_nodes("My converter can do _italic_, *bold*, `code`, ![images](https://selevas.com), and [links](https://selevas.com)!"), [
            TextNode("My converter can do ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(", ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(", ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(", ", TextType.TEXT),
            TextNode("images", TextType.IMAGE, "https://selevas.com"),
            TextNode(", and ", TextType.TEXT),
            TextNode("links", TextType.LINK, "https://selevas.com"),
            TextNode("!", TextType.TEXT),
        ])

    def test_all_conversions_reverse(self):
        self.assertListEqual(text_to_text_nodes("My converter can do [links](https://selevas.com), ![images](https://selevas.com), `code`, *bold*, and _italic_!"), [
            TextNode("My converter can do ", TextType.TEXT),
            TextNode("links", TextType.LINK, "https://selevas.com"),
            TextNode(", ", TextType.TEXT),
            TextNode("images", TextType.IMAGE, "https://selevas.com"),
            TextNode(", ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(", ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(", and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode("!", TextType.TEXT),
        ])

    def test_all_conversions_complex(self):
        self.assertListEqual(text_to_text_nodes("We`re` a*bo*ut_ to get_ [crazy](https://selevas.com)!***!*_!__!_![!](https://selevas.com)"), [
            TextNode("We", TextType.TEXT),
            TextNode("re", TextType.CODE),
            TextNode(" a", TextType.TEXT),
            TextNode("bo", TextType.BOLD),
            TextNode("ut", TextType.TEXT),
            TextNode(" to get", TextType.ITALIC),
            TextNode(" ", TextType.TEXT),
            TextNode("crazy", TextType.LINK, "https://selevas.com"),
            TextNode("!", TextType.TEXT),
            TextNode("!", TextType.BOLD),
            TextNode("!", TextType.ITALIC),
            TextNode("!", TextType.ITALIC),
            TextNode("!", TextType.IMAGE, "https://selevas.com"),
        ])

