import socket
import time
from random import random

ip = ""
porta = 7000
mensagens_recebidas = 0

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((ip, porta))

while True:
	mensagem, endereco = sock.recvfrom(1024)
	mensagens_recebidas += 1
	print("Quantidade de mensagens recebidas: " + str(mensagens_recebidas))

	time.sleep(random())

	sock.sendto(mensagem, (endereco))
