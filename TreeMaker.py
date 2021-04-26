
class TreeMaker:

    depth = 1
    currentNode = "Program"

    @classmethod
    def makeNode(cls, id, goIn = False):
        # newNode = ...
        print('made node: ', id)
        if goIn:
            # currentNode = newNode if goIn = True
            cls.depth = cls.depth + 1
            print('goin in, depth: ', cls.depth)

    @classmethod
    def goUp(cls):
        cls.currentNode = cls.currentNode.parent
        cls.depth = cls.depth - 1
