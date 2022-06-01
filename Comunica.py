# ---------------------------------------------------------------------------------------------------------------------------
# Classe MeioComunicacao (Usado para conectar as Threads Cliente e Servidor)
# ---------------------------------------------------------------------------------------------------------------------------

class MeioComunicacao:
    # init method
    def __init__(self):
        # inicia pilhas vazias
        self.pilha = []

    # enviaSegmento method
    def enviaSegmento(self, segmento):
        # adiciona um segmento a pilha
        for pacote in self.pilha:
            if pacote == segmento:
                self.pilha.remove(pacote)
                print("Um pacote foi perdido e reenviado")
        segmento.tentaCorromper()
        self.pilha.append(segmento)
        print("[" + str(segmento.enderecoOrigem) + "] esta enviando um segmento[" + str(segmento.id) +
              "] " + str(segmento.tipo) + " para [" + str(segmento.enderecoDestino) + "]")

    # buscaPacote method
    def buscaPacote(self, endereco):
        # tenta retornar um pacote para determinado destinatario que está esperando uma requisicao
        aux = "Null"
        for pacote in self.pilha:
            if pacote.enderecoDestino == endereco:
                aux = pacote
        return aux

    # buscaResposta method
    def buscaResposta(self, segmento):
        # tenta retornar um pacote para determinado destinatario que está esperando uma resposta
        aux = "Null"
        for pacote in self.pilha:
            if pacote.id == segmento.id:
                aux = pacote
        return aux

    # removePacote method
    def removePacote(self, segmento):
        # remove os pacotes da pilha
        for pacote in self.pilha:
            if pacote.id == segmento.id:
                self.pilha.remove(pacote)
