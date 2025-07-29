
import unittest

from utils import split_nodes_delimiter
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
