from collections import deque


class Node(object):
    def __init__(self, id):
        self.adj = {}  # dict id voisin -> poids
        self.id = id

    def add(self, v, w):
        self.adj[v] = w

    def remove(self, v):
        self.adj.pop(v)

    def is_adj(self, v):
        return v in self.adj

    def weight(self, v):
        return self.adj[v]

    def neighbours(self):
        return self.adj.items()

    def __lt__(self, other):
        return self.dist < other.dist



class WGraph(object):
    def __init__(self):
        self.nodes = {}

    def add_node(self, u):
        self.nodes[u] = Node(u)

    def get_node(self, u):
        return self.nodes[u]

    def is_node_in(self, u):
        return u in self.nodes

    def add_edge(self, u, v, w):
        unode = self.nodes.setdefault(u, Node(u))
        if not (unode.is_adj(v)): unode.add(v, w)
        vnode = self.nodes.setdefault(v, Node(v))
        if not (vnode.is_adj(u)): vnode.add(u, w)

    def remove_edge(self, u, v):
        self.nodes[u].remove(v)
        self.nodes[v].remove(u)

    def weight(self, u, v):
        return self.nodes[u].weight(v)

    def neighbour(self, u):
        return self.nodes[u].neighbours()

    def bfs(self, src, dest):
        """
        breadth = width first search
        :param src:
        :param dest:
        :return:
        """
        for node in self.nodes.values():
            node.explored = False
            self.nodes[src].explored = True
            queue = deque([src])
        while queue:
            u = queue.popleft()
            print(self.nodes[u].id, end=' ')
            if u == dest: return
            for (v, _) in self.neighbours(u):
                if not self.nodes[v].explored:
                    self.nodes[v].explored = True
                queue.append(v)
                # raise NotFound()


def traverse(nodes, dest):
    path = []
    while dest is not None:
        path.append(dest)
        dest = nodes[dest].pred
        path.reverse()
    return path
