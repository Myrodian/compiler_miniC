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
    abrePar = 18
    fechaPar = 19
    virg = 20
    ptoVirg = 21
    pto = 22
    atrib = 23
    igual = 24
    diferente = 25
    menor = 26
    menorIgual = 27
    maior = 28
    maiorIgual = 29
    AND = 30
    OR = 31
    NOT = 32
    mais = 33
    menos = 34
    multiplica = 35
    divide = 36
    modulo = 37
    abreChave = 38
    fechaChave = 39
    abrecolchete = 40
    fechacolchete = 41


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
            14:'program',
            15:'for',
            16:'break',
            17:'continue',
            18:'(',
            19:')',
            20:',',
            21:';',
            22:'.',
            23:'=',
            24:'==',
            25:'!=',
            26:'<',
            27:'<=',
            28:'>',
            29:'>=',
            30:'&&', # and
            31:'||', # or
            32:'!', # not  
            33:'+',
            34:'-',
            35:'*',
            36:'/',
            37:'%',
            38:'{',
            39:'}',
            40:'[',
            41:']',

        }
        return nomes[token]

    @classmethod
    def reservada(cls, lexema):
        reservadas = {
            'if': TOKEN.IF,
            'else': TOKEN.ELSE,
            'and': TOKEN.AND,
            'or': TOKEN.OR,
            'not': TOKEN.NOT,
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