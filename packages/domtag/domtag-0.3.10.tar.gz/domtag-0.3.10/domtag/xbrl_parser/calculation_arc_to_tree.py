"""Parse the calculation definitions into a tree
"""
from bs4 import BeautifulSoup
import anytree

path = "domtag/resources/newmarketcorp/neu-20211231_cal.xml"

with open(path, "r") as f:
    soup = BeautifulSoup(f.read(), 'xml')
links = soup.find_all('link:calculationArc')
nodes = {}
for link in links:
    parent_name = link.attrs['xlink:from'].rsplit('_', 1)[0].rsplit('_', 1)[-1]
    child_name = link.attrs['xlink:to'].rsplit('_', 1)[0].rsplit('_', 1)[-1]
    weight = float(link.attrs['weight'])
    if parent_name not in nodes:
        nodes[parent_name] = anytree.Node(parent_name)
    parent_node = nodes[parent_name]
    if child_name not in nodes:
        nodes[child_name] = anytree.Node(child_name)
    child_node = nodes[child_name]
    child_node.parent = parent_node
    child_node.weight = weight

for node in nodes.values():
    if 'weight' in node.__dict__:
        # noinspection PyUnresolvedReferences
        if node.weight == 1.0:
            node.sign = '+'
        elif node.weight == -1.0:
            node.sign = '-'
        else:
            # noinspection PyUnresolvedReferences
            raise Exception(f"Unknown weight {node.weight}")
    else:
        node.sign = ''

for node_name, node in nodes.items():
    if not node.parent and node.children:
        for pre, fill, sub_node in anytree.RenderTree(node):
            print("%s%s %s" % (
                pre,
                sub_node.sign,
                sub_node.name
            ))
