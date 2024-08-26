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
        for chunk in range(len(chunks)):
            if chunks[chunk] == "":
                continue
            if chunk % 2:
                split_nodes.append(TextNode(chunks[chunk], text_type))
            else:
                split_nodes.append(TextNode(chunks[chunk], tt.text_type_text))
        new_nodes.extend(split_nodes)
    return new_nodes

