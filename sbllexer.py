''' Lexer for SBL '''

from sly import Lexer


class Expr:
    pass

class Statement:
    pass

class ErrorSyntax(Exception):
    pass

class ErrorSemantic(Exception):
    pass

class Number(Expr):
    def __init__(self,value):
        if '.' in value or 'e' in value:
            self.value = float(value)
        else:
            self.value = int(value)

    def eval(self):
        return self.value

class String(Expr):
    def __init__(self,value):
        self.value = str(value)

    def eval(self):
        return self.value


class SblLexer(Lexer):
    #Tokens
    tokens = {
        NUMBER, STRING,
        TRUE, FALSE,
        PLUS, MINUS, MUL, DIVIDE, DIV, EXPONENT, MOD,
        IN, CONS,
        NOT, ANDALSO, ORELSE,
        LT, LTE, EQ, NEQ, GTE, GT,
        LPAREN, RPAREN, LBRACKET, RBRACKET, LCBRACKET, RCBRACKET,
        TUPLE_INDEX, COMMA, SEMICOLON,
        IF, ELSE, WHILE, PRINT, ASSIGN, ID,
        FUN
    }

    # String containing ignored characters
    ignore = ' \t'

    # Regular expression rules for tokens
    TRUE = r'True'
    FALSE = r'False'
    PLUS = r'\+'
    MINUS = r'-'
    EXPONENT = r'\*\*'
    MUL = r'\*'
    DIVIDE = r'/'
    DIV = r'div'
    MOD = r'mod'
    CONS = r'::'
    NOT = r'not'
    ANDALSO = r'andalso'
    ORELSE = r'orelse'
    EQ = r'=='
    ASSIGN = r'='
    NEQ = r'<>'
    LTE = r'<='
    LT = r'<'
    GTE = r'>='
    GT = r'>'
    LPAREN = r'\('
    RPAREN = r'\)'
    LBRACKET = r'\['
    RBRACKET = r'\]'
    LCBRACKET = r'\{'
    RCBRACKET = r'\}'
    COMMA = r','
    SEMICOLON = r';'
    TUPLE_INDEX = r'#'
    FUN = r'fun'

    #function based definition of NAME tokens
    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'

    ID['if'] = IF
    ID['else'] = ELSE
    ID['while'] = WHILE
    ID['print'] = PRINT
    ID['in'] = IN

    #function based definition of NUMBER tokens
    @_(r'-?(\d*\.?\d*[e][-]?\d+|(\d+\.\d+|\d*\.\d+)|\d+)')
    def NUMBER(self, t):
        t.value = Number(t.value)
        return t

    #function based definition of STRING tokens
    @_(r'\'[^\']*\'|\"[^\"]*\"')
    def STRING(self,t):
        t.value = String(t.value[1:-1])
        return t

    def error(self, t):
        raise ErrorSyntax
        #print('Line %d: Bad character %r' % (self.lineno, t.value[0]))
        #self.index += 1


    '''
    if __name__ == '__main__':
        while True:
            try:
                text = input('calc > ')
                lexer = SblLexer()
                for tok in lexer.tokenize(text):
                    print('type=%r, value=%r' % (tok.type, tok.value))
            except EOFError:
                break
    '''
