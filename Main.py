from Cliente import Emissor
from Aplicacao import AplicacaoEmissor
from Comunica import MeioComunicacao
from Servidor import Receptor
import threading

# ---------------------------------------------------------------------------------------------------------------------------
# Função Main
# ---------------------------------------------------------------------------------------------------------------------------


def Main():
    # Responsavel por iniciar e encerrar o processo do TCP Simplificado
    meioComunicacao = MeioComunicacao()
    semaforo = threading.Condition()
    receptor = Receptor(meioComunicacao, semaforo)
    receptor.start()
    aplicacao = AplicacaoEmissor()
    ipEmissor = aplicacao.retornaIpAplicacao()
    portaEmissor = aplicacao.definePortaEmissor()
    enderecoDestino = aplicacao.retornaEnderecoDestino()
    emissor = Emissor(meioComunicacao, semaforo, ipEmissor,
                      portaEmissor, enderecoDestino)
    emissor.start()
    rodando = True
    while rodando == True:
        payload = aplicacao.recebeMensagemDoUsuario()
        emissor.requisicao(payload)
        emissor.join()
        executarNovamente = input("Deseja enviar mais uma mensagem? (s) (n): ")
        if executarNovamente == "s":
            rodando = True
        else:
            rodando = False
            receptor.encerrarServidor()
            receptor.join()
    print("Encerrando operações")


if __name__ == '__main__':
    Main()
