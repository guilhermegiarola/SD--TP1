import socket

ip = ''
porta = 7002

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((ip, porta))
sock.listen(1)

conn, addr = sock.accept()
arq = open('receivedArchive.tar.gz', 'wb')

while True:
    dados = conn.recv(1024)
    arq.write(dados)

arq.close()
