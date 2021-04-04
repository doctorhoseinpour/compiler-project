#Globals
file = open('input.txt', 'r')
tokens_file = open('tokens.txt', 'w')
err_file = open('lexical_errors.txt', 'w')
table_file = open('symbol_table.txt', 'w')
lastReadChar = None #everytime you want to go back (used a lookahead), set this to the current read character
reserved_keywords = ["if", "else", "void", "int", "while", "break", "switch", "default", "case", "return", "for"]
lineNo = 1
tokensFirstPanic = 1
onNewLine = True
tokenString = ""
tokens = []

class PanicException(Exception):    
    def __init__(self, message):
        self.message = message


class NotRegex:
    @staticmethod
    def detect(txt, *regex):
        res = False

        for r in regex:
            if r == "\d":
                res = res or txt.isdigit()
            elif r == "\w":
                res = res or txt.isdigit() or txt.isalpha()
            elif r == "\sym":
                res = res or (txt in ['$', ':', ',', ';' , '[' , ']' , ';' , ')' , '{' , '}' , '+' , '-' , '=' , '*' , '<'])
            elif r == "\s":
                res = res or (txt in ["\n", "\t", " ", "\f", "\v", "\r"])
            else:
                res = res or txt == r
            if res:
                return res
        return res

symbol_table = []
def install_id(*ids):
    for id in ids:
        if not id in symbol_table:
            symbol_table.append(id)
            table_file.write(f"{len(symbol_table)}.\t{id}\n")
install_id(*reserved_keywords)

class Token:
    def __init__(self, tokenType, value):
        self.tokenType = tokenType # id / keyword / num / symbol 
        self.value = value
    
    @staticmethod
    def create_token(tokenString, stateNumber):
        # print(stateNumber, " -> ", tokenString)
        global reserved_keywords
        if stateNumber == 2:
            install_id(tokenString)
            if tokenString in reserved_keywords:
                return Token("KEYWORD", tokenString)
            return Token("ID", tokenString)
        elif stateNumber == 4:
            return Token("NUM", tokenString)
        elif stateNumber == 5:
            return Token("SYMBOL", tokenString)    
        elif stateNumber == 7 or stateNumber == 9:
            return Token("SYMBOL" , tokenString)
    
    def __str__(self):
        return f"{self.tokenType}, {self.value}"




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
        dest = None
        for e in self.edges:
            if e.matches(character):
                dest = e.destinationNode

        if dest == None and not self.isFinal:
            raise PanicException("nowhere to go & it's not final!")
        
        return dest


class Edge:

    #regex
    #destinationNode

    def __init__(self,number, destination, *regexes):
        self.number = number
        self.regexes = regexes
        self.destinationNode = destination

    def matches(self, character):
        return NotRegex.detect(character, *(self.regexes))



def panic(panicNodeNumber):
    global lineNo
    global onNewLine
    global tokenString
    global tokensFirstPanic
    if onNewLine:
        err_file.write(f"\n{lineNo}.\t")
        onNewLine = False
    if (tokensFirstPanic == 1):
        if (panicNodeNumber == 0):
            err_file.write(f"({tokenString}, invalid input) ")
        elif (panicNodeNumber == 1):
            err_file.write(f"({tokenString}, invalid input) ")
        elif (panicNodeNumber == 3):
            err_file.write(f"({tokenString}, invalid number) ")
        elif (panicNodeNumber == 8):
            err_file.write(f"({tokenString}, Unmatched comment) ")
        tokensFirstPanic = 0
    tokenString = tokenString[0:-1]
    


# creates the scanner DFA and returns the srart node
def createDFA():
    s0 = Node(0 , isFinal = False)
    s1 = Node(1 , isFinal = False)
    s2 = Node(2 , isFinal = True)
    s3 = Node(3 , isFinal = False)
    s4 = Node(4 , isFinal = True)
    s5 = Node(5 , isFinal = True)
    s6 = Node(6 , isFinal = False)
    s7 = Node(7 , isFinal = True)
    s8 = Node(8 , isFinal = False)
    s9 = Node(9 , isFinal = True)
    s10 = Node(10 , isFinal = False)
    s11 = Node(11, isFinal = False)
    s12 = Node(12 , isFinal = True)
    s13 = Node(13 , isFinal = False)
    s14 = Node(14 , isFinal = False)
    s15 = Node(15 , isFinal = True)

    # ID / Keyword
    s0.addEdge(Edge(1, s1 ,"\w"))
    s1.addEdge(Edge(1,s1,"\w") , Edge(0 , s2,"\s", "\sym", "/"))
    
    # Number
    s0.addEdge(Edge(2 , s3 ,"\d"))
    s3.addEdge(Edge(1 , s3 ,"\d") , Edge(0 , s4 ,"\s" ,"\sym" ))

    # Symbol
    s0.addEdge(Edge(3 , s5 ,":" , ";" , "," , "[" , "]" , "(" , ")" , "{" , "}" , "+" , "-" , "<" ) , Edge(4 , s6 ,"=" ) , Edge(5 , s8 ,"*"))
    s6.addEdge(Edge(1 ,  s7 ,"=" ) , Edge(0 , s9 ,"\d" , "\w" , "\s" , ":" , ";" , "," , "[" , "]" , "(" , ")" , "{" , "}" , "+" , "-" , "*" , "<"))
    s8.addEdge(Edge(0 ,  s9 ,"\d" , "\w" , "\sym" , "\s")) 

    # Comment
    s0.addEdge(Edge(6 , s10 , "/"))
    s10.addEdge(Edge(1 ,s11 , "/") , Edge(2 ,s13 ,"*"))
    s11.addEdge(Edge(1 ,s12 ,"\n" ) , Edge(0 , s11 , "\sym" , "\w" , "\d" , "\t" , " " , "\f"))
    s13.addEdge(Edge(1 ,s14 , "*") , Edge(0 ,s13 , "\s" , "\w" , "\d" ,":" , ";" , "," , "[" , "]" , "(" , ")" , "{" , "}" , "+" , "-" , "=" , "<"))
    s14.addEdge(Edge(1 ,s14 , "*") , Edge(2 ,s12 , "/") , Edge(0 ,s13 , "\w" , "\d" , "\s" ,":" , ";" , "," , "[" , "]" , "(" , ")" , "{" , "}" , "+" , "-" , "=" , "<" ))
    
    # Whitespace
    s0.addEdge(Edge(7 , s15 , "\s" , "\v"))

    return s0
    

startNode = createDFA()



def close_files():
    file.close()
    err_file.close()
    table_file.close()
    tokens_file.close()


def get_next_token():
    hasEnded = False
    global lastReadChar
    global lineNo
    global onNewLine
    global tokenString
    global tokensFirstPanic
    # start making the token
    currentNode = startNode
    tokenString = ""
    tokensFirstPanic = 1
    while True:
        char = lastReadChar if (lastReadChar != None) else file.read(1)
        lastReadChar = None

        if not char:
            if len(tokenString) > 0:
                tokenString = tokenString.replace("\n", "")
                msg = tokenString if len(tokenString) < 8  else tokenString[0:6]
                err_file.write(f"{lineNo}.\t\t{msg}..., Unclosed comment")
                close_files()

            hasEnded = True
            break

        if char == "\n":
            lineNo = lineNo + 1
            onNewLine = True

        tokenString = tokenString + char
        token = None
        try:
            nextNode = currentNode.getNextState(char)
            panicNode = currentNode
            currentNode = nextNode
            if nextNode.isFinal:
                if currentNode.number in [2, 4, 9]:
                    lastReadChar = char
                    tokenString = tokenString[0:-1]
                token = Token.create_token(tokenString, currentNode.number)
                if token != None:
                    tokens.append(token)
                    if onNewLine:
                        tokens_file.write(f"\n{lineNo}.\t")
                        onNewLine = False
                    tokens_file.write(f"({token.tokenType}, {token.value}) ")
                                        # print("\n", currentNode.number, " -> ", token, sep="")
                                        # if lastReadChar != None :
                                        #     print("LastReadChar: ", lastReadChar if lastReadChar != " " else " SPACE " )
                break
            elif nextNode != None:
                currentNode = nextNode
            else:
                panic(panicNode.number)
                
        except PanicException:
            panic(panicNode.number)

    #token is made    
    return (token, hasEnded)


while True:
    
    res = get_next_token()
    hasEnded = res[1]
    token = res[0]
              
    if hasEnded: 
        break
