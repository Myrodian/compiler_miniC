from lexico import Lexico
from sintatico import Sintatico

class Tradutor:

    def __init__(self, nomeArq):
        self.nomeArq = nomeArq

    def inicializa(self):
        self.sintatico = Sintatico(self.nomeArq)

    def traduz(self):
        self.sintatico.traduz()

# inicia a traducao
if __name__ == '__main__':
    try:
        x = Tradutor('teste.txt')
        x.inicializa()
        x.traduz()
    except Exception as e:
        print(e)