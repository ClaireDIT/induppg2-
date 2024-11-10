import socket
import threading

#IP och port för servern
HOST = '127.0.0.1' #Anslutning till locast( samma dator)
PORT = 12345 #Portnumret vi kommunicerar via

#Funktion för att hantera mottagande av meddelanden från servern 
def receive_messages(sock):
    #Kör en loop för att hela tiden kolla efter nya meddelanden
    while True:
        try:
            #Tar emot data från servern ( max 512 bytes åt gången)
            data = sock.recv(512)
            if data:
                #Om vi faktiskt får något, skriv ut meddelandet efter attha avkodat det
                print(f"nytt meddelande: {data.decode('utf-8')}")
            else:
                #Om data är tom, bryter vi loopen (förmodligen för att anslutningen är stängd)
                break
        except:
            #Om något går fel, skriver vi ut ett meddelande och lämnar loopen
            print("anslutning till servern tappades.")
            break
#Skapar en socket-anslutning till servern 
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    #Ansluter till servern med den angivna IP:n och porten 
    client_socket.connect((HOST, PORT))
    print('Ansluten till servern') #Bekräftar på att vi är anslutna
     
    # Starter en ny tråd för att lyssna på inkommande meddelanden 
    receive_thread = threading.Thread(target = receive_messages, args=(client_socket,))
    receive_thread.start() #Startar tråden för att hantera inkommande meddelanden 

    # Huvudloopen för att skicka meddelanden
    while True:
        #Ber användaren skriva in ett meddelande 
        message = input ("Skriv ett meddelande: ")
        #Om meddelandet är 'exit' avslutas loopen( så vi kan lämna chatten)
        if message.lower() == 'exit':
            break
        #Skickar det skrivna meddelandet till servern, kodar det som UTf-8
        client_socket.sendall(message.encode('utf-8'))
