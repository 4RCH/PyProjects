import unittest
import texttypes as tt
from textnode import TextNode
from textnode_markdown import split_nodes_delimiter

class TestMarkdown(unittest.TestCase):
    def test_bold(self):
        node0 = TextNode("This is text with a **bold words** word tag.", tt.text_type_bold)
        splitnode = split_nodes_delimiter([node0], tt.delimiter_bold, tt.text_type_bold)
        self.assertEqual(str(splitnode), "[Textnode This is text with a , text, None, Textnode bold words, bold, None, Textnode  word tag., text, None]" )

    def test_text(self):
        node1 = TextNode("This is text without tags.", tt.text_type_text)
        splitnode = split_nodes_delimiter([node1], tt.delimiter_bold, tt.text_type_text)
        self.assertEqual(str(splitnode), "[Textnode This is text without tags., text, None]")
    
    def test_italic(self):
        node2 = TextNode("This is text with *italic* tags.", tt.text_type_italic)
        splitnode = split_nodes_delimiter([node2], tt.delimiter_italics, tt.text_type_italic)
        self.assertEqual(str(splitnode), "[Textnode This is text with , text, None, Textnode italic, italic, None, Textnode  tags., text, None]")

    def test_code(self):
        node3 = TextNode("New is text with `code` tags.", tt.text_type_code)
        splitnode = split_nodes_delimiter([node3], tt.delimiter_code, tt.text_type_code)
        self.assertEqual(str(splitnode), "[Textnode New is text with , text, None, Textnode code, code, None, Textnode  tags., text, None]")

    def test_missing_markdown(self):
        node3 = TextNode("This * isn't a tag.", tt.text_type_italic)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node3], tt.delimiter_italics, tt.text_type_italic)

if __name__ == "__main__":
    unittest.main()