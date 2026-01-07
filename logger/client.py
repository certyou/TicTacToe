import socket
import sys

# Récupérer l'IP du serveur via argument ou env
SERVER_IP = sys.argv[1] if len(sys.argv) > 1 else '127.0.0.1'
PORT = 6666
print(SERVER_IP, PORT)

def print_board(board_data):
    b = board_data.split(',')
    print(f"\n {b[0]} | {b[1]} | {b[2]} ")
    print("---+---+---")
    print(f" {b[3]} | {b[4]} | {b[5]} ")
    print("---+---+---")
    print(f" {b[6]} | {b[7]} | {b[8]} \n")

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        print("Connecting to server:", SERVER_IP, PORT)
        client.connect((SERVER_IP, PORT))
    except Exception as e:
        print(f"Impossible de se connecter au serveur: {e}")
        return

    while True:
        try:
            msg = client.recv(1024).decode('utf-8')
            if not msg: break
            
            # Protocole simple basé sur des préfixes
            if msg.startswith("BOARD:"):
                parts = msg.split(":")
                print_board(parts[1])
                print(parts[2]) # Info status
            elif msg.startswith("INPUT:"):
                move = input(msg.split(":", 1)[1])
                client.send(move.encode('utf-8'))
            elif msg.startswith("MSG:") or msg.startswith("START:"):
                print(msg.split(":", 1)[1])
                
        except KeyboardInterrupt:
            break
    client.close()

if __name__ == "__main__":
    start_client()