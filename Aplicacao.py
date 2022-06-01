import numpy

# ---------------------------------------------------------------------------------------------------------------------------
# Classe AplicaçãoEmissor
# ---------------------------------------------------------------------------------------------------------------------------


class AplicacaoEmissor:
    # init method
    def __init__(self):
        # inicia um objeto aplicação emissor
        self.payload = ""
        self.enderecoDestino = "192.168.0.8:666"
        self.ip = "192.168.237.37"

    # retornaEnderecoDestino method
    def retornaEnderecoDestino(self):
        # retorna o endereco do receptor
        return self.enderecoDestino

    # recebeMensagemDoUsuario method
    def recebeMensagemDoUsuario(self):
        # recebe uma mensagem por input e envia ela para a aplicação destino
        payload = input('Insira uma mensagem: ')
        payload = str(payload)
        self.payload = payload
        return self.payload

    # retornaIpAplicacao method
    def retornaIpAplicacao(self):
        # retorna o ip da aplicação receptor
        return self.ip

    # definePortaEmissor method
    def definePortaEmissor(self):
        # retorna a porta da aplicação receptor
        porta = numpy.random.randint(1024, 49151)
        porta = str(porta)
        return porta

# ---------------------------------------------------------------------------------------------------------------------------
# Classe AplicaçãoReceptor
# ---------------------------------------------------------------------------------------------------------------------------


class AplicacaoReceptor:

    # init method
    def __init__(self):
        # inicia um objeto aplicação receptor
        self.mensagens = []

    # enviaMensagem method
    def enviaMensagem(self, mensagem):
        # adiciona a mensagem recebida a lista de mensagens da aplicação receptor e
        # imprime a mensagem recebida no terminal
        self.mensagens.append(mensagem)
        print("A Aplicação-Receptor recebeu uma mensagem : '" + str(mensagem) + " '")
