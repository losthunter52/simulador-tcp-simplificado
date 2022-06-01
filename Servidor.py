import threading
from Dados import Segmento, Buffer
from Aplicacao import AplicacaoReceptor
from Envia import EnviarPacote

# ---------------------------------------------------------------------------------------------------------------------------
# Classe Receptor (Thread responsavel por receber pacotes e enviar a mensagem para a aplicação)
# ---------------------------------------------------------------------------------------------------------------------------


class Receptor (threading.Thread):
    # init method
    def __init__(self, meioComunicacao, semaforo):
        # inicia um objeto segmento com os parametros informados.
        threading.Thread.__init__(self)
        self.meioComunicacao = meioComunicacao
        self.semaforo = semaforo
        self.ip = "192.168.0.8"
        self.portaServidor = "666"
        self.mensagem = ""
        self.rodando = True
        self.buffer = Buffer()
        self.enviado = []
        self.recebido = []
        self.threadList = []

    # retornaEndereco method
    def retornaEndereco(self):
        # retorna o endereço do servidor.
        endereco = (str(self.ip) + ":" + str(self.portaServidor))
        return endereco

    # enviarMensagem method
    def enviarMensagem(self):
        # imprime a mensagem armazenada no recebido
        mensagem = ""
        self.recebido.sort()
        for segmento in self.recebido:
            mensagem = (mensagem + " " + str(segmento.payload))
        self.mensagem = mensagem

    # verificaBuffer method
    def verificaBuffer(self):
        # verifica se existe algum pacote nACK e verifica se falta algum pacote na sequencia
        enviarMensagem = True
        self.enviado.sort()
        id = 0
        for segmento in self.enviado:
            id = segmento.id
        for segmento in self.enviado:
            if id > segmento.id:
                id = segmento.id
        for segmento in self.enviado:
            if segmento.id != id:
                enviarMensagem = False
            if segmento.tipo == "nACK":
                enviarMensagem = False
            id += 1
        return enviarMensagem

    # adicionarAoRecebido method
    def adicionarAoRecebido(self, segmento):
        # recebe um pacote, verifica se ele está no recebido e caso esteja deixa apenas o pacote mais recente.
        # caso o contrario ele apenas adiciona o pacote ao recebido.
        for dado in self.recebido:
            if segmento.id == dado.id:
                self.recebido.remove(dado)
        self.recebido.append(segmento)

    # adicionarAoEnviado method
    def adicionarAoEnviado(self, segmento):
        # recebe um pacote, verifica se ele está no enviado e caso esteja deixa apenas o pacote mais recente.
        # caso o contrario ele apenas adiciona o pacote ao enviado.
        for dado in self.enviado:
            if segmento.id == dado.id:
                self.enviado.remove(dado)
        self.enviado.append(segmento)

    # verificaSePodeCorromper method
    def verificaSePodeCorromper(self, segmento):
        # define se um pacote pode ou não ser corrompido
        podeCorromper = True
        for pacote in self.enviado:
            if segmento.id == pacote.id:
                podeCorromper = False
        return podeCorromper

    # encerrarServidor method
    def encerrarServidor(self):
        # encerra o loop do while do metodo Run do servidor
        self.rodando = False

    # processarSegmento method
    def processarSegmento(self, segmento):
        # metodo responsavel por criar os pacotes de resposta e inserir os mesmos no buffers para futura conferencia
        podeCorromper = self.verificaSePodeCorromper(segmento)
        if segmento.corrompido == True:
            segmento = Segmento(segmento.id, self.retornaEndereco(
            ), segmento.enderecoOrigem, "nACK", "", podeCorromper)
            self.adicionarAoEnviado(segmento)
            return segmento
        elif segmento.tipo == "SYN":
            self.enviado = []
            self.recebido = []
            self.adicionarAoRecebido(segmento)
            segmento = Segmento(segmento.id, self.retornaEndereco(
            ), segmento.enderecoOrigem, "ACK", "", podeCorromper)
            self.adicionarAoEnviado(segmento)
            return segmento
        elif segmento.tipo == "DADO":
            self.adicionarAoRecebido(segmento)
            segmento = Segmento(segmento.id, self.retornaEndereco(
            ), segmento.enderecoOrigem, "ACK", "", False)
            self.adicionarAoEnviado(segmento)
            return segmento
        elif segmento.tipo == "FIN":
            self.adicionarAoRecebido(segmento)
            segmento = Segmento(segmento.id, self.retornaEndereco(
            ), segmento.enderecoOrigem, "ACK", "", podeCorromper)
            self.adicionarAoEnviado(segmento)
            if self.verificaBuffer() == True:
                self.enviarMensagem()
            else:
                print("Erro, um ou mais pacotes foram perdidos")
            return segmento

    # enviaPacote method
    def enviaPacote(self, segmento):
        # inicia uma thread para enviar um pacote
        self.buffer.adicionaSegmento(segmento)
        thread = EnviarPacote(
            self.meioComunicacao, self.semaforo, self.buffer, segmento.id)
        thread.start()
        self.threadList.append(thread)

    # run method
    def run(self):
        # metodo que inicia a Thread Servidor
        print("O Servidor foi Iniciado")
        aplicacao = AplicacaoReceptor()
        while self.rodando:
            self.semaforo.acquire()
            segmento = self.meioComunicacao.buscaPacote(self.retornaEndereco())
            self.semaforo.release()
            if segmento != "Null":
                self.semaforo.acquire()
                self.meioComunicacao.removePacote(segmento)
                self.semaforo.release()
                resposta = self.processarSegmento(segmento)
                self.enviaPacote(resposta)
                if segmento.tipo == "FIN" and segmento.corrompido == False:
                    for thread in self.threadList:
                        thread.join()
                    aplicacao.enviaMensagem(self.mensagem)
