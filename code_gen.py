# Globals
symbol_table = []
pbIndex = 0
pb = []
semanticStack = []
tmpAddr = 500
wordLength = 4

def find_addr(look_ahead):
    global semanticStack
    for i in symbol_table:
        if look_ahead.value == i[1]:
            return i[2]
        


def fill_pb(indx , op , A1 , A2 = '' , R = ''):
    global pb
    while len(pb) <= indx:
        pb.append('')
    pb[indx] = "({}, {}, {}, {})".format(op , A1 , A2 , R)



def get_tmp(slots = 1):
    global pbIndex
    global tmpAddr
    global wordLength
    addr = str(tmpAddr)
    for i in range(slots):
        fill_pb(pbIndex , 'ASSIGN' , '#0' , str(tmpAddr))
        tmpAddr = tmpAddr + wordLength
        pbIndex = pbIndex + 1
    return addr


def init_var(varType , varId , slots):
    global pbIndex
    global symbol_table
    if varType == 'arr':
        arrAddress = get_tmp()
        arr = get_tmp(int(slots))
        fill_pb(pbIndex , 'ASSIGN' , '#{}'.format(arr) , arrAddress)
        pbIndex = pbIndex + 1
        symbol_table.append('arr' , varId , arrAddress)
    elif varType == 'int':
        intAddress = get_tmp()
        symbol_table.append('int' ,varId , intAddress)




def generateCode(look_ahead , action):
    global semanticStack
    global pb
    global pbIndex
    global wordLength
    match (action):
        case '#pid':
            semanticStack.append(find_addr(look_ahead))
        case 'pnum':
            semanticStack.append('#{}'.format(look_ahead.value))
        case 'mult':
            tmp = get_tmp()
            fill_pb(pbIndex , 'MULT' , semanticStack[len(semanticStack) - 1] , semanticStack[len(semanticStack) - 1] , tmp)
            semanticStack.pop()
            semanticStack.pop()
            pbIndex = pbIndex + 1
            semanticStack.append(tmp)
        case '#setvar':
            init_var('int' , semanticStack.pop() , '')
        case 'setarr':
            arrSlots = semanticStack.pop()
            init_var('arr' , semanticStack.pop() , arrSlots[1:])
        case '#assign':
            fill_pb(pbIndex , 'ASSIGN' , semanticStack[len(semanticStack) - 1] , semanticStack[len(semanticStack) - 2])
            semanticStack.pop()
            pbIndex = pbIndex + 1
        case '#index':
            indx = semanticStack.pop()
            addr = semanticStack.pop()
            tmp1 = get_tmp()
            tmp2 = get_tmp()
            fill_pb(pbIndex , 'MULT' , '#{}'.format(wordLength) , tmp1)
            pbIndex = pbIndex + 1
            fill_pb(pbIndex , 'ASSIGN' , '@{}'.format(addr) , tmp2)
            pbIndex = pbIndex + 1
            fill_pb(pbIndex , 'ADD' , tmp1 , tmp2 , tmp1)
            pbIndex = pbIndex + 1
            semanticStack.append('@{}'.format(tmp1))
        case '#pop':
            semanticStack.pop()
        case '#saveinp':
            semanticStack.append(look_ahead.value)
        case 'opperation':
            var2 = semanticStack.pop()
            op = semanticStack.pop()
            var1 = semanticStack.pop()
            tmp = get_tmp()
            match(op):
                case '*':
                    fill_pb(pbIndex , 'MULT' , var1 , var2 , tmp)
                case '+':
                    fill_pb(pbIndex , 'ADD' , var1 , var2 , tmp)
                case '-':
                    fill_pb(pbIndex , 'SUB' , var1 , var2 , tmp)
                case '==':
                    fill_pb(pbIndex , 'EQ' , var1 , var2 , tmp)
                case '<':
                    fill_pb(pbIndex , 'LT' , var1 , var2 , tmp)
            pbIndex = pbIndex + 1
            semanticStack.append(tmp)
        case '#signed':
            tmp = get_tmp()
            fill_pb(pbIndex , 'SUB' , '#0' , semanticStack.pop() , tmp)
            pbIndex = pbIndex + 1
            semanticStack.append(tmp)
        case '#save':
            semanticStack.append(pbIndex)
            pbIndex = pbIndex + 1
        case '#jpf_save':
            jpFrom = semanticStack.pop()
            X = semanticStack.pop()
            fill_pb(jpFrom , 'JPF' , X , '{}'.format(pbIndex + 1))
            semanticStack.append(pbIndex)
            pbIndex = pbIndex + 1
        case '#jp':
            jpFrom = semanticStack.pop()
            fill_pb(int(jpFrom) , 'JP' , pbIndex)
        case '#lable':
            semanticStack.append(pbIndex)
        case '#while':
            endIndex = semanticStack.pop()
            X = semanticStack.pop()
            label = semanticStack.pop()
            fill_pb(endIndex , 'JPF' , X , '{}'.format(pbIndex + 1))
            fill_pb(pbIndex , 'JP' , label)
            pbIndex = pbIndex + 1

