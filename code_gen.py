import scanner
# Globals
symbol_table = []
pbIndex = 0
pb = []
semanticStack = []
scope_stack = []
tmpAddr = 500
wordLength = 4
forElementsCount = 0
breakQ = []
returnQ = []
functionCallArgsCount = 0
semanticErrorFile = open('semantic_errors.txt' , 'w')
semanticErrorFileEmpty = True


def semanticError(message = '', lineOffset = 0):
    global semanticErrorFileEmpty
    lineNo = scanner.lineNo
    if semanticErrorFileEmpty:
        semanticErrorFileEmpty = False
    semanticErrorFile.write(f'#{lineNo - lineOffset} : Semantic Error! {message}\n')


def get_type(addr):
    global symbol_table
    if addr.startswith('#'):
        return 'int'
    for i in symbol_table[::-1]:
        if addr == i[2]:
            return i[0] 


def find_addr(look_ahead):
    global semanticStack
    global symbol_table
    for i in symbol_table[::-1]:
        if look_ahead.value == i[1]:
            return i[2]
    semanticError(f'\'{look_ahead.value}\' is not defined')

def find_name(addr):
    global symbol_table
    for i in symbol_table[::-1]:
        if addr == i[2]:
            return i[1]
        

def fill_pb(indx , op , A1 , A2 = '' , R = ''):
    global pb
    while len(pb) <= indx:
        pb.append('')
    pb[indx] = f"({op}, {A1}, {A2}, {R})"

def write_pb():
    global pb
    output_file = open('output.txt', 'w')
    if semanticErrorFileEmpty:
        for index, i in enumerate(pb):
            output_file.write(f"{index}\t{i}\n")
    else :
        output_file.write("The code has not been generated")
    output_file.close()
    if semanticErrorFileEmpty:
        semanticErrorFile.write('The input program is semantically correct.')
    semanticErrorFile.close()


def get_tmp(slots = 1):
    global pbIndex
    global tmpAddr
    global wordLength
    addr = str(tmpAddr)
    for _ in range(slots):
        fill_pb(pbIndex , 'ASSIGN' , '#0' , str(tmpAddr))
        tmpAddr = tmpAddr + wordLength
        pbIndex = pbIndex + 1
    return addr


def init_var(varType , varId , slots):
    global pbIndex
    global symbol_table

    if varType == 'array':
        arrAddress = get_tmp()
        arr = get_tmp(int(slots))
        fill_pb(pbIndex , 'ASSIGN' , '#{}'.format(arr) , arrAddress)
        pbIndex = pbIndex + 1
        symbol_table.append(('array' , varId , arrAddress))
    
    elif varType == 'int' or varType == 'void':
        intAddress = get_tmp()
        symbol_table.append((varType ,varId , intAddress))


def functionCall():
    global semanticStack
    global pbIndex
    global functionCallArgsCount

    if semanticStack[-1] == 'output': return
    ssLen = len(semanticStack)
    funcArgs = []
    
    for s in semanticStack[::-1]:
        if isinstance(s, list):
            funcArgs = s
            break;
    else:
        return
    
    inputLen = len(funcArgs) - 3

    funcName = find_name(semanticStack[-1 -functionCallArgsCount])

    if inputLen != functionCallArgsCount:
        semanticError(f"Mismatch in numbers of arguments of \'{funcName}\'")
        for _ in range(functionCallArgsCount): semanticStack.pop()
        return

    # assign function inputs
    for i in range(inputLen):
        var1 = semanticStack[ssLen - inputLen + i]
        var2 = funcArgs[i+1]
        functypes = []
        for j in symbol_table:
            if j[0] == 'FUNC' and j[2] == funcArgs: functypes = j[3]
        if get_type(var1) != functypes[i]:
            semanticError(f"Mismatch in type of argument {i+1} of \'{funcName}\'. Expected \'{functypes[i]}\' but got \'{get_type(var1)}\' instead.")
        fill_pb(pbIndex, 'ASSIGN', var1, var2)
        pbIndex = pbIndex + 1

    # assign return address after function compeletion
    fill_pb(pbIndex, 'ASSIGN', f'#{pbIndex + 2}', funcArgs[inputLen + 1])
    pbIndex = pbIndex + 1

    # go  to function //second initvar is for function location
    fill_pb(pbIndex, 'JP', funcArgs[0] + 1)
    pbIndex = pbIndex + 1
    for _ in range(inputLen + 1):
        semanticStack.pop()
        
    # create a new variable and assign function output to it
    addr = get_tmp()
    semanticStack.append(addr)
    fill_pb(pbIndex, 'ASSIGN', funcArgs[inputLen + 2], addr)
    pbIndex = pbIndex + 1




def generateCode(look_ahead , action):
    global semanticStack
    global pb
    global pbIndex
    global scope_stack
    global wordLength
    global forElementsCount
    global functionCallArgsCount
    global breakQ
    global returnQ

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
        if typ == 'void':
            semanticError(f'Illegal type of void for {id}', 1)
        init_var(typ, id, '')

    elif action == '#initArr':
        arrSlots = semanticStack.pop()
        id = semanticStack.pop()
        if semanticStack.pop() == 'void':
            semanticError('void var init')
        
        init_var('array' , id , arrSlots[1:])

    elif action == '#FuncStart':
        stackTop = semanticStack.pop()
        semanticStack.append(pbIndex)
        semanticStack.append(stackTop)
        pbIndex = pbIndex + 1
        symbol_table.append('BEGINNING')


    elif action == '#addFuncToSymTable':
        funcAttr = []
        funcAttrType = []
        latestSymbol = symbol_table.pop()
        while latestSymbol != 'BEGINNING':
            funcAttr.append(latestSymbol[2])
            funcAttrType.append(latestSymbol[0])
            latestSymbol = symbol_table.pop()
        funcAttr.append(semanticStack[-3])
        funcAttr.reverse()
        funcAttr.append(semanticStack[-2])
        funcAttr.append(semanticStack[-1])
        symbol_table.append(('FUNC', semanticStack[-4], funcAttr, funcAttrType))
        for _ in range(4): semanticStack.pop()

        if symbol_table[-1][1] != 'main':
            fill_pb(semanticStack.pop(), 'JP', pbIndex)
        semanticStack.pop()


    elif action == '#init_func_variables':
        for _ in range(2):
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
        if len(breakQ) == 0:
            semanticError("No 'while' or 'switch' found for 'break'.", 1)       
        breakQ.append(pbIndex)
        pbIndex = pbIndex + 1

    elif action == '#break_start':
        breakQ.append("begin")

    elif action == '#break_end':
        index = breakQ.pop()
        while index != 'begin':
            fill_pb(index, 'JP', pbIndex)
            index = breakQ.pop()

    elif action == '#return':
        value = semanticStack.pop()
        returnQ.append((pbIndex, value))
        pbIndex = pbIndex + 2
    
    elif action == "#empty_return":
        returnQ.append((pbIndex, '#0'))
        pbIndex = pbIndex + 2

    elif action == '#return_start':
        returnQ.append(('begin', '#0'))

    elif action == '#return_end':
        index = returnQ.pop()
        while index[0] != 'begin':
            fill_pb(index[0], 'ASSIGN', index[1], semanticStack[-1])
            fill_pb(index[0] + 1, 'JP', pbIndex)
            index = returnQ.pop()

    elif action == '#FunctionCall':
        functionCall()
        functionCallArgsCount = 0

    elif action == "#funcArgGiven":
        functionCallArgsCount += 1

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
        fill_pb(pbIndex , 'ASSIGN' , '@{}'.format(addr) , tmp2)
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

        if var1 == None or var2 == None:
            var1 = '#0'
            var2 = '#0'
        
        type1 = get_type(var1)
        type2 = get_type(var2)

        if (type1 == 'void' and type2 != 'void') or (type1 != 'void' and type2 =='void') :
            semanticError(f'Type mismatch in operands, Got {type2} instead of {type1}')
        
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
    

    #FOR
    elif action == "#iteration_start":
        t = get_tmp()
        fill_pb(pbIndex, 'ASSIGN', f'#{pbIndex+1}', t)
        semanticStack.append(t) # address of the i = x assignment
        semanticStack.append(find_addr(look_ahead))
        pbIndex += 1
        forElementsCount = 0

    elif action == "#save_for_var":
        iterator = semanticStack.pop()
        fill_pb(pbIndex, 'ASSIGN', find_addr(look_ahead), iterator)
        pbIndex += 1
        semanticStack.append(pbIndex)
        semanticStack.append(iterator)
        pbIndex += 1
        forElementsCount += 1
    
    elif action == "#jmp_end":
        semanticStack.append(pbIndex) # -> this pbIndex will later be filled with jp to the end of forstmt
        pbIndex += 1

    elif action == "#jmp_start":
        fill_pb(semanticStack.pop(), 'JP', pbIndex + 2)
        fill_pb(pbIndex, 'ADD', '#2', semanticStack[-2], semanticStack[-2])
        fill_pb(pbIndex + 1, 'JP', f'@{semanticStack[-2]}')
        semanticStack.pop()
        semanticStack.pop() 
        pbIndex += 2

    elif action == "#set_start_for":
        jmp_end_index = semanticStack.pop()
        iterator = semanticStack.pop()
        for k in range (0, forElementsCount):
            fill_pb(semanticStack.pop(), 'JP', pbIndex)
        forElementsCount = 0
        semanticStack.append(iterator)
        semanticStack.append(jmp_end_index)




    elif action == '#scope_start':
        scope_stack.append(len(symbol_table))

    elif action == '#scope_end':
        for i in range (0, len(symbol_table) - scope_stack.pop()):
            symbol_table.pop()

    elif action == '#output':
        if len(semanticStack) > 1 and semanticStack[-2] == 'output':
            fill_pb(pbIndex , 'PRINT', semanticStack.pop())
            pbIndex += 1