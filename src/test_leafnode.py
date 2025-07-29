import unittest

from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_leaf_to_html_a(self):
        node = LeafNode("a", "boot.dev", {"href": "https://www.boot.dev"})
        self.assertEqual(node.to_html(), '<a href="https://www.boot.dev">boot.dev</a>')
    
    def test_leaf_no_value(self):
        with self.assertRaises(ValueError):
            node = LeafNode("p", None, {"class": "para"})
            node.to_html()

    def test_leaf_no_tag(self):
        node = LeafNode(None, "boot.dev", {"href": "https://www.boot.dev"})
        self.assertEqual(node.to_html(), "boot.dev")

        