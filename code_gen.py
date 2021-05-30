# Globals
symbol_table = []
pbIndex = 0
pb = []
semanticStack = []
tmpAddr = 500
wordLength = 4

def find_addr(look_ahead):
    global semanticStack
    global symbol_table

    print("\n\n\t find addr for ")
    print(str(look_ahead))
    print("semanticStack = ")
    print(semanticStack)
    print("symbol_table = ")
    print(symbol_table)

    for i in symbol_table:
        if look_ahead.value == i[1]:
            return i[2]
        


def fill_pb(indx , op , A1 , A2 = '' , R = ''):
    global pb
    while len(pb) <= indx:
        pb.append('')
    pb[indx] = f"({op}, {A1}, {A2}, {R})"

def write_pb():
    global pb
    output_file = open('output.txt', 'w')
    for index, i in enumerate(pb):
        output_file.write(f"{index}\t{i}\n")
    output_file.close()




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

    print(f'\n\ninit var   {varId}\n\n')

    if varType == 'arr':
        arrAddress = get_tmp()
        arr = get_tmp(int(slots))
        fill_pb(pbIndex , 'ASSIGN' , '#{}'.format(arr) , arrAddress)
        pbIndex = pbIndex + 1
        symbol_table.append(('arr' , varId , arrAddress))
    
    elif varType == 'int' or varType == 'void':
        intAddress = get_tmp()
        symbol_table.append((varType ,varId , intAddress))




def generateCode(look_ahead , action):
    global semanticStack
    global pbIndex
    global wordLength

    print(f"\t\t\t SS: {semanticStack}")
    print(f"\t LA = {look_ahead} \t\t\t\t action = {action}\t \n\n")

    if action == '#pid':
        semanticStack.append(find_addr(look_ahead))
    
    elif action == '#pnum':
        semanticStack.append(f'#{look_ahead.value}')
    
    elif action == '#mult':
        tmp = get_tmp()
        fill_pb(pbIndex , 'MULT' , semanticStack[len(semanticStack) - 1] , semanticStack[len(semanticStack) - 1] , tmp)
        semanticStack.pop()
        semanticStack.pop()
        pbIndex = pbIndex + 1
        semanticStack.append(tmp)
    
    elif action == '#setvar':
        id = semanticStack.pop()
        typ = semanticStack.pop()
        init_var(typ, id, '')
    
    elif action == '#setarr':
        arrSlots = semanticStack.pop()
        init_var('arr' , semanticStack.pop() , arrSlots[1:])
    
    elif action == '#assign':
        fill_pb(pbIndex , 'ASSIGN' , semanticStack[len(semanticStack) - 1] , semanticStack[len(semanticStack) - 2])
        semanticStack.pop()
        pbIndex = pbIndex + 1
    
    elif action == '#index':
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
        semanticStack.append(f'@{tmp1}')
    
    elif action == '#pop':
        semanticStack.pop()
    
    elif action == '#saveinp':
        semanticStack.append(look_ahead.value)

    elif action == "#setType":
        semanticStack.append(look_ahead.value)
    
    elif action == '#opperation':
        var2 = semanticStack.pop()
        op = semanticStack.pop()
        var1 = semanticStack.pop()
        tmp = get_tmp()

        if op == '*':
            fill_pb(pbIndex , 'MULT' , var1 , var2 , tmp)
        elif op == '+':
            fill_pb(pbIndex , 'ADD' , var1 , var2 , tmp)
        elif op == '-':
            fill_pb(pbIndex , 'SUB' , var1 , var2 , tmp)
        elif op == '==':
            fill_pb(pbIndex , 'EQ' , var1 , var2 , tmp)
        elif op == '<':
            fill_pb(pbIndex , 'LT' , var1 , var2 , tmp)

        pbIndex = pbIndex + 1
        semanticStack.append(tmp)
    
    elif action == '#signed':
        tmp = get_tmp()
        fill_pb(pbIndex , 'SUB' , '#0' , semanticStack.pop() , tmp)
        pbIndex = pbIndex + 1
        semanticStack.append(tmp)
    
    elif action == '#save':
        semanticStack.append(pbIndex)
        pbIndex = pbIndex + 1
    
    elif action == '#jpf_save':
        jpFrom = semanticStack.pop()
        X = semanticStack.pop()
        fill_pb(jpFrom , 'JPF' , X , '{}'.format(pbIndex + 1))
        semanticStack.append(pbIndex)
        pbIndex = pbIndex + 1
    
    elif action == '#jp':
        jpFrom = semanticStack.pop()
        fill_pb(int(jpFrom) , 'JP' , pbIndex)
    
    elif action == '#lable':
        semanticStack.append(pbIndex)
    
    elif action == '#while':
        endIndex = semanticStack.pop()
        X = semanticStack.pop()
        label = semanticStack.pop()
        fill_pb(endIndex , 'JPF' , X , '{}'.format(pbIndex + 1))
        fill_pb(pbIndex , 'JP' , label)
        pbIndex = pbIndex + 1

