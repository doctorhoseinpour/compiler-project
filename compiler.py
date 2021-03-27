import re


class PanicException(Exception):    
    def __init__(self, message):
        self.message = message


class Node:

    # isFinal
    # edges
    # number

    def __init__(self, number, isFinal = False):
        self.number = number
        self.isFinal = isFinal
        self.edges = []

    def addEdge(self, *edges):
        for e in edges:
            self.edges.append(e)

    # gets character and returns the next state. if there are no moves using the given char, if current state is final, returns null. otherwise raises a panicException
    def getNextState(self, character):
        for e in self.edges:
            if e.matches(character):
                return e.destinationNode
        if self.isFinal:
            return None

        raise PanicException("nowhere to go & it's not final!")


class Edge:

    #regex   
    #destinationNode

    def __init__(self,number,regex, destination):
        self.number = number
        self.regex = regex
        self.destinationNode = destination

    def matches(self, character):
        regRes = re.findall(self.regex, character)
        return len(regRes) > 0


def create_token(tokenString):
    keywords = ["if", "else", "void", "int", "while", "break", "switch", "default", "case", "return", "for"]
    if keywords.

def install_id():
    print("TODO")


# creates the scanner DFA and returns the srart node
def createDFA():
    
    s0 = Node("0" , isFinal = False)
    s1 = Node("1" , isFinal = False)
    s2 = Node("2" , isFinal = True)
    s3 = Node("3" , isFinal = False)
    s4 = Node("4" , isFinal = True)
    s5 = Node("5" , isFinal = True)
    s6 = Node("6" , isFinal = False)
    s7 = Node("7" , isFinal = True)
    s8 = Node("8" , isFinal = False)
    s9 = Node("9" , isFinal = True)
    s10 = Node("10" , isFinal = False)
    s11 = Node("11" , isFinal = False)
    s12 = Node("12" , isFinal = True)
    s13 = Node("13" , isFinal = False)
    s14 = Node("14" , isFinal = False)
    s15 = Node("15" , isFinal = True)

    # ID / Keyword
    s0.addEdge(Edge(1, "\w+", s1))
    s1.addEdge(Edge(1,"\w+", s1) , Edge(0 , "\s | : | ; | , | [ | ] | ( | ) | { | } | + | - | = | * | <", s2))
    
    # Number
    s0.addEdge(Edge(2 , "\d+" , s3))
    s3.addEdge(Edge(1 , "\d+" , s3) , Edge(0 , "\s | : | ; | , | [ | ] | ( | ) | { | } | + | - | = | * | <" , s4))

    # Symbol
    s0.addEdge(Edge(3 , ": | ; | , | [ | ] | ( | ) | { | } | + | - | <" , s5) , Edge(4 , "=" , s6) , Edge(5 , "*" , s8))
    s6.addEdge(Edge(1 , "=" , s7) , Edge(0 , "" , s9))
    s8.addEdge(Edge(0 , "" , s9)) 
 

    


def get_token():
    print("TODO")


f = open("input.txt", "r")



"""
void main ( void ) {
    int a = 0;
    // comment1
    a = 2 + 2;
    a = a - 3;
    cde = a;
    if (b /* comment2 */ == 3d) {
        a = 3;
        cd!e = 7;
    }
    else */
    {
        b = a < cde;
        {cde = @2;
    }}
    return;/* comment 3
}
"""

