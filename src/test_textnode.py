import unittest

from textnode import *

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_url_prop(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.ITALIC, "https://www.boot.dev")
        self.assertIsNone(node.url)
        self.assertIsNotNone(node2.url)

    def test_wrong_texttype(self):
        with self.assertRaises(TypeError):
            node = TextNode("This is a text node", "string")

    def test_ne(self):
        node = TextNode("This is a text node", TextType.CODE)
        node2 = TextNode("This is a text node", TextType.BOLD)
        
        node3 = TextNode("This is a text node", TextType.BOLD, "https://www.google.com")
        node4 = TextNode("This is a text node", TextType.BOLD, "https://www.facebook.com")
        self.assertNotEqual(node, node2)
        self.assertNotEqual(node3, node4)

    def test_text_node_to_html_node_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_node_to_html_node_image(self):
        node = TextNode("This is blank image", TextType.IMAGE, "/home/speci/images/001.jpg")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), '<img src="/home/speci/images/001.jpg" alt="This is blank image"></img>')

    def test_text_node_to_html_node_link(self):
        node = TextNode("boot.dev", TextType.LINK, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), '<a href="https://www.boot.dev">boot.dev</a>')

if __name__ == "__main__":
    unittest.main()