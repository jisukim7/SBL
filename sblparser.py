from sly import Parser
from sbllexer import *

#global vars
vars = {}
#global funcs
funcs = {}


class Boolean(Expr):
    def __init__(self, v):
        if v == 'True':
            self.v = True
        elif v == 'False':
            self.v = False

    def eval(self):
        return self.v


class BinOp(Expr):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

    def eval(self):

        x = self.left.eval()
        y = self.right.eval()
        z = self.op

        if(z == '+' or z == '-' or z == '*' or z == '/' or z == 'div' or z == 'mod' or z == '**'):
            if(type(x) != type(y)):
                if(isinstance(x,float) and isinstance(y,int)):
                    pass
                elif(isinstance(x,int) and isinstance(y,float)):
                    pass
                else:
                    raise ErrorSemantic

        if(z == '/' or z == 'div'):
            if(y == 0):
                raise ErrorSemantic

        if(z == 'orelse' or z == 'andalso'):
            if(isinstance(x,bool) and isinstance(y,bool)):
                pass
            else:
                raise ErrorSemantic


        if(z == '==' or z == '<>' or z == '<' or z == '<=' or z == '>' or z == '>=' ):
            if(not(isinstance(x,str) and isinstance(y,str))):
                pass
            if(type(x) != type(y)):
                if(isinstance(x,float) and isinstance(y,int)):
                    pass
                elif(isinstance(x,int) and isinstance(y,float)):
                    pass
                else:
                    raise ErrorSemantic


        if self.op == 'orelse':
            return x or y
        elif self.op == 'andalso':
            return x and y
        elif self.op == '==':
            return x == y
        elif self.op == '<>':
            return x != y
        elif self.op == '<':
            return x < y
        elif self.op == '<=':
            return x <= y
        elif self.op == '>':
            return x > y
        elif self.op == '>=':
            return x >= y
        elif self.op == '::':
            return [x] + y
        elif self.op == 'in':
            return x in y
        elif self.op == '+':
            return x + y
        elif self.op == '-':
            return x - y
        elif self.op == '*':
            return x * y
        elif self.op == '/':
            return x / y
        elif self.op == 'div':
            return x // y
        elif self.op == 'mod':
            return x % y
        elif self.op == '**':
            return x ** y

class Negation(Expr):
    def __init__(self, right):
        self.right = right

    def eval(self):
        return not self.right.eval()

class List(Expr):
    def __init__(self, v):
        self.v = v
    def eval(self):
        x = self.v.eval()
        if x == None:
            return []
        return [x]

class ListAdd(Expr):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def eval(self):
        x = self.left.eval()
        y = self.right.eval()
        return [x] + y

class Tuples(Expr):
    def __init__(self, v):
        self.v = v
    def eval(self):
        x = self.v.eval()
        return (x,)

class TuplesAdd(Expr):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def eval(self):
        x = self.left.eval()
        y = self.right.eval()

        z = (x,)
        return z + y

class IndexList(Expr):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def eval(self):
        x = self.left.eval()
        y = self.right.eval()

        if(not isinstance(y,int)):
            raise ErrorSemantic
        if(len(x) <= y):
            raise ErrorSemantic

        return x[y]

class IndexTuples(Expr):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def eval(self):
        x = self.left.eval() - 1
        return self.right.eval()[x]



class IndexVar(Expr):
    def __init__(self,v1,v2):
        self.v1 = v1
        self.v2 = v2

    def eval(self):
        list = vars[self.v1]
        return list[self.v2.eval()]


class IndexTupleVar(Expr):
    def __init__(self,v1,v2):
        self.v1 = v1
        self.v2 = v2

    def eval(self):
        x = self.v1.eval() - 1
        y = vars[self.v2]
        return y[x]

#AST node to represent variables
class Variables(Statement):
    def __init__(self,name):
        self.name = name

    def eval(self):
        return vars[self.name]

class Block(Statement):
    def __init__(self,list):
        self.list = list

    def execute(self):
        if(self.list == None):
            return
        for s in self.list:
            s.execute()

class Assignment(Statement):
    def __init__(self,left,right):
        self.left = left
        self.right = right

    def execute(self):
        vars[self.left] = self.right.eval()

class ArrayAssignment(Statement):
    def __init__(self,arrayName, arrayIndex, value):
        self.arrayName = arrayName
        self.arrayIndex = arrayIndex
        self.value = value

    def execute(self):
        x = self.arrayName
        y = self.arrayIndex.eval()
        z = vars[self.value]

        list = vars[x]
        list[y] = z

class Print(Statement):
    def __init__(self,v):
        self.v = v

    def execute(self):
        if(self.v == None):
            return
        else:
            print(self.v.eval())

class IfStatement(Statement):
    def __init__(self,condition,block):
        self.condition = condition
        self.block = block

    def execute(self):
        if self.condition.eval() == True:
            self.block.execute()

class IfElseStatement(Statement):
    def __init__(self,condition,block1,block2):
        self.condition = condition
        self.block1 = block1
        self.block2 = block2

    def execute(self):
        if self.condition.eval() == True:
            self.block1.execute()
        else:
            self.block2.execute()


class WhileLoop(Statement):
    def __init__(self,condition,block):
        self.condition = condition
        self.block = block

    def execute(self):
        while(self.condition.eval()):
            self.block.execute()

#'FUN ID LPAREN params RPAREN ASSIGN block expr SEMICOLON'

class Program:
    def __init__(self, functions, block):
        self.functions = functions
        self.block = block

    def execute(self):
        for fun in self.functions:
            fun.eval()
        self.block.execute()


class Function:
    def __init__(self,name,params,block,expr):
        self.params = params
        self.block = block
        self.expr = expr
        self.name = name

    def eval(self):
        funcs[self.name] = self

    def execute(self):
        self.block.execute()

#'ID LPAREN args RPAREN'
class FunctionCall:
    def __init__(self,name,args):
        self.name = name
        self.args = args

    def eval(self):

        global vars

        function = funcs[self.name]

        func_params = function.params
        fun_call_args = self.args

        if(fun_call_args == None):
            fun_call_args = []

        if(func_params == None):
            func_params = []

        temp = {}
        for i in range(len(func_params)):
            temp[func_params[i]] = fun_call_args[i].eval()

        vars.update(temp)

        function.execute()
        res = function.expr.eval()

        if(res == None):
            raise ErrorSemantic

        return res


class SBLParser(Parser):
    #debugfile = 'parser.out'
    tokens = SblLexer.tokens

    #Parsing Rules
    precedence = (
        ('left',ORELSE),
        ('left',ANDALSO),
        ('left',NOT),
        ('left',EQ,NEQ,LT,LTE,GT,GTE),
        ('right',CONS),
        ('left',IN),
        ('left',PLUS,MINUS),
        ('left',MUL,DIVIDE,DIV,MOD),
        ('right',UMINUS),
        ('right',EXPONENT),
        ('left',LBRACKET,RBRACKET),
        ('left',TUPLE_INDEX),
        ('left',COMMA),
        ('left',LPAREN,RPAREN)
    )

    #### handling of function definition and function call ####

    @_('functions block')
    def program(self,p):
        return Program(p.functions, p.block)

    @_('block')
    def program(self,p):
        return p.block

    @_('functions function')
    def functions(self,p):
        return p.functions + [p.function]

    @_('function')
    def functions(self,p):
        return [p.function]


    @_('FUN ID LPAREN params RPAREN ASSIGN block expr SEMICOLON')
    def function(self,p):
        return Function(p.ID, p.params, p.block, p.expr)


    @_('ID COMMA params')
    def params(self,p):
        return [p.ID] + p.params

    @_('ID')
    def params(self,p):
        return [p.ID]

    @_('empty')
    def params(self,p):
        return None


    @_('ID LPAREN args RPAREN')
    def fun_call(self,p):
        return FunctionCall(p.ID,p.args)

    @_('expr COMMA args')
    def args(self,p):
        return [p.expr] + p.args


    @_('expr')
    def args(self,p):
        return [p.expr]

    @_('empty')
    def args(self,p):
        return None


    @_('LCBRACKET RCBRACKET')
    def block(self,p):
        return Block(None)

    @_('LCBRACKET statements RCBRACKET')
    def block(self,p):
        return Block(p.statements)

    @_('statements statement')
    def statements(self,p):
        return p.statements + [p.statement]

    @_('statement')
    def statements(self,p):
        return [p.statement]

    @_('expr SEMICOLON')
    def statement(self,p):
        return p.expr

    @_('ID ASSIGN expr SEMICOLON')
    def statement(self,p):
        return Assignment(p.ID, p.expr)

    @_('ID LBRACKET expr RBRACKET ASSIGN ID SEMICOLON')
    def statement(self,p):
        return ArrayAssignment(p.ID0, p.expr, p.ID1)

    '''

    @_('ID LBRACKET ID RBRACKET ASSIGN ID SEMICOLON')
    def statement(self,p):
        return ArrayAssignment(p.ID0, p.ID1, p.ID2)

    @_('ID LBRACKET ID RBRACKET ASSIGN expr SEMICOLON')
    def statement(self,p):
        return ArrayAssignment(p.ID0, p.ID1, p.expr)

    @_('ID LBRACKET expr RBRACKET ASSIGN expr SEMICOLON')
    def statement(self,p):
        return ArrayAssignment(p.ID, p.expr0, p.expr1)
    '''


    @_('PRINT LPAREN expr RPAREN SEMICOLON')
    def statement(self,p):
        return Print(p.expr)

    @_('IF LPAREN expr RPAREN block')
    def statement(self,p):
        return IfStatement(p.expr, p.block)

    @_('IF LPAREN expr RPAREN block ELSE block')
    def statement(self,p):
        return IfElseStatement(p.expr,p.block0,p.block1)

    @_('WHILE LPAREN expr RPAREN block')
    def statement(self,p):
        return WhileLoop(p.expr, p.block)

    @_('ID')
    def expr(self, p):
        return Variables(p.ID)

    @_(
    'expr ORELSE expr',
    'expr ANDALSO expr',
    'expr EQ expr',
    'expr NEQ expr',
    'expr LT expr',
    'expr LTE expr',
    'expr GT expr',
    'expr GTE expr',
    'expr CONS expr',
    'expr IN expr',
    'expr PLUS expr',
    'expr MINUS expr',
    'expr MUL expr',
    'expr DIVIDE expr',
    'expr DIV expr',
    'expr MOD expr',
    'expr EXPONENT expr')
    def expr(self,p):
        return BinOp(p[1],p.expr0,p.expr1)

    @_('TRUE',
    'FALSE')
    def boolean(self,p):
        return Boolean(p[0])


    @_('MINUS expr %prec UMINUS')
    def expr(self,p):
        return -p.expr

    @_('NOT expr')
    def expr(self,p):
        return Negation(p.expr)

    @_('LPAREN expr RPAREN')
    def expr(self,p):
        return p.expr

    #list
    @_('LBRACKET list_expr RBRACKET')
    def list(self,p):
        return p.list_expr

    @_('LBRACKET RBRACKET')
    def empty_list(self,p):
        return List(None)

    @_('expr')
    def list_expr(self,p):
        return List(p[0])

    @_('expr COMMA list_expr')
    def list_expr(self,p):
        return ListAdd(p.expr,p.list_expr)

    #tuples
    @_('LPAREN tup_expr RPAREN')
    def tuples(self,p):
        return p.tup_expr

    @_('expr')
    def tup_expr(self,p):
        return Tuples(p[0])

    @_('expr COMMA')
    def tup_expr(self,p):
        return Tuples(p[0])

    @_('expr COMMA tup_expr')
    def tup_expr(self,p):
        return TuplesAdd(p.expr,p.tup_expr)

    @_('ID LBRACKET expr RBRACKET')
    def var_list_index(self,p):
        return IndexVar(p.ID,p.expr)


    #indexing list
    @_('expr LBRACKET expr RBRACKET')
    def index_list(self,p):

        return IndexList(p.expr0,p.expr1)

    #indexing tuple
    @_('TUPLE_INDEX expr tuples')
    def index_tuple(self,p):
        return IndexTuples(p.expr,p.tuples)

    @_('TUPLE_INDEX expr ID')
    def var_tuple_index(self,p):
        return IndexTupleVar(p.expr,p.ID)

    @_('TUPLE_INDEX expr LPAREN ID RPAREN')
    def var_tuple_index_err(self,p):
        raise ErrorSemantic


    @_('NUMBER',
    'STRING',
    'boolean',
    'list',
    'empty_list',
    'index_list',
    'tuples',
    'index_tuple',
    'var_list_index',
    'var_tuple_index',
    'var_tuple_index_err',
    'fun_call')
    #'var_tuple_index_err')
    def expr(self,p):
        return p[0]


    @_('')
    def empty(self, p):
        pass


    def error(self,p):
        if p:
            raise ErrorSemantic
        else:
            return None
