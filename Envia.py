import threading
from Dados import Segmento
import time

# ---------------------------------------------------------------------------------------------------------------------------
# Classe EnviarPacote (Thread responsavel por enviar pacotes para o meio de comunicação)
# ---------------------------------------------------------------------------------------------------------------------------


class EnviarPacote (threading.Thread):
    # init method
    def __init__(self, meioComunicacao, semaforo, buffer, id):
        # inicia um objeto segmento com os parametros informados.
        threading.Thread.__init__(self)
        self.meioComunicacao = meioComunicacao
        self.semaforo = semaforo
        self.buffer = buffer
        self.id = id
        self.segmento = "Null"

    # enviaPacote method
    def enviaPacote(self, segmento):
        # envia um pacote para o meio de comunicação
        self.semaforo.acquire()
        self.meioComunicacao.enviaSegmento(segmento)
        self.semaforo.release()

    # removePacote method
    def removePacote(self):
        # remove um pacote do buffer
        self.semaforo.acquire()
        self.buffer.removeSegmentoPorId(self.id)
        self.semaforo.release()

    # buscaPacote method
    def buscaPacote(self):
        # busca o pacote no buffer
        buscando = True
        while buscando == True:
            self.semaforo.acquire()
            pacote = self.buffer.buscaSegmentoPorId(self.id)
            self.semaforo.release()
            if pacote != "Null":
                self.segmento = pacote
                buscando = False

    # run method
    def run(self):
        # Inicia a Thread que envia pacotes para o meio de comunicação.
        self.buscaPacote()
        self.enviaPacote(self.segmento)
        self.removePacote()

# ---------------------------------------------------------------------------------------------------------------------------
# Classe EnviarPacoteRecebeResposta (Thread responsavel por enviar pacotes para o meio de comunicação e esperar uma resposta)
# ---------------------------------------------------------------------------------------------------------------------------


class EnviarPacoteRecebeResposta (threading.Thread):
    # init method
    def __init__(self, meioComunicacao, semaforo, buffer, id):
        # inicia um objeto segmento com os parametros informados.
        threading.Thread.__init__(self)
        self.meioComunicacao = meioComunicacao
        self.semaforo = semaforo
        self.buffer = buffer
        self.id = id
        self.segmento = "Null"

    # aguardaResposta method
    def aguardaResposta(self):
        # Aguarda até que uma resposta referente ao pacote enviado seja enviada para o meio de comunicação
        loop = True
        count = 0
        while loop:
            if count > 25:
                print("Um pacote foi perdido e será reenviado")
                self.enviaPacote(self.segmento)
            segmento = self.buscaPacote()
            count += 1
            if segmento != "Null":
                loop = self.processaResposta(segmento)
            time.sleep(0.5)

    # processaResposta method
    def processaResposta(self, segmento):
        # Verifica a integridade da resposta recebida
        if segmento.enderecoDestino == self.segmento.enderecoOrigem:
            if segmento.corrompido:
                self.removePacote()
                self.enviaPacote(self.segmento)
                return True
            elif segmento.tipo == "SYN":
                return True
            elif segmento.tipo == "DADO":
                return True
            elif segmento.tipo == "FIN":
                return True
            elif segmento.tipo == "nACK":
                self.removePacote()
                aux = Segmento(
                    self.segmento.id, self.segmento.enderecoOrigem, self.segmento.enderecoDestino, self.segmento.tipo, self.segmento.payload, False)
                self.enviaPacote(aux)
                return True
            elif segmento.tipo == "ACK":
                self.removePacote()
                self.removePacoteBuffer()
                return False
            else:
                print("Erro")
                return True
        else:
            return True

    # buscaPacote method
    def buscaPacote(self):
        # tenta buscar um pacote no meio de comunicação
        self.semaforo.acquire()
        segmento = self.meioComunicacao.buscaResposta(self.segmento)
        self.semaforo.release()
        return segmento

    # enviaPacote method
    def enviaPacote(self, segmento):
        # envia um pacote para o meio de comunicação
        self.semaforo.acquire()
        self.meioComunicacao.enviaSegmento(segmento)
        self.semaforo.release()

    # removePacote method
    def removePacote(self):
        # tenta remover um pacote no meio de comunicação
        self.semaforo.acquire()
        self.meioComunicacao.removePacote(self.segmento)
        self.semaforo.release()

    # removePacote method
    def removePacoteBuffer(self):
        # remove um pacote do buffer
        self.semaforo.acquire()
        self.buffer.removeSegmentoPorId(self.id)
        self.semaforo.release()

    # buscaPacote method
    def buscaPacoteBuffer(self):
        # busca o pacote no buffer
        buscando = True
        while buscando == True:
            self.semaforo.acquire()
            pacote = self.buffer.buscaSegmentoPorId(self.id)
            self.semaforo.release()
            if pacote != "Null":
                self.segmento = pacote
                buscando = False

    # run method
    def run(self):
        # Inicia a Thread que envia pacotes para o meio de comunicação e aguarda por uma resposta
        self.buscaPacoteBuffer()
        self.enviaPacote(self.segmento)
        self.aguardaResposta()
