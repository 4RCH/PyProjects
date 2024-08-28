import re
import data_constants as tt

# Break text into blocks
def markdown_to_blocks(markdown):
    pattern = r"\n\s+"
    blocks = []

    lines = re.split(pattern, markdown)
    blocks = [line for line in lines if line.strip()]
    return blocks

# Get a block and return the type 
def block_to_blocktype(markdown_block):
    if not markdown_block:
        raise ValueError("[!] Missing markdown string")
    
    lines = markdown_block.split("\n")
    first_char = markdown_block[0]

    # Check for Heading type
    if first_char == tt.tag_heading:
        for i in range(1, 7):
            if markdown_block.startswith('#' * i + ' '):
                return tt.markdown_heading
    
    # Check for Code type
    if markdown_block.startswith("```") and markdown_block.endswith("```"):
        return tt.markdown_code
    
    # Check for Quote type
    if markdown_block.startswith(tt.tag_quote + ' '):
        if all(line.startswith(f'{tt.tag_quote} ') for line in lines):
            return tt.markdown_quote
    
    # Check for unordered list type
    if markdown_block.startswith(('* ','- ')):
        if all(line.startswith(('* ', '_ ')) for line in lines):                
            return tt.markdown_un_list
    
    # Check for ordered list type
    if markdown_block[0].isdigit and markdown_block[1] == '.':
        count = 1
        if all(line.startswith(f'{count}. ') for count, line in enumerate(lines, start=1)):
            return tt.markdown_ord_list

    return tt.markdown_paragraph
