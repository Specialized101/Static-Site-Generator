import re

from textnode import *
from htmlnode import HTMLNode

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

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)

    return nodes

def markdown_to_blocks(markdown):
    # blocks = list(map(lambda s: s.strip(), markdown.split("\n\n")))
    blocks = [block.strip() for block in markdown.split("\n\n") if block.strip() != ""]
    return blocks

def block_to_block_type(markdown):
    if re.match(r"^#{1,6} .*?$", markdown):
        return BlockType.HEADING
    if markdown.startswith("```") and markdown.endswith("```"):
        return BlockType.CODE
    lines = markdown.split("\n")
    is_quote = True
    is_ul = True
    is_ol = True
    i = 1
    for line in lines:
        if not line.startswith(">"):
            is_quote = False
        if not line.startswith("- "):
            is_ul = False
        if not line.startswith(f"{i}. "):
            is_ol = False
            
        i += 1
        
    if is_quote:
        return BlockType.QUOTE
    if is_ul:
        return BlockType.UNORDERED_LIST
    if is_ol:
        return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH
    
def markdown_to_html_node(markdown):
    parent = HTMLNode("div", None, [])
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.HEADING:
                parent.children.append(markdown_heading_to_html_heading(block))
            case BlockType.QUOTE:
                parent.children.append(markdown_quote_to_html_quote(block))
            case BlockType.UNORDERED_LIST:
                parent.children.append(markdown_ul_to_html_ul(block))
            case BlockType.ORDERED_LIST:
                parent.children.append(markdown_ol_to_html_ol(block))
            case BlockType.CODE:
                parent.children.append(markdown_code_to_html_code(block))
            case _:
                parent.children.append(markdown_p_to_html_p(block))

    return parent

def markdown_heading_to_html_heading(markdown):
    splits = markdown.split(" ", 1)
    hashtag_count = splits[0].count("#")
    return HTMLNode(f"h{hashtag_count}", None, text_to_children(splits[1]))

def markdown_quote_to_html_quote(markdown):
    lines = markdown.split("\n")
    text = "\n".join(list(map(lambda s: s[1:].strip(), lines)))
    return HTMLNode("blockquote", None, text_to_children(text))

def markdown_ul_to_html_ul(markdown):
    lines = markdown.split("\n")
    li_nodes = []
    for line in lines:
        li_nodes.append(HTMLNode("li", None, text_to_children(line[1:].strip())))
    return HTMLNode("ul", None, li_nodes)

def markdown_ol_to_html_ol(markdown):
    lines = markdown.split("\n")
    ol_nodes = []
    for line in lines:
        ol_nodes.append(HTMLNode("li", None, text_to_children(line.split(" ", 1)[1].strip())))
    return HTMLNode("ol", None, ol_nodes)

def markdown_code_to_html_code(markdown):
    code_content = markdown[3:-3].strip()
    code_node = HTMLNode("code", code_content)
    return HTMLNode("pre", None, [code_node])

def markdown_p_to_html_p(markdown):
    return HTMLNode("p", None, text_to_children(markdown.strip()))

def text_to_children(text):
    textnodes = text_to_textnodes(text)
    htmlnodes = []
    for textnode in textnodes:
        htmlnodes.append(text_node_to_html_node(textnode))
    return htmlnodes

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.strip().startswith("# "):
            return line.strip().replace("# ", "", 1).strip()
    raise Exception("the markdown document is missing a h1 heading")