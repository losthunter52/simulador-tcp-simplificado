from Dados import Segmento, Buffer
from Envia import EnviarPacoteRecebeResposta
import time
import threading

# ---------------------------------------------------------------------------------------------------------------------------
# Classe Emissor
# ---------------------------------------------------------------------------------------------------------------------------


class Emissor (threading.Thread):
    # init method
    def __init__(self, meioComunicacao, semaforo, ip, portaCliente, enderecoDestino):
        # inicia um objeto segmento com os parametros informados
        threading.Thread.__init__(self)
        self.meioComunicacao = meioComunicacao
        self.semaforo = semaforo
        self.ip = ip
        self.portaCliente = portaCliente
        self.mensagem = ""
        self.enderecoDestino = enderecoDestino
        self.buffer = Buffer()
        self.id = 0
        self.threadList = []

    # retornaEndereco method
    def retornaEndereco(self):
        # retorna o endereço do cliente.
        endereco = (str(self.ip) + ":" + str(self.portaCliente))
        return endereco

    # enviaPacote method
    def enviaPacote(self, segmento):
        # inicia uma thread para enviar um pacote
        self.buffer.adicionaSegmento(segmento)
        thread = EnviarPacoteRecebeResposta(
            self.meioComunicacao, self.semaforo, self.buffer, segmento.id)
        thread.start()
        self.threadList.append(thread)

    # conexao method
    def conexao(self, tipo):
        # inicia ou finaliza uma conexão com o receptor com base no argumento tipo
        self.id += 1
        segmento = Segmento(self.id, self.retornaEndereco(),
                            self.enderecoDestino, tipo, "", True)
        self.buffer.adicionaSegmento(segmento)
        self.semaforo.acquire()
        self.meioComunicacao.enviaSegmento(segmento)
        self.semaforo.release()
        loop = True
        count = 0
        while loop:
            if count > 25:
                count = 0
                self.semaforo.acquire()
                self.meioComunicacao.enviaSegmento(segmento)
                self.semaforo.release()
            count += 1
            self.semaforo.acquire()
            pacote = self.meioComunicacao.buscaResposta(segmento)
            self.semaforo.release()
            if pacote != "Null":
                if pacote.enderecoDestino == self.retornaEndereco():
                    if pacote.tipo == "nACK":
                        self.semaforo.acquire()
                        self.meioComunicacao.removePacote(segmento)
                        self.semaforo.release()
                        self.buffer.removeSegmentoPorId(segmento.id)
                        segmento = Segmento(self.id, self.retornaEndereco(
                        ), self.enderecoDestino, tipo, "", False)
                        self.semaforo.acquire()
                        self.meioComunicacao.enviaSegmento(segmento)
                        self.semaforo.release()
                    elif pacote.tipo == "ACK":
                        self.semaforo.acquire()
                        self.meioComunicacao.removePacote(segmento)
                        self.semaforo.release()
                        self.buffer.removeSegmentoPorId(segmento.id)
                        loop = False
            time.sleep(0.5)
            

    # requisicao method
    def requisicao(self, payload):
        # inicia uma nova requisição ao servidor
        self.mensagem = payload
        print("O Cliente iniciou um requisição")
        self.conexao("SYN")
        payloadList = str(self.mensagem).split()
        for payload in payloadList:
            self.id += 1
            segmento = Segmento(self.id, self.retornaEndereco(
            ), self.enderecoDestino, "DADO", payload, True)
            self.enviaPacote(segmento)
        for thread in self.threadList:
            thread.join()
        self.conexao("FIN")

    # run method
    def run(self):
        # Inicia a thread emissor
        print("Emissor foi iniciado")
