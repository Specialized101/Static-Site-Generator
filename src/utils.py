
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        count = node.text.count(delimiter)
        if count == 0:
            new_nodes.append(node)
            continue
        
        if count % 2 != 0:
            raise ValueError(f"Incorrect markdown syntax, received: {node.text}")
        
        node_splits = node.text.split(delimiter)
        for i in range(len(node_splits)):
            if i % 2 == 0:
                new_nodes.append(TextNode(node_splits[i], TextType.TEXT))
            else:
                new_nodes.append(TextNode(node_splits[i], text_type))

    return new_nodes
