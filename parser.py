import anytree
import scanner
from printColors import colors
from anytree import Node , RenderTree

#Global flags
hasLearntTheGrammar = False
lookahead = None
Ended = False



class Grammar:
    
    grammar = {'Program':['DeclarationList $']}

    @classmethod
    def learnGrammar(cls):
        gf = open('grammar.txt', 'r')
        lines = gf.readlines()
        for line in lines[1:] :
            line = line.replace('\n', '').split(' -> ')
            lhs = line[0].strip()
            rhs = [line[1].strip()]
            if 'ε' in rhs: continue
            if lhs in cls.grammar.keys():
                cls.grammar[lhs] = cls.grammar[lhs] + rhs
            else:
                cls.grammar[lhs] = rhs

    @classmethod
    def get_first(cls, nonTerminal):
        if nonTerminal == 'Program':
            return "$~int~void"
        if nonTerminal == 'DeclarationList':
            return "int~void~EPSILON"
        if nonTerminal == 'Declaration':
            return "int~void"
        if nonTerminal == 'DeclarationInitial':
            return "int~void"
        if nonTerminal == 'DeclarationPrime':
            return ";~[~("
        if nonTerminal == 'VarDeclarationPrime':
            return ";~["
        if nonTerminal == 'FunDeclarationPrime':
            return "("
        if nonTerminal == 'TypeSpecifier':
            return "int~void"
        if nonTerminal == 'Params':
            return "int~void"
        if nonTerminal == 'ParamListVoidAbtar':
            return "ID~EPSILON"
        if nonTerminal == 'ParamList':
            return ",~EPSILON"
        if nonTerminal == 'Param':
            return "int~void"
        if nonTerminal == 'ParamPrime':
            return "[~EPSILON"
        if nonTerminal == 'CompoundStmt':
            return "{"
        if nonTerminal == 'StatementList':
            return "ID~;~NUM~(~{~break~if~while~return~for~+~-~EPSILON"
        if nonTerminal == 'Statement':
            return "ID~;~NUM~(~{~break~if~while~return~for~+~-"
        if nonTerminal == 'ExpressionStmt':
            return "ID~;~NUM~(~break~+~-"
        if nonTerminal == 'SelectionStmt':
            return "if"
        if nonTerminal == 'IterationStmt':
            return "while"
        if nonTerminal == 'ReturnStmt':
            return "return"
        if nonTerminal == 'ReturnStmtPrime':
            return "ID~;~NUM~(~+~-"
        if nonTerminal == 'ForStmt':
            return "for"
        if nonTerminal == 'Vars':
            return "ID"
        if nonTerminal == 'VarZegond':
            return ",~EPSILON"
        if nonTerminal == 'Var':
            return "ID"
        if nonTerminal == 'Expression':
            return "ID~NUM~(~+~-"
        if nonTerminal == 'B':
            return "[~(~=~<~==~+~-~*~EPSILON"
        if nonTerminal == 'H':
            return "=~<~==~+~-~*~EPSILON"
        if nonTerminal == 'SimpleExpressionZegond':
            return "NUM~(~+~-"
        if nonTerminal == 'SimpleExpressionPrime':
            return "(~<~==~+~-~*~EPSILON"
        if nonTerminal == 'C':
            return "<~==~EPSILON"
        if nonTerminal == 'Relop':
            return "<~=="
        if nonTerminal == 'AdditiveExpression':
            return "ID~NUM~(~+~-"
        if nonTerminal == 'AdditiveExpressionPrime':
            return "(~+~-~*~EPSILON"
        if nonTerminal == 'AdditiveExpressionZegond':
            return "NUM~(~+~-"
        if nonTerminal == 'D':
            return "+~-~EPSILON"
        if nonTerminal == 'Addop':
            return "+~-"
        if nonTerminal == 'Term':
            return "ID~NUM~(~+~-"
        if nonTerminal == 'TermPrime':
            return "(~*~EPSILON"
        if nonTerminal == 'TermZegond':
            return "NUM~(~+~-"
        if nonTerminal == 'G':
            return "*~EPSILON"
        if nonTerminal == 'SignedFactor':
            return "ID~NUM~(~+~-"
        if nonTerminal == 'SignedFactorPrime':
            return "(~EPSILON"
        if nonTerminal == 'SignedFactorZegond':
            return "NUM~(~+~-"
        if nonTerminal == 'Factor':
            return "ID~NUM~("
        if nonTerminal == 'VarCallPrime':
            return "[~(~EPSILON"
        if nonTerminal == 'VarPrime':
            return "[~EPSILON"
        if nonTerminal == 'FactorPrime':
            return "(~EPSILON"
        if nonTerminal == 'FactorZegond':
            return "NUM~("
        if nonTerminal == 'Args':
            return "ID~NUM~(~+~-~EPSILON"
        if nonTerminal == 'ArgList':
            return "ID~NUM~(~+~-"
        if nonTerminal == 'ArgListPrime':
            return ",~EPSILON"
        return nonTerminal

    @classmethod
    def get_follow(cls, nonTerminal):
        if nonTerminal == 'Program':
            return "$"
        if nonTerminal == 'DeclarationList':
            return "$~ID~;~NUM~(~{~}~break~if~while~return~for~+~-"
        if nonTerminal == 'Declaration':
            return "$~ID~;~NUM~(~int~void~{~}~break~if~while~return~for~+~-"
        if nonTerminal == 'DeclarationInitial':
            return ";~[~(~)~,"
        if nonTerminal == 'DeclarationPrime':
            return "$~ID~;~NUM~(~int~void~{~}~break~if~while~return~for~+~-"
        if nonTerminal == 'VarDeclarationPrime':
            return "$~ID~;~NUM~(~int~void~{~}~break~if~while~return~for~+~-"
        if nonTerminal == 'FunDeclarationPrime':
            return "$~ID~;~NUM~(~int~void~{~}~break~if~while~return~for~+~-"
        if nonTerminal == 'TypeSpecifier':
            return "ID"
        if nonTerminal == 'Params':
            return ")"
        if nonTerminal == 'ParamListVoidAbtar':
            return ")"
        if nonTerminal == 'ParamList':
            return ")"
        if nonTerminal == 'Param':
            return ")~,"
        if nonTerminal == 'ParamPrime':
            return ")~,"
        if nonTerminal == 'CompoundStmt':
            return "$~ID~;~NUM~(~int~void~{~}~break~if~else~while~return~for~+~-"
        if nonTerminal == 'StatementList':
            return "}"
        if nonTerminal == 'Statement':
            return "ID~;~NUM~(~{~}~break~if~else~while~return~for~+~-"
        if nonTerminal == 'ExpressionStmt':
            return "ID~;~NUM~(~{~}~break~if~else~while~return~for~+~-"
        if nonTerminal == 'SelectionStmt':
            return "ID~;~NUM~(~{~}~break~if~else~while~return~for~+~-"
        if nonTerminal == 'IterationStmt':
            return "ID~;~NUM~(~{~}~break~if~else~while~return~for~+~-"
        if nonTerminal == 'ReturnStmt':
            return "ID~;~NUM~(~{~}~break~if~else~while~return~for~+~-"
        if nonTerminal == 'ReturnStmtPrime':
            return "ID~;~NUM~(~{~}~break~if~else~while~return~for~+~-"
        if nonTerminal == 'ForStmt':
            return "ID~;~NUM~(~{~}~break~if~else~while~return~for~+~-"
        if nonTerminal == 'Vars':
            return "ID~;~NUM~(~{~break~if~while~return~for~+~-"
        if nonTerminal == 'VarZegond':
            return "ID~;~NUM~(~{~break~if~while~return~for~+~-"
        if nonTerminal == 'Var':
            return "ID~;~NUM~(~{~break~if~while~return~for~+~-"
        if nonTerminal == 'Expression':
            return ";~]~)~,"
        if nonTerminal == 'B':
            return ";~]~)~,"
        if nonTerminal == 'H':
            return ";~]~)~,"
        if nonTerminal == 'SimpleExpressionZegond':
            return ";~]~)~,"
        if nonTerminal == 'SimpleExpressionPrime':
            return ";~]~)~,"
        if nonTerminal == 'C':
            return ";~]~)~,"
        if nonTerminal == 'Relop':
            return "ID~NUM~(~+~-"
        if nonTerminal == 'AdditiveExpression':
            return ";~]~)~,"
        if nonTerminal == 'AdditiveExpressionPrime':
            return ";~]~)~,~<~=="
        if nonTerminal == 'AdditiveExpressionZegond':
            return ";~]~)~,~<~=="
        if nonTerminal == 'D':
            return ";~]~)~,~<~=="
        if nonTerminal == 'Addop':
            return "ID~NUM~(~+~-"
        if nonTerminal == 'Term':
            return ";~]~)~,~<~==~+~-"
        if nonTerminal == 'TermPrime':
            return ";~]~)~,~<~==~+~-"
        if nonTerminal == 'TermZegond':
            return ";~]~)~,~<~==~+~-"
        if nonTerminal == 'G':
            return ";~]~)~,~<~==~+~-"
        if nonTerminal == 'SignedFactor':
            return ";~]~)~,~<~==~+~-~*"
        if nonTerminal == 'SignedFactorPrime':
            return ";~]~)~,~<~==~+~-~*"
        if nonTerminal == 'SignedFactorZegond':
            return ";~]~)~,~<~==~+~-~*"
        if nonTerminal == 'Factor':
            return ";~]~)~,~<~==~+~-~*"
        if nonTerminal == 'VarCallPrime':
            return ";~]~)~,~<~==~+~-~*"
        if nonTerminal == 'VarPrime':
            return "ID~;~NUM~]~(~)~,~{~break~if~while~return~for~<~==~+~-~*"
        if nonTerminal == 'FactorPrime':
            return ";~]~)~,~<~==~+~-~*"
        if nonTerminal == 'FactorZegond':
            return ";~]~)~,~<~==~+~-~*"
        if nonTerminal == 'Args':
            return ")"
        if nonTerminal == 'ArgList':
            return ")"
        if nonTerminal == 'ArgListPrime':
            return ")"

    @classmethod
    def get_first_rhs(cls, rhs):
        stuff = rhs.split(' ')
        firsts = []
        for i in stuff:
            if not cls.is_non_terminal(i):
                firsts.append(i)
                return firsts
            ifirst = cls.get_first(i).split('~')
            if 'EPSILON' in ifirst:
                firsts = firsts + ifirst[:-1]
            else:
                firsts = firsts + ifirst
                return firsts
        return firsts


    @classmethod
    def get_rhs_grammars(cls, nonTerminal):
        return cls.grammar[nonTerminal]

    @classmethod
    def is_non_terminal(cls, x):
        return (x in cls.grammar.keys())






class TreeMaker:

    depth = 1
    root = Node(name = "program" , parent = None)
    currentNode = root
    @classmethod
    def appendNode(cls, ID, goIn = False):
        new_node = Node(name = ID , parent = cls.currentNode)
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
    @classmethod
    def printTree(cls):
        for pre, _, node in RenderTree(cls.root):
            print("%s%s" % (pre, node.name))
    @classmethod
    def renderTreeInFile(cls):
        file = open("parse_tree.txt" , "w")
        file.write()
        file.close


def match(terminal):
    global lookahead
    if lookahead.tokenType in ['KEYWORD', 'SYMBOL']:
        la = lookahead.value
    else:
        la = lookahead.tokenType

    if terminal == la:
        print(f"{colors.OKGREEN}\t\tMATCH -> {lookahead}{colors.ENDC}")
        TreeMaker.appendNode(str(lookahead), False)
    else:
        print(f"{colors.FAIL}well fuck! @ match{colors.ENDC}")
    next_lookahead()






count = 0
def procedure(nonTerminal):
    global lookahead
    global Ended
    global count
    count = count + 1
    if count > 200:
        exit()

    if lookahead.tokenType in ['KEYWORD', 'SYMBOL']:
        la = lookahead.value
    else:
        la = lookahead.tokenType

    print(f'\t\t{colors.OKCYAN} Procedure: {nonTerminal} ... lookahead: {la} {colors.ENDC} \n')

  
    rhs = Grammar.get_rhs_grammars(nonTerminal)
    print('RHS = ', rhs)
    for r in rhs:
        if Ended: return

        firsts = Grammar.get_first_rhs(r)
        print('\t r from rhs is:', r,  'firsts: ', firsts)
        if la in firsts:
            for word in r.split(' '):
                if Ended: return

                if Grammar.is_non_terminal(word):
                    TreeMaker.makeNode(word, goIn=True)
                    procedure(word)
                else:
                    match(word)
                    if lookahead.tokenType in ['KEYWORD', 'SYMBOL']:
                        la = lookahead.value
                    else:
                        la = lookahead.tokenType
            TreeMaker.goUp()
            return 
                    
    #error handling
    else:

        print(f"{colors.FAIL}\t\t#{scanner.lineNo} : follow of  {nonTerminal} : {Grammar.get_follow(nonTerminal)} {colors.ENDC}")
        if la in Grammar.get_follow(nonTerminal).split('~'):
            if 'EPSILON' in Grammar.get_first(nonTerminal).split('~'):
                TreeMaker.makeNode('epsilon', goIn=False)
                TreeMaker.goUp()
                return 

            print(f"{colors.FAIL}\t\t#{scanner.lineNo} : Missing {nonTerminal}{colors.ENDC}")
            #honestly idk what we're supposed to do here! :| 
            TreeMaker.goUp()
            return 
        else:
            if (la == '$'):
                print(f'{colors.FAIL}\t\t#{scanner.lineNo} : syntax error, unexpected EOF{colors.ENDC}')
                Ended = True
            else:
                print(f'{colors.FAIL}\t\t#{scanner.lineNo} : syntax error, illegal {la}{colors.ENDC}')
                next_lookahead()
                procedure(nonTerminal)
            return
    TreeMaker.goUp()
    return




def next_lookahead():
    global lookahead
    
    if lookahead and lookahead.tokenType == '$': 
        print(TreeMaker.depth)
        return
    
    lookahead = scanner.get_next_token()
    while(not lookahead):
        lookahead = scanner.get_next_token()
    print(f"{colors.WARNING} got the next token: {lookahead}{colors.ENDC}")


def startParsing():
    global lookahaed
    Grammar.learnGrammar()
    next_lookahead()
    procedure('Program')

    # if token.tokenType == '$':
        #this is the end


# Grammar.learnGrammar()
# print(Grammar.get_first_rhs('SimpleExpressionPrime'))

# lookahead = scanner.Token('KEYWORD', 'void')
# procedure('Program')