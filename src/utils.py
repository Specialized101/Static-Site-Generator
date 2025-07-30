import re

from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        count = node.text.count(delimiter)
        if count == 0:
            new_nodes.append(node)
            continue
        
        if count % 2 != 0:
            raise ValueError(f"Incorrect markdown syntax, received: {node.text}")
        
        node_splits = node.text.split(delimiter)
        for i in range(len(node_splits)):
            if i % 2 == 0:
                new_nodes.append(TextNode(node_splits[i], TextType.TEXT))
            else:
                new_nodes.append(TextNode(node_splits[i], text_type))

    return new_nodes

def extract_markdown_images(text):
    # matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    # matches = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        images = extract_markdown_images(node.text)
        if not images:
            new_nodes.append(node)
            continue
        
        current_text = node.text
        for image in images:
            sections = current_text.split(f"![{image[0]}]({image[1]})", 1)
            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
            current_text = sections[1]

        if current_text:
            new_nodes.append(TextNode(current_text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        links = extract_markdown_links(node.text)
        if not links:
            new_nodes.append(node)
            continue
        
        current_text = node.text
        for link in links:
            sections = current_text.split(f"[{link[0]}]({link[1]})", 1)
            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            current_text = sections[1]

        if current_text:
            new_nodes.append(TextNode(current_text, TextType.TEXT))
    return new_nodes
