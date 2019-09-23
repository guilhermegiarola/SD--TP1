import socket

HOST = ''              # Endereco IP do Servidor
PORT = 7002            # Porta que o Servidor esta

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
orig = (HOST, PORT)

tcp.bind(orig)
tcp.listen(1)

while True:
    con, cliente = tcp.accept()
    while True:
        msg = con.recv(1024)
        if not msg: break
    con.close()
