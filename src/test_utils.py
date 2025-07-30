
import unittest

from utils import *
from textnode import TextNode, TextType

class TestUtils(unittest.TestCase):
    def test_split_nodes_delimiter_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ])

    def test_split_nodes_delimiter_bold(self):
        node = TextNode("This is a **very important part** of this paragraph", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [
            TextNode("This is a ", TextType.TEXT),
            TextNode("very important part", TextType.BOLD),
            TextNode(" of this paragraph", TextType.TEXT),
        ])
        
    def test_split_nodes_delimiter_italic(self):
        node = TextNode("The last part of this phrase is in _italic text_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(new_nodes, [
            TextNode("The last part of this phrase is in ", TextType.TEXT),
            TextNode("italic text", TextType.ITALIC),
            TextNode("", TextType.TEXT)
        ])

    def test_split_nodes_delimiter_multiple_bold(self):
        node = TextNode("**HTML** and **CSS** are more difficult than **Rust**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [
            TextNode("", TextType.TEXT),
            TextNode("HTML", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("CSS", TextType.BOLD),
            TextNode(" are more difficult than ", TextType.TEXT),
            TextNode("Rust", TextType.BOLD),
            TextNode("", TextType.TEXT),
        ])

    def test_split_nodes_delimiter_multiple_nodes(self):
        node = TextNode("This is a **first paragraph** with bold text", TextType.TEXT)
        node2 = TextNode("This is a **second paragraph** with bold text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node, node2], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [
            TextNode("This is a ", TextType.TEXT),
            TextNode("first paragraph", TextType.BOLD),
            TextNode(" with bold text", TextType.TEXT),
            TextNode("This is a ", TextType.TEXT),
            TextNode("second paragraph", TextType.BOLD),
            TextNode(" with bold text", TextType.TEXT),
        ])

    def test_split_nodes_delimiter_invalid_markdown(self):
        with self.assertRaises(ValueError):
            node = TextNode("This is a **first paragraph with bold text", TextType.TEXT)
            new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_split_nodes_delimiter_consecutive_blocks(self):
        node = TextNode("**a** **b**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [
            TextNode("", TextType.TEXT),
            TextNode("a", TextType.BOLD),
            TextNode(" ", TextType.TEXT),
            TextNode("b", TextType.BOLD),
            TextNode("", TextType.TEXT)  
        ])

    def test_split_nodes_delimiter_no_delimiter(self):
            node = TextNode("This is simple text with no delimiter", TextType.TEXT)
            new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
            self.assertEqual(new_nodes, [
                TextNode("This is simple text with no delimiter", TextType.TEXT),
            ])

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_markdown_images_wrong_md(self):
        matches = extract_markdown_images(
            "This is text with an [image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertEqual([], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with an [link](https://www.boot.dev)"
        )
        self.assertListEqual([("link", "https://www.boot.dev")], matches)
    
    def test_extract_markdown_links_wrong_md(self):
        matches = extract_markdown_links(
            "This is text with an [link(https://www.boot.dev)"
        )
        self.assertEqual([], matches)
    
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png).",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
                TextNode(".", TextType.TEXT),
            ],
            new_nodes,
        )
    
    def test_split_images_multiple_nodes(self):
        node1 = TextNode(
            "This is node 1 with an ![image](https://i.imgur.com/zjjcJKZ.png).",
            TextType.TEXT
        )
        node2 = TextNode(
            "This is node 2 with the same ![image](https://i.imgur.com/zjjcJKZ.png).",
            TextType.TEXT
        )
        new_nodes = split_nodes_image([node1, node2])
        self.assertListEqual(
            [
                TextNode("This is node 1 with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(".", TextType.TEXT),
                TextNode("This is node 2 with the same ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(".", TextType.TEXT)
            ],
            new_nodes
        )

    def test_split_links(self):
        node = TextNode(
            "This is some text with a [google](https://www.google.com) link and another to [boot.dev](https://www.boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is some text with a ", TextType.TEXT),
                TextNode("google", TextType.LINK, "https://www.google.com"),
                TextNode(" link and another to ", TextType.TEXT),
                TextNode("boot.dev", TextType.LINK, "https://www.boot.dev"),
            ],
            new_nodes
        )
    
    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual([
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev")
            ], 
            new_nodes
        )