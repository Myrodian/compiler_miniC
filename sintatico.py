from ttoken import TOKEN
from lexico import Lexico
import traceback

class Sintatico:
    def __init__(self, nomeArquivo):
        self.lexico = Lexico(nomeArquivo)

    def traduz(self):
        self.tokenLido = self.lexico.getToken()
        try:
            self.program()
            self.consome(TOKEN.eof)
            print("Traduzido com sucesso!")
        except Exception as e:
            print("Falha na tradução:", e)
            traceback.print_exc()

    def consome(self, tokenAtual):
        (token, lexema, linha, coluna) = self.tokenLido
        if tokenAtual == token:
            self.tokenLido = self.lexico.getToken()
        else:
            msgTokenLido = TOKEN.msg(token)
            msgTokenAtual = TOKEN.msg(tokenAtual)
            print(f"Erro na linha {linha}, coluna {coluna}: ")

            if token == TOKEN.erro:
                msg = lexema
            else:
                msg = msgTokenLido
            print(f"Era esperado {msgTokenAtual} mas foi lido {msg}")
            raise Exception("Erro Sintático")


    def program(self): # Program ->  Function Program | LAMBDA
        if self.tokenLido[0] in (TOKEN.INT, TOKEN.FLOAT, TOKEN.CHAR):
            self.function()
            self.program()
        else:
            # LAMBDA
            pass
        
    def function(self): # Function -> Type ident ( ArgList ) CompoundStmt
        self.type()
        self.consome(TOKEN.ident)
        self.consome(TOKEN.abreParentese)
        self.argList()
        self.consome(TOKEN.fechaParentese)
        self.compoundStmt()

    def type(self): # Type -> int | float | char
        if self.tokenLido[0] in (TOKEN.INT, TOKEN.FLOAT, TOKEN.CHAR):
            self.consome(self.tokenLido[0])

    def argList(self): # ArgList ->  Arg RestoArgList | LAMBDA
        if self.tokenLido[0] in (TOKEN.INT, TOKEN.FLOAT, TOKEN.CHAR):
            self.arg()
            self.restoArgList()
        else:
            # LAMBDA
            pass

    def restoArgList(self): # RestoArgList -> , Arg RestoArgList | LAMBDA
        if self.tokenLido[0] == TOKEN.virgula:
            self.consome(TOKEN.virgula)
            self.arg()
            self.restoArgList()
        else:
            # LAMBDA
            pass

    def arg(self): # Arg -> Type IdentArg
        self.type()
        self.identArg()

        