import socket
import time
import datetime
import os

class Cliente:
    ip = "127.0.0.1"
    portaTCP = 7000
    portaUDP = 7002
    timeout = 0.1 #Segundos
    qnt_pacotes = 10

    def __init__(self):
        self.sockUDP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sockUDP.connect((self.ip, self.portaUDP))
        self.sockTCP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sockTCP.settimeout(self.timeout)
        
        print("Caso queira sair do sistema, digite x.")
        print("Se quiser testar a vazão, digite 1, caso queira testar o ping e perda de pacotes, digite 2: ")
        op = input()
        
        while op!='x':
            if op == '1':
                self.envio_udp()
            elif op == '2':
                self.pacotes_tcp()
            else:
                print("Opção inválida. Escolha outra opção.")
            
            print("Caso queira sair do sistema, digite x.")
            print("Se quiser testar a vazão, digite 1, caso queira testar o ping e perda de pacotes, digite 2: ")
            op = input()

    def envio_udp(self):
        input("Digite \"enter\" para testar a vazão.")
        path = 'sentArchive.txt'
        arq = open(path, 'rb')
        l = arq.read(1024)

        initial_time = time.time()

        while(l):
            self.sockUDP.send(l)
            l = arq.read(1024)

        final_time = time.time()
        elapsed_time = final_time - initial_time

        print("\nA vazão obtida foi de: " +
         str(round(os.path.getsize(path)/(elapsed_time*1024*1024),2))
         + " Mbps\n")

        arq.close()

    def pacotes_tcp(self):
        input("Digite \"enter\" para pingar.")
        self.qnt_pacotes_retornados = 0
        self.qnt_pacotes_perdidos = 0
        self.somatorio_rtt = 0
        self.somatorio_vazao = 0

        for i in range(self.qnt_pacotes):
            tempo_inicial = time.time()
            self.sockTCP.sendto(bytearray("Testando ping", "UTF-8"), (self.ip, self.portaTCP))

            try:
                self.sockTCP.recvfrom(1024)
                print("Pacote " + str(i + 1) + " retornado!")
                self.qnt_pacotes_retornados += 1

                tempo_final = time.time()
                intervalo_de_tempo = tempo_final - tempo_inicial
                #O intervalo de tempo passa a ser em microsegundos
                intervalo_de_tempo = intervalo_de_tempo/1000
                print("RTT: " + str(int(intervalo_de_tempo)) + " microsegundos.\n")

                self.contabilizar_rtt(intervalo_de_tempo)
                self.contabilizar_vazao(intervalo_de_tempo)
            except socket.timeout:
                print("Pacote " + str(i + 1) + " perdido!\n")
                self.qnt_pacotes_perdidos += 1

        self.gerar_relatorio()

    def contabilizar_rtt(self, intervalo_de_tempo):
        self.somatorio_rtt += intervalo_de_tempo

    def contabilizar_vazao(self, intervalo_de_tempo):
        #Conversao de microsegundos para segundos
        intervalo_de_tempo = intervalo_de_tempo/1000000
        #Calculo da vazao
        vazao = 1024/intervalo_de_tempo
        #Conversao de B/s para MB/s
        vazao = vazao/1048576
        #Contabiliza a vazao
        self.somatorio_vazao += vazao

    def gerar_relatorio(self):
        #Verificacao necessaria para evitar divisao por zero
        if self.qnt_pacotes_retornados != 0:
            rtt_medio = self.somatorio_rtt / self.qnt_pacotes_retornados
            print("RTT medio: " + str(int(rtt_medio)) + " microsegundos.")
            vazao_media = self.somatorio_vazao / self.qnt_pacotes_retornados
            print("Vazao: " + str(round(vazao_media, 2)) + " MB/s.")
        else:
            print("Nenhum pacote voltou!")
        proporcao_perda = self.qnt_pacotes_perdidos / self.qnt_pacotes
        percentual_perda = round(proporcao_perda * 100, 2)
        print("Taxa de perda: " + str(percentual_perda) + "%\n")

Cliente()
