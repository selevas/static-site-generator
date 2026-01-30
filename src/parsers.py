import re

from textnode import TextType, TextNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        parts = node.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise Exception(f'The text "{node.text}" contains a mismatched \'{delimiter}\'.')
        for idx, part in enumerate(parts):
            if part == "":
                continue
            if idx % 2 == 0:
                new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                new_nodes.append(TextNode(part, text_type)) 
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        remaining_text = node.text
        images = extract_markdown_images(remaining_text)
        for image in images:
            previous_text, remaining_text = remaining_text.split(f"![{image[0]}]({image[1]})", maxsplit=1)
            if previous_text != "":
                new_nodes.append(TextNode(previous_text, TextType.TEXT))
            new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
        if remaining_text != "":
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        remaining_text = node.text
        links = extract_markdown_links(remaining_text)
        for link in links:
            previous_text, remaining_text = remaining_text.split(f"[{link[0]}]({link[1]})", maxsplit=1)
            if previous_text != "":
                new_nodes.append(TextNode(previous_text, TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
        if remaining_text != "":
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes

