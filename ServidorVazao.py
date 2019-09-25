from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread


HOST = ''              # Endereco IP do Servidor
PORT = 7003            # Porta que o Servidor esta

tcp = socket(AF_INET, SOCK_STREAM)
orig = (HOST, PORT)
tcp.bind(orig)

def acceptIncomingConnections():
    while True:
        connection, cliente = tcp.accept()
        Thread(target=handleClient, args=(connection,)).start()

def handleClient(con):
        while True:
            msg = con.recv(1024)
            if not msg: break
        con.close()

if __name__ == "__main__":
    tcp.listen()

    accept_thread = Thread(target=acceptIncomingConnections)
    accept_thread.start()
    accept_thread.join()

    server.close()