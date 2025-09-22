from ttoken import TOKEN

class Lexico:
    def __init__(self, arqFonte):
        self.arqFonte = arqFonte
        with open(self.arqFonte, 'r', encoding='utf-8') as f:
            self.fonte = f.read()
        self.tamFonte = len(self.fonte)
        self.indiceFonte = 0
        self.tokenLido = None
        self.linha = 1
        self.coluna = 0


    def fimDoArquivo(self):
        return self.indiceFonte >= self.tamFonte
    
    def getchar(self):
        if self.fimDoArquivo():
            return '\0'
        car = self.fonte[self.indiceFonte]
        self.indiceFonte += 1
        if car == '\n':
            self.linha += 1
            self.coluna = 0
        else:
            self.coluna += 1
        return car

    def ungetchar(self, simbolo):
        if simbolo == '\n':
            self.linha -= 1
        if self.indiceFonte > 0:
            self.indiceFonte -=1
        self.coluna -= 1

    def imprimeToken(self, tokenCorrente):
        (token, lexema, linha, coluna) = tokenCorrente
        msg = TOKEN.msg(token)
        if len(msg) > 7:
            if len(lexema) >= 8:
                print(f'(token = {msg}\t lex = "{lexema}" \t lin = {linha} col = {coluna})')
            else:
                print(f'(token = {msg}\t lex = "{lexema}" \t\t lin = {linha} col = {coluna})')
        else:
            if len(lexema) >= 8:
                print(f'(token = {msg}\t\t lex = "{lexema}" \t lin = {linha} col = {coluna})')
            else:
                print(f'(token = {msg}\t\t lex = "{lexema}" \t\t lin = {linha} col = {coluna})')


    def getToken(self):
        estado = 1
        simbolo = self.getchar()
        lexema = ''
        
        lin = self.linha
        col = self.coluna
        while True:
            if estado == 1:
                if simbolo.isalpha():
                    estado = 2 #idents, pal.reservadas
                
                elif simbolo.isdigit():
                    estado = 3 #numeros
                
                elif simbolo == '/':  # pode ser divisão ou comentário
                    estado = 4
                
                elif simbolo == '=': # verificar se é comparação ou atribuição
                    estado = 5

                elif simbolo == '<':
                    estado = 6

                elif simbolo == '>':
                    estado = 7

                elif simbolo == '\'':
                    estado = 8
                
                elif simbolo == '\"':
                    estado = 9

                elif simbolo == '!':
                    estado = 10

                elif simbolo == '&':
                    estado = 11

                elif simbolo == '|':
                    estado = 12

                elif simbolo == '+':
                    return (TOKEN.mais, simbolo, lin, col)
                
                elif simbolo == '%':
                    return (TOKEN.modulo, simbolo, lin, col)
                
                elif simbolo == '-':
                    return (TOKEN.menos, simbolo, lin, col)
                
                elif simbolo == '*':
                    return (TOKEN.multiplica, simbolo, lin, col)
                
                elif simbolo == '(':
                    return(TOKEN.abrePar, simbolo, lin, col)
                
                elif simbolo == ')':
                    return(TOKEN.fechaPar, simbolo, lin, col)
                
                elif simbolo == '{':
                    return(TOKEN.abreChave, simbolo, lin, col)
                
                elif simbolo == '}':
                    return(TOKEN.fechaChave, simbolo, lin, col)
                
                elif simbolo == '[':
                    return(TOKEN.abrecolchete, simbolo, lin, col)
                
                elif simbolo == ']':
                    return(TOKEN.fechacolchete, simbolo, lin, col)

                elif simbolo == ',':
                    return (TOKEN.virg, simbolo, lin, col)

                elif simbolo == ';':
                    return (TOKEN.ptoVirg, simbolo, lin, col)
                
                elif simbolo == '.':
                    return (TOKEN.pto, simbolo, lin, col)

                elif simbolo == '\0':
                    return (TOKEN.eof, '', self.linha, self.coluna)
                
                elif simbolo in [' ', '\t', '\n', '\r']:
                    # ignora brancos e quebras de linha
                    lexema = ''
                    estado = 1
                else:
                    # qualquer outro caractere não reconhecido é erro
                    estado = 0

            elif estado == 2:
                if simbolo.isalnum() or simbolo == '_':
                    estado = 2
                else:
                    self.ungetchar(simbolo)
                    token = TOKEN.reservada(lexema)
                    return (token, lexema, lin, col)
            
            elif estado == 3:
                if simbolo.isdigit():
                    estado = 3
                
                elif simbolo == '.':
                    estado = 31  # ponto visto, mas ainda não confirmou parte decimal

                elif simbolo.isalpha():
                    estado = 0  # erro: número não pode conter letras
                
                else:
                    self.ungetchar(simbolo)
                    return (TOKEN.valorInt, lexema, lin, col)

            elif estado == 31:  # depois de ver um ponto, precisa de pelo menos um dígito
                if simbolo.isdigit():
                    estado = 32  # agora sim, entrou na parte decimal
                else:
                    estado = 0  # erro: não tinha dígito depois do ponto

            elif estado == 32:  # já leu pelo menos um dígito da parte decimal
                if simbolo.isdigit():
                    estado = 32  # continua lendo parte decimal
                
                elif simbolo == '.' or simbolo.isalpha():
                    estado = 0  # erro: dois pontos ou letra dentro do número
                
                else:
                    self.ungetchar(simbolo)
                    return (TOKEN.valorFloat, lexema, lin, col)
            elif estado == 4:
                if simbolo == '/':  # é comentário
                    # descarta até fim da linha
                    while simbolo != '\n' and simbolo != '\0':
                        simbolo = self.getchar()
                    return self.getToken()  # continua analisando depois do comentário
                else:
                    self.ungetchar(simbolo)  # não era comentário, devolve o caractere
                    return (TOKEN.divide, lexema, lin, col)
                
            elif estado == 5:
                if simbolo == '=':
                    lexema += simbolo
                    return (TOKEN.igual, lexema, lin, col)
                else:
                    self.ungetchar(simbolo) # não era igualdade, devolve o caractere
                    return (TOKEN.atrib, lexema, lin, col)
            
            elif estado == 6:
                if simbolo == '=':
                    lexema += simbolo 
                    return (TOKEN.menorIgual, lexema, lin, col)
                else:
                    self.ungetchar(simbolo) # não era menorIgual, devolve o caractere
                    return (TOKEN.menor, lexema, lin, col)
            
            elif estado == 7:
                if simbolo == '=':
                    lexema += simbolo 
                    return (TOKEN.maiorIgual, lexema, lin, col)
                else:
                    self.ungetchar(simbolo) # não era maiorIgual, devolve o caractere
                    return (TOKEN.maior, lexema, lin, col)
            
            elif estado == 8:  # dentro de um literal de char
                if simbolo != '\'' and simbolo not in ['\n', '\r']:  
                    lexema += simbolo
                    simbolo = self.getchar()
                    if simbolo == '\'':  # fecha corretamente
                        lexema += simbolo
                        return (TOKEN.valorChar, lexema, lin, col)
                    else:
                        estado = 0  # erro: não fechou com aspa
                else:
                    estado = 0  # erro: char vazio ou quebra de linha
            elif estado == 9:
                
                if simbolo == ';' or simbolo == '\0':
                    estado = 0 # erro, string não pode terminar assim

                if simbolo == '\"':
                    lexema += simbolo
                    return (TOKEN.valorString, lexema, lin, col)
                
            
            elif estado == 10:
                if simbolo == '=':
                    lexema += simbolo 
                    return (TOKEN.diferente, lexema, lin, col)
                else:
                    self.ungetchar(simbolo)
                    return(TOKEN.NOT, lexema, lin, col) 
            
            elif estado == 11:
                if simbolo == '&':
                    lexema += simbolo 
                    return (TOKEN.AND, lexema, lin, col)
                else:
                    self.ungetchar(simbolo)
                    return (TOKEN.erro, lexema, lin, col)
            
            elif estado == 12:
                if simbolo == '|':
                    lexema += simbolo 
                    return (TOKEN.OR, lexema, lin, col)
                else:
                    self.ungetchar(simbolo)
                    return (TOKEN.erro, lexema, lin, col)
                
            elif estado == 0:
                if simbolo == '.' or simbolo.isalpha() or simbolo.isdigit() or simbolo == '\'':
                    estado = 0
                else:
                    self.ungetchar(simbolo)
                    return (TOKEN.erro, lexema, lin, col)
                
            if simbolo not in ['\n', '\r']:
                if estado == 9:  # string
                    lexema += simbolo
                else:  # fora da string
                    if simbolo not in [' ', '\t']:
                        lexema += simbolo
            simbolo = self.getchar()

if __name__ == '__main__':
    lexico = Lexico("teste.txt")
    token = lexico.getToken()
    while(token[0] != TOKEN.eof):
        lexico.imprimeToken(token)
        token = lexico.getToken()
    lexico.imprimeToken(token)