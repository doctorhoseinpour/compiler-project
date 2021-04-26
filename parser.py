import anytree
import scanner

#Global flags
hasLearntTheGrammar = False
lookahead = ''

class Grammar:
    
    # grammar

    @classmethod
    def learnGrammar(cls):
        gf = open('grammar.txt', 'r')
        lines = gf.readlines()
        cls.grammar = {'Program':['DeclarationList', '$']}
        for line in lines[1:] :
            line = line.replace('\n', '').split('-> ')
            lhs = line[0]
            rhs = [line[1]]
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
            return "(~,"
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
    def get_rhs_grammars(cls, nonTerminal):
        return "AllRHSfromGrammarWhere_nonTerminal_isOntheLHS"





def procedure(nonTerminal, la):
    rhs = ParserBro.get_rhs_grammars(nonTerminal)
    rhss = rhs.split('~')
    for r in rhss: # except for epsilon 
        rr = r.split(' ') #first token/non_terminal = rr[0]
        frists = ParserBro.get_first(rr[0]).split('~')
        if la in frists:
            for gholam in rr:
                if fuck in terminals:
                    match(la, gholam)
                else:
                    procedure(gholam, la)
            #callthem
    #error handling
    else:
        print("yo mama dumb")




def next_lookahead():
    token = scanner.get_next_token()
    while(not token):
        token = scanner.get_next_token()
    return token

def learnGrammar():
    open('grammar.txt', 'r')


def startParsing():
    global lookahaed
    learnGrammar()
    lookahead = next_lookahead().tokenType
    procedure('program', lookahead)

    # if token.tokenType == '$':
        #this is the end


Grammar.learnGrammar()