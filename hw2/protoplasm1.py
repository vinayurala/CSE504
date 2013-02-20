import cStringIO, tokenize

def get_tokens(lines):
    token_list = []
    token_list = tokenize.generate_tokens(cStringIO.StringIO(lines).readline)

    return token_list

with open('example1.proto') as f:
    lines = f.readlines()
token_list = []
for line in lines:
    if('input' in line or 'print' in line):
        print line
    else:
        tokens = get_tokens(line)
        for x in tokens:
            if (x[1] == '\n' or x[1] == ' ' or x[1] == '' or x[1] == ';'):
                continue
            token_list.append(x[1])

print token_list
