# Globals
symbol_table = []
pbIndex = 0
pb = []
semanticStack = []
tmpAddr = 500
wordLength = 4
breakQ = []
returnQ = []

def find_addr(look_ahead):
    global semanticStack
    global symbol_table
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
    global flag
    global printFlag
    global semanticStack
    global pb
    global pbIndex
    global wordLength

    if action == '#pid':
        if look_ahead.value == 'output':
            semanticStack.append('output')
            return
        semanticStack.append(find_addr(look_ahead))
    
    elif action == '#pnum':
        semanticStack.append(f'#{look_ahead.value}')
    

    elif action == '#initVar':
        id = semanticStack.pop()
        typ = semanticStack.pop()
        init_var(typ, id, '')

    elif action == '#initArr':
        arrSlots = semanticStack.pop()
        init_var('arr' , semanticStack.pop() , arrSlots[1:])
    
    elif action == '#start_symbol':
        symbol_table.append('BEGINNING')

    elif action == '#add_function_to_symbol_table':
        
        funcAttr = []
        latestSymbol = symbol_table.pop()
        while latestSymbol != 'BEGINNING':
            funcAttr.append(latestSymbol[2])
            latestSymbol = symbol_table.pop()
        funcAttr.append(semanticStack[-3])
        funcAttr.reverse()
        funcAttr.append(semanticStack[-2])
        funcAttr.append(semanticStack[-1])
        symbol_table.append(('FUNC', semanticStack[-4], funcAttr))
        semanticStack.pop()
        semanticStack.pop()
        semanticStack.pop()
        semanticStack.pop()

    elif action == '#init_variable':
        tmp = get_tmp()
        semanticStack.append(tmp)

    elif action == '#return_address':
        funcName = semanticStack[-4]
        if funcName == 'main':
            return
        returnAdrr = semanticStack[-2]
        fill_pb(pbIndex, 'JP', f'@{returnAdrr}')
        pbIndex = pbIndex + 1

    elif action == '#break':
        breakQ.append(pbIndex)
        pbIndex = pbIndex + 1

    elif action == '#startbreak':
        breakQ.append("begin")

    elif action == '#endbreak':
        index = breakQ.pop()
        while index != 'begin':
            fill_pb(index, 'JP', pbIndex)
            index = breakQ.pop()

    elif action == '#return':
        value = semanticStack.pop()
        returnQ.append((pbIndex, value))
        pbIndex = pbIndex + 2

    elif action == '#startreturn':
        returnQ.append(('begin', '#0'))

    elif action == '#endreturn':
        index = returnQ.pop()
        while index[0] != 'begin':
            fill_pb(index[0], 'ASSIGN', index[1], semanticStack[-1])
            fill_pb(index[0] + 1, 'JP', pbIndex)
            index = returnQ.pop()

    elif action == '#call_function':
        if semanticStack[-1] == 'output':
            return
        function_attributes = []
        for j in range(len(SS) - 1, -1, -1):
            if isinstance(SS[j], list):
                function_attributes = SS[j]
        input_size = len(function_attributes) - 3
        # assign function inputs
        for j in range(input_size):
            add_instruction_to_program_block(i, 'ASSIGN', SS[len(SS) - input_size + j], function_attributes[j + 1])
            i = i + 1
        # assign return address
        add_instruction_to_program_block(i, 'ASSIGN', f'#{i + 2}', function_attributes[input_size + 1])
        i = i + 1
        # go  to function
        add_instruction_to_program_block(i, 'JP', function_attributes[0] + 1)
        i = i + 1
        for j in range(input_size + 1):
            SS.pop()
        # create a new variable and assign function output to it
        address = get_temporary_variables()
        SS.append(address)
        add_instruction_to_program_block(i, 'ASSIGN', function_attributes[input_size + 2], address)
        i = i + 1

    elif action == '#special_save':
        stackTop = semanticStack.pop()
        semanticStack.append(pbIndex)
        semanticStack.append(stackTop)
        pbIndex = pbIndex + 1

    elif action == '#special_save_pair':
        if symbol_table[-1][1] == 'main':
            tmp = get_tmp()
            fill_pb(semanticStack.pop(), 'ADD', '#0', '#0', tmp)
            pbIndex = pbIndex + 1
        else:
            fill_pb(semanticStack.pop(), 'JP', pbIndex)


    elif action == '#assign':
        fill_pb(pbIndex , 'ASSIGN' , semanticStack[-1] , semanticStack[-2])
        semanticStack.pop()
        pbIndex = pbIndex + 1
    
    elif action == '#index':
        indx = semanticStack.pop()
        addr = semanticStack.pop()
        tmp1 = get_tmp()
        tmp2 = get_tmp()
        fill_pb(pbIndex , 'MULT' , '#{}'.format(wordLength) , indx, tmp1)
        pbIndex = pbIndex + 1
        fill_pb(pbIndex , 'ASSIGN' , '#{}'.format(addr) , tmp2)
        pbIndex = pbIndex + 1
        fill_pb(pbIndex , 'ADD' , tmp1 , tmp2 , tmp1)
        pbIndex = pbIndex + 1
        semanticStack.append(f'@{tmp1}')
    
    
    elif action == '#saveID':
        semanticStack.append(look_ahead.value)

    elif action == "#setType":
        semanticStack.append(look_ahead.value)
    
    elif action == '#mult':
        tmp = get_tmp()
        fill_pb(pbIndex , 'MULT' , semanticStack.pop() , semanticStack.pop() , tmp)
        pbIndex = pbIndex + 1
        semanticStack.append(tmp)
    
    elif action == "#saveOperation":
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
    
    elif action == '#inverse':
        tmp = get_tmp()
        fill_pb(pbIndex , 'SUB' , '#0' , semanticStack.pop() , tmp)
        pbIndex = pbIndex + 1
        semanticStack.append(tmp)
    
    elif action == '#pop':
        semanticStack.pop()

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
    
    elif action == '#label':
        semanticStack.append(pbIndex)
    
    elif action == '#while':
        endIndex = semanticStack.pop()
        X = semanticStack.pop()
        label = semanticStack.pop()
        fill_pb(endIndex , 'JPF' , X , '{}'.format(pbIndex + 1))
        fill_pb(pbIndex , 'JP' , label)
        pbIndex = pbIndex + 1
    
    elif action == '#output':
        if len(semanticStack) > 1 and semanticStack[-2] == 'output':
            fill_pb(pbIndex , 'PRINT', semanticStack.pop())
            pbIndex += 1