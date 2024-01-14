import operator as op

Symbol = str
Number = (int, float)
Atom = (Symbol, Number)
List = list
Exp = (List, Atom)

def add(*args):
    sum = 0
    for a in args:
        sum += a
    return sum

def sub(*args):
    if len(args) == 1:
        return -args[0]
    sum = args[0]
    for n in args[1:]:
        sum -= n
    return sum

def mul(*args):
    sum = 1
    for n in args:
        sum *= n
    return sum

class Env(dict):
    def __init__(self, parms=(), args=(), outer=None):
        self.update(zip(parms, args))
        self.outer = outer

    def find(self, var):
        return self if (var in self) else self.outer.find(var)


global_env = Env()
global_env.update({
    '+':add, '-':sub, '*':mul, '/':op.truediv, 
    '>':op.gt, '<':op.lt, '>=':op.ge, '<=':op.le, '=':op.eq, 
    'abs':     abs,
    'append':  op.add,  
    'begin':   lambda *x: x[-1],
    'car':     lambda x: x[0],
    'cdr':     lambda x: x[1:], 
    'cons':    lambda x,y: [x] + y,
    'eq?':     op.is_, 
    'equal?':  op.eq, 
    'length':  len, 
    'list':    lambda *x: list(x), 
    'list?':   lambda x: isinstance(x,list), 
    'map':     map,
    'max':     max,
    'min':     min,
    'not':     op.not_,
    'null?':   lambda x: x == [], 
    'number?': lambda x: isinstance(x, Number),   
    'procedure?': callable,
    'round':   round,
    'symbol?': lambda x: isinstance(x, Symbol),
})


class Procedure(object):
    def __init__(self, parms, body, env):
        self.parms, self.body, self.env = parms, body, env
    def __call__(self, *args):
        return evaluate(self.body, Env(self.parms, args, self.env))


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

def read(s: str):
    return parse(tokenizer(s))

def evaluate(x, env=global_env):
    if isinstance(x, Symbol):
        return env.find(x)[x]
    elif not isinstance(x, List):
        return x
    elif x[0] == 'if':
        (_, test, conseq, alt) = x
        exp = (conseq if evaluate(test, env) else alt)
        return evaluate(exp, env)
    elif x[0] == 'define':
        (_, symbol, exp) = x
        env[symbol] = evaluate(exp, env)
    elif x[0] == 'lambda':
        (_, parms, body) = x
        return Procedure(parms, body, env)
    else:
        proc = evaluate(x[0], env)
        args = [evaluate(arg, env) for arg in x[1:]]
        return proc(*args)

#print(read())
#print(tokenizer("(this is a lisp expression (+ 1 2 3))"))

def repl():
    while True:
        s = input("> ")
        val = evaluate(read(s))
        if val is not None:
            print(schemestr(val))

def schemestr(exp):
    if isinstance(exp, List):
        return '(' + ' '.join(map(schemestr, exp)) + ')'
    else:
        return str(exp)

if __name__ == '__main__':
    repl()

