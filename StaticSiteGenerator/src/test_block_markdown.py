import unittest
import data_constants as tt
from block_markdown import markdown_to_blocks, block_to_blocktype

block_types = [
            tt.markdown_paragraph,
            tt.markdown_heading,
            tt.markdown_code,
            tt.markdown_quote,
            tt.markdown_un_list,
            tt.markdown_ord_list,
            ]

blocks = [
    '# This is a heading',
    'This is a paragraph of text. It has some **bold** and *italic* words inside of it.',
    '* This is the first list item in a list block\n* This is a list item\n* This is another list item',
    '1. This is another list item in a list block\n2. This is a list item\n3. This is another list item',
    ]

class TestBlockMarkdown(unittest.TestCase):

    def setUp(self):
        with open("./src/markdown.md", "r", encoding="UTF-8") as block_list:
            self.markdown_content = block_list.read()
        
    
    def test_markdown_to_blocks(self):
        self.assertEqual(markdown_to_blocks(self.markdown_content), blocks)

    def test_markdown_to_block_to_types(self):
        for block in blocks:
            self.assertIn(block_to_blocktype(block), block_types)
    
    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(block_to_blocktype(block), tt.markdown_heading)
        block = "```\ncode\n```"
        self.assertEqual(block_to_blocktype(block), tt.markdown_code)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_blocktype(block), tt.markdown_quote)
        block = "* list\n* items"
        self.assertEqual(block_to_blocktype(block), tt.markdown_un_list)
        block = "1. list\n2. items"
        self.assertEqual(block_to_blocktype(block), tt.markdown_ord_list)
        block = "paragraph"
        self.assertEqual(block_to_blocktype(block), tt.markdown_paragraph)

if __name__ == "__main__":
    unittest.main()