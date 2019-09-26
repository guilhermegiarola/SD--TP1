import socket
import time
import datetime
import os

class Cliente:
    ip = "192.168.103.20"
    portaTCP = 7004
    portaUDP = 7000
    timeout = 0.7 #Segundos
    qnt_pacotes = 10
    qnt_pacotes_retornados = 0
    qnt_pacotes_perdidos = 0
    somatorio_rtt = 0
    somatorio_vazao = 0

    def __init__(self):
        print("Caso queira sair do sistema, digite x.")
        print("Se quiser testar a vazão, digite 1, caso queira testar o ping e perda de pacotes, digite 2: ")
        op = input()

        while op!='x':
            if op == '1':
                self.envio_tcp()
            elif op == '2':
                self.pacotes_udp()
            else:
                print("Opção inválida. Escolha outra opção.")

            print("Caso queira sair do sistema, digite x.")
            print("Se quiser testar a vazão, digite 1, caso queira testar o ping e perda de pacotes, digite 2: ")
            op = input()

    def envio_tcp(self):
        self.sockTCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sockTCP.connect((self.ip, self.portaTCP))

        input("Digite \"enter\" para testar a vazão.")
        pathTo = 'sentArchive.txt'
        arq = open(pathTo, 'rb')
        l = arq.read(1024)

        initial_time = time.time()

        while(l):
            self.sockTCP.send(l)
            l = arq.read(1024)

        final_time = time.time()
        elapsed_time = final_time - initial_time

        print("\nA vazão obtida foi de: " +
         str(round(os.path.getsize(pathTo)*8/(elapsed_time*1024*1024),2))
         + " Mbps\n")

        arq.close()

    def pacotes_udp(self):
        self.sockUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sockUDP.settimeout(self.timeout)
        input("Digite \"enter\" para pingar.")

        self.qnt_pacotes_retornados = 0
        self.qnt_pacotes_perdidos = 0
        self.lista_rtts = []

        for id in range(self.qnt_pacotes):

            tempo_inicial = time.time()
            self.sockUDP.sendto(str(id).encode(), (self.ip, self.portaUDP))
            try:
                id_incorrespondente = True
                while id_incorrespondente:
                    mensagem, endereco = self.sockUDP.recvfrom(1024)
                    id_recebido = int(mensagem.decode())
                    if id_recebido == id:
                        tempo_final = time.time()
                        intervalo_de_tempo = tempo_final - tempo_inicial
                        self.lista_rtts.append(intervalo_de_tempo)
                        # O valor eh mostrado em milisegundos
                        print("Pacote", str(id + 1), "retornou em",\
                        round(intervalo_de_tempo * 1000, 2), "ms.")
                        self.qnt_pacotes_retornados += 1
                        id_incorrespondente = False

            except socket.timeout:
                print("Pacote", str(id + 1), "perdido!")
                self.qnt_pacotes_perdidos += 1

        self.gerar_relatorio()
        self.sockUDP.close()

    def calcular_rtt_medio(self):
        if self.qnt_pacotes_retornados != 0:
            somatorio_rtts = 0
            for tempo in self.lista_rtts:
                somatorio_rtts += tempo
            rtt_medio = somatorio_rtts / self.qnt_pacotes_retornados
        else:
            rtt_medio = 0
        # O valor eh mostrado em milisegundos
        print("RTT medio:", round(rtt_medio * 1000, 2), "ms")
        return rtt_medio

    def calcular_taxa_perda(self):
        proporcao_perda = self.qnt_pacotes_perdidos / self.qnt_pacotes
        percentual_perda = proporcao_perda * 100
        percentual_perda = round(percentual_perda, 2)
        print("Taxa de perda:", percentual_perda, "%")

    def gerar_relatorio(self):
        print("---------------------------------------------------------------")
        rtt_medio = self.calcular_rtt_medio()
        self.calcular_taxa_perda()
        print()

Cliente()
