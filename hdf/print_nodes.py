import tables
import sys

with tables.open_file(sys.argv[1], "r") as f:
    nodes = list(f.root._v_children.keys())
    for node in nodes: print(node)