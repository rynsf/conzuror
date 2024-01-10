Symbol = str
Number = (int, float)
Atom = (Symbol, Number)
List = list
Exp = (List, Atom)
Env = dict

def add(*args):
    sum = 0
    for a in args:
        sum += a
    return sum

global_env = {
    '+': add,
}

def tokenizer(s):
    return s.replace('(', ' ( ').replace(')', ' ) ').split()

def parse(tokens):
    if len(tokens) == 0:
        #return read()
        raise SyntaxError('unexpected EOF')

    token = tokens.pop(0)
    if token == '(':
        exp = []
        while tokens[0] != ')':
            exp.append(parse(tokens))
        tokens.pop(0)
        return exp
    elif token == ')':
        raise SyntaxError('unexpected )')
    else:
        return atom(token)

def atom(token):
    try: return int(token)
    except ValueError:
        try: return float(token)
        except ValueError:
            return Symbol(token)

def read():
    return parse(tokenizer(input("> ")))

def evaluate(x, env=global_env):
    if isinstance(x, Symbol):
        return env[x]
    elif isinstance(x, Number):
        return x
    elif x[0] == 'if':
        (_, test, conseq, alt) = x
        exp = (conseq if eval(test, env) else alt)
        return evaluate(exp, env)
    elif x[0] == 'define':
        (_, symbol, exp) = x
        env[symbol] = evaluate(exp, env)
    else:
        proc = evaluate(x[0], env)
        args = [evaluate(arg, env) for arg in x[1:]]
        return proc(*args)

#print(read())
#print(tokenizer("(this is a lisp expression (+ 1 2 3))"))

def repl():
    while True:
        val = evaluate(read())
        if val is not None:
            print(schemestr(val))

def schemestr(exp):
    if isinstance(exp, List):
        return '(' + ' '.join(map(schemestr, exp)) + ')'
    else:
        return str(exp)

repl()

