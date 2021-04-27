from anytree import Node , RenderTree
class TreeMaker:

    depth = 1
    currentNode = Node(id = "program" , children = [])

    @classmethod
    def makeNode(cls, ID, goIn = False):
        new_node = Node(id = ID , parent = cls.currentNode , children = [])
        cls.currentNode.children.append(new_node)
        print('made node: ', ID)
        if goIn:
            cls.currentNode = new_node
            cls.depth = cls.depth + 1
            print('goin in, depth: ', cls.depth)

    @classmethod
    def goUp(cls):
        if cls.currentNode.parent:
            cls.currentNode = cls.currentNode.parent
            cls.depth = cls.depth - 1

