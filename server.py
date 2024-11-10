import socket
import threading

#sätter serverns IP-adress och portnummer
HOST = '127.0.0.1' # localhost, alltså kör servern på din egen dator
PORT = 12345 # En sluppmässig port som inte redan används

#lista för att hålla koll på alla anslutna klienter
clients=[]

#funktion som hanterar en enskild klientanslutning
def handle_client(conn, addr):
    print(F'Anslutning etablera med {addr}')# skriver ut vem som har anslutit 
    clients.append(conn) # Lägger till klienten i listan över anslutna klienter

    while True:
        try:
            # Väntar på att få data(meddelande) från klienten
            data= conn.recv(512)# tar emot upp til 512 bytes åt gången
            if not data:
                break # Om ingen data kommer in, stänger vi anslutningen

            #Dekodar meddelandet från kliente(från bytes till text)
            message = data.decode ('utf-8')
            print(F'Meddelande från {addr}: {message}')#Skriver ut meddelande på servern

            broadcast(message, sender_conn=conn) #Skickar meddelandet vidare till alla andra anslutna klienter

            
        except:
            #Om det uppstår något fel, avslutar vi loop
            break

    # När klienten kopplar bort, tar vi bort den från klientlitan och stänger anslutningen.
    conn.close()
    clients.remove(conn)
    print(f'Anslutning stängd: {addr}')
# funktion för att skicka ett meddelade till alla anslutna klienter(utom den som skickade det)
def broadcast(message, sender_conn):
    for client in clients:
        if client != sender_conn: # skickaer inte tillbaka meddelander till avsändaren
            try: 
                client.sendall(message.encode('utf-8')) #Skickar meddelandet till klienten
            except:
                pass# om något är fel, ignorera det

#skapar en server-socket och startar lyssnadet 
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))#Kopplar servern till IP och port
    server_socket.listen() #Börjar lyssna på inkommande anslutningar
    print(f'server is listening on socket address {HOST}:{PORT}')

#Loopar för alltid och accepterar nya anslutningar 
    while True:
        conn, addr = server_socket.accept() #Accepterar en ny anslutning
        thread = threading.Thread(target = handle_client, args=(conn, addr)) #Startar en tråd för att hantera klienten 
        thread.start()# Startar tråden

