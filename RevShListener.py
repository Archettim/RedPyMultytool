import socket, sys, time

def listener(ip=socket.gethostbyname(socket.gethostname()),port=4242):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((ip, port))
    s.listen(1)
    print("Listening on port " + str(port))
    conn, addr = s.accept()
    print('Connection received from ',addr)
    while True:
        ans = conn.recv(1024).decode()
        sys.stdout.write(ans)
        command = input()
        command += "\n"
        conn.send(command.encode())
        time.sleep(0.2)
        sys.stdout.write("\033[A" + ans.split("\n")[-1])

if __name__=="__main__":
    listener()