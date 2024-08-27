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

def split_nodes_image(node):
    split_nodes =[]
    image_data = extract_markdown_images(node.text)
    last_index = 0
    
    for image in image_data:
        start_index = node.text.find(f'![{image[0]}]({image[1]})', last_index)
        if start_index != -1:
            if start_index > last_index:
                split_nodes.append(TextNode(node.text[last_index:start_index], tt.text_type_text))
            split_nodes.append(TextNode(image[0], tt.text_type_image, image[1]))
            last_index = start_index + len(f'![{image[0]}]({image[1]})')

    #add remaining text after the last image
    if last_index < len(node.text):
        split_nodes.append(TextNode(node.text[last_index:], tt.text_type_text))
    
    return split_nodes

def split_nodes_links(node):
    split_nodes =[]
    link_data = extract_markdown_links(node.text)
    last_index = 0

    for link in link_data:
        start_index = node.text.find(f'[{link[0]}]({link[1]})', last_index)
        if start_index != -1:
            if start_index > last_index:
                split_nodes.append(TextNode(node.text[last_index:start_index], tt.text_type_text))
            split_nodes.append(TextNode((link[0]), tt.text_type_link, link[1]))
            last_index = start_index + len(f'[{link[0]}]({link[1]})')
    
    #add remaining text after the last link
    if last_index < len(node.text):
        split_nodes.append(TextNode(node.text[last_index:], tt.text_type_text))
    
    return split_nodes

