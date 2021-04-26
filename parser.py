import anytree
import scanner

#Global flags
hasLearntTheGrammar = False
lookahead = ''

class ParserBro:
    def get_first(nonTerminal):
        if nonTerminal == 'A':
            return "}~golabi~asghar~;~(" #first(A) = {...}
            result.split('~')


        else:
            return nonTerminal #if nonTerminal is actually a terminal, return terminal


    def get_follow(nonTermial):
        if nonTerminal == 'A':
            return "},golabi,asghar,;,(" #follow(A) = {...}
        elif nonTerminal == 'B':
            return "},,;,(" #follow(A) = {...}

    def get_rhs_grammars(nonTerminal):
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
