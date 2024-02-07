import copy


class Node(object):
    def __init__(self, name):
        self.name = name
        self.parents = dict()
        self.children = dict()

    def add_parent(self, parent):
        self.parents[parent.name] = parent

    def add_child(self, child):
        self.children[child.name] = child


class BayesNet(object):
    def __init__(self):
        self.nodes = dict()

    def add_edge(self, edge):
        (parent_name, child_name) = edge
        if parent_name not in self.nodes:
            self.nodes[parent_name] = Node(parent_name)
        if child_name not in self.nodes:
            self.nodes[child_name] = Node(child_name)
        parent = self.nodes.get(parent_name)
        child = self.nodes.get(child_name)
        parent.add_child(child)
        child.add_parent(parent)

    def check_d_separation(self, start_node, end_node, observed):
        visited = set()
        checking_nodes = [(start_node, "child_to_parent")]
        while len(checking_nodes) > 0:
            (node_name, direction) = checking_nodes.pop()
            node = self.nodes[node_name]
            if (node_name, direction) not in visited:
                visited.add((node_name, direction))
                if node_name not in observed and node_name == end_node:
                    return False
                if direction == "parent_to_child":
                    self.parent_to_child_add(checking_nodes, node, node_name, observed)
                elif direction == "child_to_parent" and node_name not in observed:
                    self.child_to_parent_add(checking_nodes, node)
        return True

    def parent_to_child_add(self, checking_nodes, node, node_name, observed):
        visit_nodes = copy.copy(observed)
        observed_ancestor = set()
        while len(visit_nodes) > 0:
            for parent in self.nodes[visit_nodes.pop()].parents:
                observed_ancestor.add(parent)
        if node_name not in observed:
            for child in node.children:
                checking_nodes.append((child, "parent_to_child"))
        if node_name in observed or node_name in observed_ancestor:
            for parent in node.parents:
                checking_nodes.append((parent, "child_to_parent"))

    def child_to_parent_add(self, checking_nodes, node):
        for child in node.children:
            checking_nodes.append((child, "parent_to_child"))
        for parent in node.parents:
            checking_nodes.append((parent, "child_to_parent"))


if __name__ == "__main__":
    bn = BayesNet()
    n = int(input().strip())
    m = int(input().strip())
    for _ in range(m):
        edge = input().strip().split('->')
        bn.add_edge(edge)
    T = int(input().strip())
    for _ in range(T):
        start = input().strip()
        end = input().strip()
        observed = input().strip().split()
        print(bn.check_d_separation(start, end, observed))
