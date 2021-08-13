import sys as sys
from sbllexer import *
from sblparser import SBLParser

if __name__ == '__main__':
    lexer = SblLexer()
    parser = SBLParser()
    try:
        input_file = open(sys.argv[1],'r')
        data = input_file.read().replace('\n','')
        result = parser.parse(lexer.tokenize(data))
        if(result != None):
            result.execute()

        '''
        if(isinstance(result,str)):
            result = "'{}'".format(result)
        if(result != None):
            print(result)
        #print(vars)
        '''
    except ErrorSyntax:
        print("SYNTAX ERROR")
    except ErrorSemantic:
        print("SEMANTIC ERROR")
