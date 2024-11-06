import socket
import threading

HOST = '127.0.0.1'
PORT = 12345


def receive_messages(sock):
    while True:
        try:
            data = sock.recv(512)
            if data:
                print(f"nytt meddelande: {data.decode('utf-8')}")

            else:
                break
        except:
            print("anslutning till servern tappades.")
            break

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((HOST, PORT))
    print('Ansluten till servern')

    receive_thread = threading.Thread(target = receive_messages, args=(client_socket,))
    receive_thread.start()

    while True:
        message = input ("Skriv ett meddelande: ")
        if message.lower() == 'exit':
            break
        client_socket.sendall(message.encode('utf-8'))
