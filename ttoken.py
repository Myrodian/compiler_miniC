#---------------------------------------------------
# Tradutor para a linguagem CALC
#
# versao 1a (mar-2024)
#---------------------------------------------------

from enum import IntEnum
class TOKEN(IntEnum):
    erro = 1
    eof = 2
    ident = 3
    num = 4
    string = 5
    IF = 6
    ELSE = 7
    INICIO = 8
    FIM = 9
    PROG = 10
    abrePar = 11
    fechaPar = 12
    virg = 13
    ptoVirg = 14
    pto = 15
    atrib = 16
    igual = 17
    diferente = 18
    menor = 19
    menorIgual = 20
    maior = 21
    maiorIgual = 22
    AND = 23
    OR = 24
    NOT = 25
    mais = 26
    menos = 27
    multiplica = 28
    divide = 29
    LEIA = 30
    ESCREVA = 31
    abreChave = 32
    fechaChave = 33


    @classmethod
    def msg(cls, token):
        nomes = {
            1:'erro',
            2:'<eof>',
            3:'ident',
            4:'numero',
            5:'string',
            6:'if',
            7:'else',
            8:'inicio',
            9:'fim',
            10:'prog',
            11:'(',
            12:')',
            13:',',
            14:';',
            15:'.',
            16:'=',
            17:'==',
            18:'!=',
            19:'<',
            20:'<=',
            21:'>',
            22:'>=',
            23:'and',
            24:'or',
            25:'not',
            26:'+',
            27:'-',
            28:'*',
            29:'/',
            30:'leia',
            31:'escreva',
            32:'{',
            33:'}',
        }
        return nomes[token]

    @classmethod
    def reservada(cls, lexema):
        reservadas = {
            'prog': TOKEN.PROG,
            'if': TOKEN.IF,
            'inicio': TOKEN.INICIO,
            'fim': TOKEN.FIM,
            'else': TOKEN.ELSE,
            'leia': TOKEN.LEIA,
            'escreva': TOKEN.ESCREVA,
            'and': TOKEN.AND,
            'or': TOKEN.OR,
            'not': TOKEN.NOT
        }
        if lexema in reservadas:
            return reservadas[lexema]
        else:
            return TOKEN.ident
