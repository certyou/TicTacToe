import socket
import sys

SERVER_IP = sys.argv[1] if len(sys.argv) > 1 else '127.0.0.1'
PORT = 5555

def start_logger():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        print("Connecting to server:", SERVER_IP, PORT)
        client.connect((SERVER_IP, PORT))
        print("Logger connecté au serveur.")
    except:
        return

    with open("/data/game_log.txt", "a") as f:
        while True:
            msg = client.recv(1024).decode('utf-8')
            if not msg: break
            
            # On log seulement les messages explicites de log ou de fin
            if msg.startswith("LOG:") or "Gagnant" in msg:
                clean_msg = msg.replace("LOG:", "")
                print(f"Enregistrement: {clean_msg.strip()}")
                f.write(clean_msg + "\n")
                f.flush()

if __name__ == "__main__":
    start_logger()