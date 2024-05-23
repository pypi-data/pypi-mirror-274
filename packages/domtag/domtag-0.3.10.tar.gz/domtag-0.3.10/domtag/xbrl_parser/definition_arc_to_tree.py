from bs4 import BeautifulSoup
import anytree

with open(
        "/domtag/resources/us-gaap-2021-01-31.xsd",
        "r") as f:
    soup = BeautifulSoup(f.read(), 'xml')
links = soup.find_all('link:definitionArc')
nodes = {}
for link in links:
    parent_name = link.attrs['xlink:from'].split('_', 1)[-1]
    child_name = link.attrs['xlink:to'].split('_', 1)[-1]
    if parent_name not in nodes:
        nodes[parent_name] = anytree.Node(parent_name)
    parent_node = nodes[parent_name]
    if child_name not in nodes:
        nodes[child_name] = anytree.Node(child_name)
    child_node = nodes[child_name]
    child_node.parent = parent_node
