from enum import IntEnum
class TOKEN(IntEnum):
    erro = 1
    eof = 2
    ident = 3
    INT = 4
    FLOAT = 5
    CHAR = 6
    valorInt = 7
    valorFloat = 8
    valorChar = 9
    valorString = 10
    IF = 11
    ELSE = 12
    WHILE = 13
    RETURN = 14
    FOR = 15
    BREAK = 16
    CONTINUE = 17
    abreParentese = 18
    fechaParentese = 19
    virgula = 20
    pontoVirgula = 21
    atribuicao = 22
    igual = 23
    diferente = 24
    menor = 25
    menorIgual = 26
    maior = 27
    maiorIgual = 28
    AND = 29
    OR = 30
    NOT = 31
    mais = 32
    menos = 33
    multiplica = 34
    divide = 35
    modulo = 36
    abreChave = 37
    fechaChave = 38
    abrecolchete = 39
    fechacolchete = 40


    @classmethod
    def msg(cls, token):
        nomes = {
            1:'erro',
            2:'<eof>',
            3:'ident',
            4:'int',
            5:'float',
            6:'char',
            7:'valorInt',
            8:'valorFloat',
            9:'valorChar',
            10:'valorString',
            11:'if',
            12:'else',
            13:'while',
            14:'return', 
            15:'for',
            16:'break',
            17:'continue',
            18:'(',
            19:')',
            20:',',
            21:';',
            22:'=',
            23:'==',
            24:'!=',
            25:'<',
            26:'<=',
            27:'>',
            28:'>=',
            29:'&&', # and
            30:'||', # or
            31:'!', # not  
            32:'+',
            33:'-',
            34:'*',
            35:'/',
            36:'%',
            37:'{',
            38:'}',
            39:'[',
            40:']',

        }
        return nomes[token]

    @classmethod
    def reservada(cls, lexema):
        reservadas = {
            'if': TOKEN.IF,
            'else': TOKEN.ELSE,
            'while': TOKEN.WHILE,
            'return': TOKEN.RETURN,
            'int': TOKEN.INT,
            'float': TOKEN.FLOAT,
            'char': TOKEN.CHAR,
            'for': TOKEN.FOR,
            'break': TOKEN.BREAK,
            'continue': TOKEN.CONTINUE,
        }
        if lexema in reservadas:
            return reservadas[lexema]
        else:
            return TOKEN.ident