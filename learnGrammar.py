class Grammar:
    
    @classmethod
    def learnGrammar(cls):
        gf = open('grammar.txt', 'r')
        lines = gf.readlines()
        self.grammar = {'Program':['DeclarationList', '$']}
        for line in lines[1:] :
            line = line.replace('\n', '').split('-> ')
            lhs = line[0]
            rhs = [line[1]]
            if 'ε' in rhs: continue
            if lhs in grammar.keys():
                self.grammar[lhs] = grammar[lhs] + rhs
            else:
                self.grammar[lhs] = rhs




Grammar().learnGrammar()
# test()