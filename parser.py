import anytree

#Global flags
hasLearntTheGrammar = False

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
        return AllRHSfromGrammarWhere_nonTerminal_isOntheLHS





def procedure(nonTerminal, la):
    if hasLearntTheGrammar == False:
        learnGrammar()
    
    rhs = ParserBro.get_rhs_grammars(nonTerminal)
    rhss = rhs.slipt('~')
    for r in rhss: # except for epsilon 
        rr = r.split(' ') #first token/non_terminal = rr[0]
        frists = ParserBro.getFirst(rr[0]).split('~')
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



def learnGrammar():
    print("i'm learning boss")