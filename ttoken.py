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
    FUNCTION = 41


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
            41:'function',

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
            'function': TOKEN.FUNCTION,
        }
        if lexema in reservadas:
            return reservadas[lexema]
        else:
            return TOKEN.ident
        

    @classmethod
    def tabelaOperacoes(cls):
        return {
            # operações aritméticas
            frozenset({(TOKEN.INT, False), TOKEN.mais, (TOKEN.INT, False)}): (TOKEN.INT, False),
            frozenset({(TOKEN.INT, False), TOKEN.menos, (TOKEN.INT, False)}): (TOKEN.INT, False),
            frozenset({(TOKEN.INT, False), TOKEN.multiplica, (TOKEN.INT, False)}): (TOKEN.INT, False),
            frozenset({(TOKEN.INT, False), TOKEN.divide, (TOKEN.INT, False)}): (TOKEN.FLOAT, False),
            frozenset({(TOKEN.INT, False), TOKEN.modulo, (TOKEN.INT, False)}): (TOKEN.INT, False),
            frozenset({(TOKEN.FLOAT, False), TOKEN.mais, (TOKEN.FLOAT, False)}): (TOKEN.FLOAT, False),
            frozenset({(TOKEN.FLOAT, False), TOKEN.mais, (TOKEN.INT, False)}): (TOKEN.FLOAT, False),
            frozenset({(TOKEN.FLOAT, False), TOKEN.multiplica, (TOKEN.INT, False)}): (TOKEN.FLOAT, False),
            frozenset({(TOKEN.FLOAT, False), TOKEN.divide, (TOKEN.INT, False)}): (TOKEN.FLOAT, False),

            # operações relacionais

            frozenset({(TOKEN.INT, False), TOKEN.igual, (TOKEN.INT, False)}): (TOKEN.BOOLEAN, False),
            frozenset({(TOKEN.INT, False), TOKEN.diferente, (TOKEN.INT, False)}): (TOKEN.BOOLEAN, False),
            frozenset({(TOKEN.INT, False), TOKEN.menor, (TOKEN.INT, False)}): (TOKEN.BOOLEAN, False),
            frozenset({(TOKEN.INT, False), TOKEN.menorIgual, (TOKEN.INT, False)}): (TOKEN.BOOLEAN, False),
            frozenset({(TOKEN.INT, False), TOKEN.maior, (TOKEN.INT, False)}): (TOKEN.BOOLEAN, False),
            frozenset({(TOKEN.INT, False), TOKEN.maiorIgual, (TOKEN.INT, False)}): (TOKEN.BOOLEAN, False),
            frozenset({(TOKEN.FLOAT, False), TOKEN.igual, (TOKEN.FLOAT, False)}): (TOKEN.BOOLEAN, False),
            frozenset({(TOKEN.FLOAT, False), TOKEN.diferente, (TOKEN.FLOAT, False)}): (TOKEN.BOOLEAN, False),
            frozenset({(TOKEN.FLOAT, False), TOKEN.menor, (TOKEN.FLOAT, False)}): (TOKEN.BOOLEAN, False),
            frozenset({(TOKEN.FLOAT, False), TOKEN.menorIgual, (TOKEN.FLOAT, False)}): (TOKEN.BOOLEAN, False),
            frozenset({(TOKEN.FLOAT, False), TOKEN.maior, (TOKEN.FLOAT, False)}): (TOKEN.BOOLEAN, False),
            frozenset({(TOKEN.FLOAT, False), TOKEN.maiorIgual, (TOKEN.FLOAT, False)}): (TOKEN.BOOLEAN, False),
            frozenset({(TOKEN.STRING, False), TOKEN.igual, (TOKEN.STRING, False)}): (TOKEN.BOOLEAN, False), # terá essas operações para string????
            frozenset({(TOKEN.STRING, False), TOKEN.diferente, (TOKEN.STRING, False)}): (TOKEN.BOOLEAN, False), # terá essas operações para string????
            frozenset({(TOKEN.INT, False), TOKEN.igual, (TOKEN.FLOAT, False)}): (TOKEN.BOOLEAN, False),
            frozenset({(TOKEN.INT, False), TOKEN.diferente, (TOKEN.FLOAT, False)}): (TOKEN.BOOLEAN, False),
            frozenset({(TOKEN.INT, False), TOKEN.menor, (TOKEN.FLOAT, False)}): (TOKEN.BOOLEAN, False),
            frozenset({(TOKEN.INT, False), TOKEN.menorIgual, (TOKEN.FLOAT, False)}): (TOKEN.BOOLEAN, False),
            frozenset({(TOKEN.INT, False), TOKEN.maior, (TOKEN.FLOAT, False)}): (TOKEN.BOOLEAN, False),
            frozenset({(TOKEN.BOOLEAN, False), TOKEN.igual, (TOKEN.BOOLEAN, False)}): (TOKEN.BOOLEAN, False), # não temos o token boolean, vai ter?
            frozenset({(TOKEN.BOOLEAN, False), TOKEN.diferente, (TOKEN.BOOLEAN, False)}): (TOKEN.BOOLEAN, False),# não temos o token boolean, vai ter?
            frozenset({(TOKEN.BOOLEAN, False), TOKEN.AND, (TOKEN.BOOLEAN, False)}): (TOKEN.BOOLEAN, False),# não temos o token boolean, vai ter?
            frozenset({(TOKEN.BOOLEAN, False), TOKEN.OR, (TOKEN.BOOLEAN, False)}): (TOKEN.BOOLEAN, False),# não temos o token boolean, vai ter?

            # operações unárias
            frozenset({TOKEN.mais, (TOKEN.INT, False)}): (TOKEN.INT, False),
            frozenset({TOKEN.menos, (TOKEN.INT, False)}): (TOKEN.INT, False),
            frozenset({TOKEN.mais, (TOKEN.FLOAT, False)}): (TOKEN.FLOAT, False),
            frozenset({TOKEN.menos, (TOKEN.FLOAT, False)}): (TOKEN.FLOAT, False),

            # valores hardcoded
            frozenset([(TOKEN.INT, False)]): (TOKEN.INT, True),
            frozenset([(TOKEN.FLOAT, False)]): (TOKEN.FLOAT, True),
            # frozenset([(TOKEN.STRING, False)]): (TOKEN.STRING, True),
            # frozenset([(TOKEN.TRUE, False)]): (TOKEN.BOOLEAN, False),
            frozenset([(TOKEN.INT, False), (TOKEN.FLOAT, False)]): (TOKEN.FLOAT, True),
        }