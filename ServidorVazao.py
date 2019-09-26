from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread


HOST = ''              # Endereco IP do Servidor
PORT = 7004            # Porta que o Servidor esta

tcp = socket(AF_INET, SOCK_STREAM)
orig = (HOST, PORT)
tcp.bind(orig)

def acceptIncomingConnections():
    while True:
        connection, cliente = tcp.accept()
        Thread(target=handleClient, args=(connection,)).start()

def handleClient(con):
        while True:
            arq = open('receivedArchive.tar.gz','wb')
            msg = con.recv(1024)
            arq.write(msg)
            if not msg: break
        con.close()
        arq.close()

if __name__ == "__main__":
    tcp.listen()

    accept_thread = Thread(target=acceptIncomingConnections)
    accept_thread.start()
    accept_thread.join()

    server.close()
