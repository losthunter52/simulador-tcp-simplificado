import random

# ---------------------------------------------------------------------------------------------------------------------------
# Classe Segmento (Usado para comunicação entre as Threads Cliente e Servidor)
# ---------------------------------------------------------------------------------------------------------------------------


class Segmento:
    # init method
    def __init__(self, id, enderecoOrigem, enderecoDestino, tipo, payload, podeCorromper):
        # inicia um objeto segmento com os parametros informados
        self.id = id
        self.corrompido = False
        self.podeCorromper = podeCorromper
        self.enderecoOrigem = enderecoOrigem
        self.enderecoDestino = enderecoDestino
        self.tipo = tipo
        self.payload = payload

    # lt method
    def __lt__(self, other):
        # serve para que os objetos do tipo Segmento possam ser ordenados por ID
        return self.id < other.id

    # tentaCorromper method
    def tentaCorromper(self):
        # corrompe um pacote caso ele possa ser corrompido.
        rand = bool(random.getrandbits(1))
        if self.podeCorromper and rand == True:
            self.corrompido = True

# ---------------------------------------------------------------------------------------------------------------------------
# Classe Buffer (Usado para armazenar segmentos)
# ---------------------------------------------------------------------------------------------------------------------------


class Buffer:
    # init method
    def __init__(self):
        # inicia um objeto buffer com os parametros informados
        self.pilha = []

    # adicionaSegmento method
    def adicionaSegmento(self, segmento):
        # adiciona um segmento a pilha
        self.pilha.append(segmento)

    # removeSegmentoPorId method
    def removeSegmentoPorId(self, id):
        # tenta remover um segmento da pilha
        for segmento in self.pilha:
            if segmento.id == id:
                self.pilha.remove(segmento)

    # buscaSegmentoPorId method
    def buscaSegmentoPorId(self, id):
        # tenta retornar um segmento da pilha
        segmento = "Null"
        for pacote in self.pilha:
            if pacote.id == id:
                segmento = pacote
        return segmento
