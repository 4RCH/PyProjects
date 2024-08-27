import re
from textnode import TextNode
import texttypes as tt

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        chunks = old_node.text.split(delimiter)
        if len(chunks)% 2 == 0:
            raise ValueError("[!] Missing closing delimiter")
        for i, chunk in enumerate(chunks):
            if chunk == "":
                continue
            if i % 2:
                split_nodes.append(TextNode(chunk, text_type))
            else:
                split_nodes.append(TextNode(chunk, tt.text_type_text))
        new_nodes.extend(split_nodes)
    return new_nodes

def extract_markdown_images(raw_markdown):
    pattern = r"!\[(.*?)\]\((.*?)\)"
    formatted_text = re.findall(pattern, raw_markdown)
    return formatted_text

def extract_markdown_links(raw_markdown):
    pattern = r"\[(.*?)\]\((.*?)\)"
    formatted_text = re.findall(pattern, raw_markdown)
    return formatted_text

def split_nodes_generic(nodes, pattern, text_type):
    new_nodes = []
    for node in nodes:
        split_nodes =[]
        matches = re.finditer(pattern, node.text)
        last_index = 0
        
        for match in matches:
            start_index = match.start()
            if start_index > last_index:
                split_nodes.append(TextNode(node.text[last_index:start_index], tt.text_type_text))
            if text_type == tt.text_type_image:
                split_nodes.append(TextNode(match.group(1), text_type, match.group(2)))
            else:
                split_nodes.append(TextNode(match.group(1), text_type, match.group(2)))
            last_index = match.end()
        
        #add remaining text after the last image
        if last_index < len(node.text):
            split_nodes.append(TextNode(node.text[last_index:], tt.text_type_text))

        new_nodes.extend(split_nodes)
    return new_nodes

def split_nodes_image(nodes):
    pattern = r"!\[(.*?)\]\((.*?)\)"
    return split_nodes_generic(nodes, pattern, tt.text_type_image)

def split_nodes_links(nodes):
    pattern = r"\[(.*?)\]\((.*?)\)"
    return split_nodes_generic(nodes, pattern, tt.text_type_link)

