import unittest
from textnode import TextNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold", "http://www.google.com")
        node2 = TextNode("This is a text node", "bold", "http://www.google.com")
        self.assertEqual(node, node2)

    def test_stringtext(self):
        node = TextNode(0, "bold", "http://www.google.com")
        self.assertNotIsInstance(node.text, str, "Textnode is not a string")

    def test_none_url(self):
        node = TextNode("This is a text node", "bold", None)
        self.assertIsNone(node.url, "Textnode.url is None")

    def test_emptyurl(self):
        node = TextNode("This is a text node", "bold", "")
        self.assertIs(node.url, "")

    def test_badStyle(self):
        node = TextNode("This is a text node", "c0de", "http://www.google.com")
        valid_types = ["text", "bold", "italic", "code", "link", "image"]
        self.assertNotIn(node.text_type, valid_types, "Invalid text_type")
    

if __name__ == "__main__":
    unittest.main()