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

        # 🔹 LOG: manda o token atual pro arquivo de saída
        self.lexico.imprimeToken(self.tokenLido)

        if tokenAtual == token:
            self.tokenLido = self.lexico.getToken()
        else:
            msgTokenLido = TOKEN.msg(token)
            msgTokenAtual = TOKEN.msg(tokenAtual)
            with open(self.lexico.arqSaida, "a", encoding="utf-8") as f:
                f.write(f"Erro na linha {linha}, coluna {coluna}: ")
                f.write(f"Era esperado {msgTokenAtual} mas foi lido {msgTokenLido}\n")
            raise Exception("Erro Sintático")

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

    def identArg(self): # IdentArg -> ident OpcIdentArg
        self.consome(TOKEN.ident)
        self.opcIdentArg()

    def opcIdentArg(self): # OpcIdentArg ->  [ ] | LAMBDA
        if self.tokenLido[0] == TOKEN.abrecolchete:
            self.consome(TOKEN.abrecolchete)
            self.consome(TOKEN.fechacolchete)
        else:
            # LAMBDA
            pass
    def compoundStmt(self): # CompoundStmt ->  { StmtList }
        self.consome(TOKEN.abreChave)
        self.stmtList()
        self.consome(TOKEN.fechaChave)

    def stmtList(self): # StmtList ->  Stmt StmtList | LAMBDA
        predict_set = (TOKEN.BREAK, TOKEN.CONTINUE,TOKEN.RETURN,TOKEN.pontoVirgula, TOKEN.FOR, TOKEN.IF,TOKEN.WHILE, TOKEN.abreChave,TOKEN.INT, TOKEN.FLOAT, 
                       TOKEN.CHAR, TOKEN.NOT, TOKEN.mais, TOKEN.menos, TOKEN.abrecolchete, TOKEN.valorInt, TOKEN.valorFloat, TOKEN.valorChar, TOKEN.valorString, 
                       TOKEN.ident)
        
        if self.tokenLido[0] in predict_set:
            self.stmt()
            self.stmtList()
        else:
            # LAMBDA
            pass
    def stmt(self): # Stmt -> ForStmt | WhileStmt | IfStmt | CompoundStmt | break ; | continue ; | return Expr ; | Expr ; | Declaration | ;
        if self.tokenLido[0] == TOKEN.FOR:
            self.forStmt()

        elif self.tokenLido[0] == TOKEN.WHILE:
            self.whileStmt()

        elif self.tokenLido[0] == TOKEN.IF:
            self.ifStmt()

        elif self.tokenLido[0] == TOKEN.abreChave:
            self.compoundStmt()

        elif self.tokenLido[0] == TOKEN.BREAK:
            self.consome(TOKEN.BREAK)
            self.consome(TOKEN.pontoVirgula)

        elif self.tokenLido[0] == TOKEN.CONTINUE:
            self.consome(TOKEN.CONTINUE)
            self.consome(TOKEN.pontoVirgula)

        elif self.tokenLido[0] == TOKEN.RETURN:
            self.consome(TOKEN.RETURN)
            self.expr()
            self.consome(TOKEN.pontoVirgula)

        elif self.tokenLido[0] in (TOKEN.INT, TOKEN.FLOAT, TOKEN.CHAR):
            self.declaration()

        elif self.tokenLido[0] in (TOKEN.NOT, TOKEN.mais, TOKEN.menos, TOKEN.abrecolchete, TOKEN.valorInt, TOKEN.valorFloat, TOKEN.valorChar, TOKEN.valorString, TOKEN.ident):
            self.expr()
            self.consome(TOKEN.pontoVirgula)

        elif self.tokenLido[0] == TOKEN.pontoVirgula:
            self.consome(TOKEN.pontoVirgula)

        else:
            msgTokenLido = TOKEN.msg(self.tokenLido[0])
            (token, lexema, linha, coluna) = self.tokenLido
            print(f"Erro na linha {linha}, coluna {coluna}: ")
            if token == TOKEN.erro:
                msg = lexema
            else:
                msg = msgTokenLido
            print(f"Era esperado um início de comando mas foi lido {msg}")
            raise Exception("Erro Sintático")
    
    def forStmt(self): # ForStmt -> for ( Expr ; OptExpr ; OptExpr ) Stmt
        self.consome(TOKEN.FOR)
        self.consome(TOKEN.abreParentese)
        self.expr()
        self.consome(TOKEN.pontoVirgula)
        self.optExpr()
        self.consome(TOKEN.pontoVirgula)
        self.optExpr()
        self.consome(TOKEN.fechaParentese)
        self.stmt()
    
    def optExpr(self): # OptExpr -> Expr | LAMBDA
        if self.tokenLido[0] in (TOKEN.NOT, TOKEN.mais, TOKEN.menos, TOKEN.abrecolchete, TOKEN.valorInt, TOKEN.valorFloat, TOKEN.valorChar, TOKEN.valorString, TOKEN.ident):
            self.expr()
        else:
            # LAMBDA
            pass

    def whileStmt(self): # WhileStmt -> while ( Expr ) Stmt
        self.consome(TOKEN.WHILE)
        self.consome(TOKEN.abreParentese)
        self.expr()
        self.consome(TOKEN.fechaParentese)
        self.stmt()

    def ifStmt(self): # IfStmt -> if ( Expr ) Stmt ElsePart
        self.consome(TOKEN.IF)
        self.consome(TOKEN.abreParentese)
        self.expr()
        self.consome(TOKEN.fechaParentese)
        self.stmt()
        self.elsePart()
    
    def elsePart(self): # ElsePart -> else Stmt | LAMBDA
        if self.tokenLido[0] == TOKEN.ELSE:
            self.consome(TOKEN.ELSE)
            self.stmt()
        else:
            # LAMBDA
            pass
    def declaration(self): # Declaration -> Type IdentList ;
        self.type()
        self.identList()
        self.consome(TOKEN.pontoVirgula)
    
    def type(self): # Type -> int | float | char
        if self.tokenLido[0] in (TOKEN.INT, TOKEN.FLOAT, TOKEN.CHAR):
            self.consome(self.tokenLido[0])
    
    def identList(self): # IdentList -> IdentDeclar RestoIdentList
        self.identDeclar()
        self.restoIdentList()
    
    def restoIdentList(self): # RestoIdentList -> , IdentDeclar RestoIdentList | LAMBDA
        if self.tokenLido[0] == TOKEN.virgula:
            self.consome(TOKEN.virgula)
            self.identDeclar()
            self.restoIdentList()
        else:
            # LAMBDA
            pass
    def identDeclar(self): # IdentDeclar -> ident OpcIdentDeclar
        self.consome(TOKEN.ident)
        self.opcIdentDeclar()
    
    def opcIdentDeclar(self): # OpcIdentDeclar ->  [ valorInt ] | LAMBDA
        if self.tokenLido[0] == TOKEN.abrecolchete:
            self.consome(TOKEN.abrecolchete)
            self.consome(TOKEN.valorInt)
            self.consome(TOKEN.fechacolchete)
        else:
            # LAMBDA
            pass
    
    def expr(self): # Expr -> Log RestoExpr
        self.log()
        self.restoExpr()

    def restoExpr(self): # RestoExpr ->  = Expr RestoExpr | LAMBDA
        if self.tokenLido[0] == TOKEN.atribuicao:
            self.consome(TOKEN.atribuicao)
            self.expr()
            self.restoExpr()
        else:
            # LAMBDA
            pass

    def log(self): # Log -> Nao RestoLog
        self.nao()
        self.restoLog()

    def restoLog(self): # RestoLog -> AND Nao RestoLog | OR Nao RestoLog | LAMBDA
        if self.tokenLido[0] == TOKEN.AND:
            self.consome(TOKEN.AND)
            self.nao()
            self.restoLog()
        elif self.tokenLido[0] == TOKEN.OR:
            self.consome(TOKEN.OR)
            self.nao()
            self.restoLog()
        else:
            # LAMBDA
            pass
    def nao(self): # Nao -> NOT Nao | Rel
        if self.tokenLido[0] == TOKEN.NOT:
            self.consome(TOKEN.NOT)
            self.nao()
        else:
            self.rel()
    
    def rel(self): # Rel ->  Soma RestoRel
        self.soma()
        self.restoRel()

    def restoRel(self): # RestoRel ->  opRel Soma | LAMBDA
        if self.tokenLido[0] in (TOKEN.maior, TOKEN.menor, TOKEN.maiorIgual, TOKEN.menorIgual, TOKEN.igual, TOKEN.diferente):
            self.consome(self.tokenLido[0])
            self.soma()
        else:
            # LAMBDA
            pass
    
    def soma(self): # Soma -> Mult RestoSoma
        self.mult()
        self.restoSoma()
    
    def restoSoma(self): # RestoSoma ->  + Mult RestoSoma | - Mult RestoSoma | LAMBDA
        if self.tokenLido[0] == TOKEN.mais:
            self.consome(TOKEN.mais)
            self.mult()
            self.restoSoma()
        elif self.tokenLido[0] == TOKEN.menos:
            self.consome(TOKEN.menos)
            self.mult()
            self.restoSoma()
        else:
            # LAMBDA
            pass

    def mult(self): # Mult ->  Uno RestoMult
        self.uno()
        self.restoMult()

    def restoMult(self): # RestoMult ->  * Uno RestoMult | / Uno RestoMult | % Uno RestoMult | LAMBDA
        if self.tokenLido[0] == TOKEN.multiplica:
            self.consome(TOKEN.multiplica)
            self.uno()
            self.restoMult()
        elif self.tokenLido[0] == TOKEN.divide:
            self.consome(TOKEN.divide)
            self.uno()
            self.restoMult()
        elif self.tokenLido[0] == TOKEN.modulo:
            self.consome(TOKEN.modulo)
            self.uno()
            self.restoMult()
        else:
            # LAMBDA
            pass
    
    def uno(self): # Uno -> + Uno | - Uno | Folha
        if self.tokenLido[0] == TOKEN.mais:
            self.consome(TOKEN.mais)
            self.uno()
        elif self.tokenLido[0] == TOKEN.menos:
            self.consome(TOKEN.menos)
            self.uno()
        else:
            self.folha()
    
    def folha(self): # Folha -> ( Expr ) | Identifier | valorInt | valorFloat | valorChar | valorString
        
        if self.tokenLido[0] == TOKEN.abreParentese:
            self.consome(TOKEN.abreParentese)
            self.expr()
            self.consome(TOKEN.fechaParentese)
        
        elif self.tokenLido[0] == TOKEN.ident:
            self.identifier()

        elif self.tokenLido[0] == TOKEN.valorInt:
            self.consome(TOKEN.valorInt)

        elif self.tokenLido[0] == TOKEN.valorFloat:
            self.consome(TOKEN.valorFloat)

        elif self.tokenLido[0] == TOKEN.valorChar:
            self.consome(TOKEN.valorChar)

        elif self.tokenLido[0] == TOKEN.valorString:
            self.consome(TOKEN.valorString)

        else:
            msgTokenLido = TOKEN.msg(self.tokenLido[0])
            (token, lexema, linha, coluna) = self.tokenLido
            print(f"Erro na linha {linha}, coluna {coluna}: ")
            if token == TOKEN.erro:
                msg = lexema
            else:
                msg = msgTokenLido
            print(f"Era esperado um valor ou identificador mas foi lido {msg}")
            raise Exception("Erro Sintático")
        
    def identifier(self): # Identifier ->  ident OpcIdentifier
        self.consome(TOKEN.ident)
        self.opcidentifier()

    def opcidentifier(self): # OpcIdentifier ->  [ Expr ] | ( Params ) | LAMBDA
        if self.tokenLido[0] == TOKEN.abrecolchete:
            self.consome(TOKEN.abrecolchete)
            self.expr()
            self.consome(TOKEN.fechacolchete)
        elif self.tokenLido[0] == TOKEN.abreParentese:
            self.consome(TOKEN.abreParentese)
            self.params()
            self.consome(TOKEN.fechaParentese)
        else:
            # LAMBDA
            pass

    def params(self): # Params ->  Expr RestoParams | LAMBDA
        self.expr()
        self.restoParams()

    def restoParams(self): # RestoParams  ->  , Expr RestoParams | LAMBDA
        if self.tokenLido[0] == TOKEN.virgula:
            self.consome(TOKEN.virgula)
            self.expr()
            self.restoParams()
        else:
            # LAMBDA
            pass
