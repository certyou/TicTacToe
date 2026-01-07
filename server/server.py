import socket
import threading

#HOST
HOST = '0.0.0.0'
PORT = 5555

# État du jeu
board = [" " for _ in range(9)]
current_player = "X"
clients = {} # stocke les sockets { "X": sock, "O": sock, "LOG": sock }

def check_winner():
    w = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
    for a,b,c in w:
        if board[a] == board[b] == board[c] and board[a] != " ":
            return board[a]
    if " " not in board: return "DRAW"
    return None

def broadcast(message):
    for role, sock in clients.items():
        try:
            sock.send(message.encode('utf-8'))
        except: pass

def handle_game():
    global current_player
    
    # Message de début
    broadcast("START:Le jeu commence !\n")
    
    while True:
        try:
            # Envoi de l'état du plateau
            board_str = f"BOARD:{','.join(board)}:Tour de {current_player}"
            broadcast(board_str)
            
            # Attente du coup du joueur actuel
            current_sock = clients[current_player]
            current_sock.send("INPUT:Ton tour (0-8): ".encode('utf-8'))
            
            move = current_sock.recv(1024).decode('utf-8').strip()
            
            if not move.isdigit() or int(move) not in range(9) or board[int(move)] != " ":
                current_sock.send("MSG:Coup invalide.\n".encode('utf-8'))
                continue
                
            # Appliquer le coup
            board[int(move)] = current_player
            
            # Log
            if "LOG" in clients:
                clients["LOG"].send(f"LOG:Joueur {current_player} joue en {move}\n".encode('utf-8'))

            # Vérifier victoire
            winner = check_winner()
            if winner:
                board_str = f"BOARD:{','.join(board)}:FIN"
                broadcast(board_str)
                broadcast(f"MSG:Gagnant: {winner}\n" if winner != "DRAW" else "MSG:Match nul\n")
                break
            
            # Changer de joueur
            current_player = "O" if current_player == "X" else "X"
            
        except Exception as e:
            print(f"Erreur: {e}")
            break

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(3)
    print(f"Serveur écoute sur {PORT}...")

    # Connexion séquencée pour simplifier
    conn1, addr1 = server.accept()
    clients["X"] = conn1
    conn1.send("MSG:Tu es Joueur X. Attente des autres...\n".encode('utf-8'))
    print("Joueur X connecté")

    conn2, addr2 = server.accept()
    clients["O"] = conn2
    conn2.send("MSG:Tu es Joueur O. Attente du logger...\n".encode('utf-8'))
    print("Joueur O connecté")

    conn3, addr3 = server.accept()
    clients["LOG"] = conn3
    print("Logger connecté")

    handle_game()

if __name__ == "__main__":
    start_server()