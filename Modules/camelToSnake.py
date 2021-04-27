def camelCase(x):
    y = ''
    skipNext = False
    for i in range(0, len(x)):
        if skipNext:
            skipNext = False
            continue
        if x[i] == '-' and x[i-1].isalpha() and i+1<len(x) and x[i+1].isalpha():
            y = y + x[i+1].upper()
            skipNext = True
        else:
            y = y + x[i]
    return y




def kinda_snake_case(x):
    for i in range(1, len(x) - 1):
        if x[i].isupper():
            x = x[:i] + '-' + x[i].lower() + x[i+1:]
    return x
