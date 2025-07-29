import unittest

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertEqual(node, node2)

    def test_url_prop(self):
        node = TextNode("This is a text node", TextType.ITALIC_TEXT)
        node2 = TextNode("This is a text node", TextType.ITALIC_TEXT, "https://www.boot.dev")
        self.assertIsNone(node.url)
        self.assertIsNotNone(node2.url)

    def test_wrong_texttype(self):
        with self.assertRaises(TypeError):
            node = TextNode("This is a text node", "string")

    def test_ne(self):
        node = TextNode("This is a text node", TextType.CODE_TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        
        node3 = TextNode("This is a text node", TextType.BOLD_TEXT, "https://www.google.com")
        node4 = TextNode("This is a text node", TextType.BOLD_TEXT, "https://www.facebook.com")
        self.assertNotEqual(node, node2)
        self.assertNotEqual(node3, node4)

if __name__ == "__main__":
    unittest.main()