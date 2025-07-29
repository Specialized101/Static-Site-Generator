import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("a", "boot.dev", [], {"href": "https://www.boot.dev"})
        node2 = HTMLNode("a", "boot.dev", [], {"href": "https://www.boot.dev"})
        self.assertEqual(node, node2)

    def test_ne(self):
        node = HTMLNode("a", "boot.dev", [], {"href": "https://www.google.com"})
        node2 = HTMLNode("a", "boot.dev", [], {"href": "https://www.boot.dev"})
        
        node3 = HTMLNode("p", "This is a paragraph with a link", [node], {"class": "main-p"})
        node4 = HTMLNode("p", "This is a paragraph with a link", [node2], {"class": "main-p"})
        
        self.assertNotEqual(node, node2)
        self.assertNotEqual(node3, node4)

    def test_props_to_html(self):
        node = HTMLNode("div", "This is a div container", [], {"class": "main", "id": "main"})
        self.assertEqual(node.props_to_html(), ' class="main" id="main"')
        
    def test_repr(self):
        node = HTMLNode("div", "This is a div container", [], {"class": "main", "id": "main"})
        expected_output = "HTMLNode(div, This is a div container, [], {'class': 'main', 'id': 'main'})"
        node2 = HTMLNode("div", "This is a div container", [node], {"class": "main", "id": "main"})
        expected_output2 = "HTMLNode(div, This is a div container, ['HTMLNode(div, This is a div container, [], {'class': 'main', 'id': 'main'})'], {'class': 'main', 'id': 'main'})"
        self.assertEqual(repr(node), expected_output)