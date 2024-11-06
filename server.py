import socket
import threading


HOST = '127.0.0.1'
PORT = 12345

clients=[]


def handle_client(conn, addr):
    print(F'Anslutning etablera med {addr}')
    clients.append(conn)

    while True:
        try:
            data= conn.recv(512)
            if not data:
                break
            message = data.decode ('utf-8')
            print(F'Meddelande från {addr}: {message}')

            
        except:
            break

    conn.close()

    clients.remove(conn)
    print(f'Anslutning stängd: {addr}')

def broadcast(message, sender_conn):
    for client in clients:
        if client != sender_conn: 
            try: 
                client.sendall(message.encode('utf-8'))
            except:
                pass


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f'server is listening on socket address {HOST}:{PORT}')

    while True:
        conn, addr = server_socket.accept()
        thread = threading.Thread(target = handle_client, args=(conn, addr))
        thread.start()

