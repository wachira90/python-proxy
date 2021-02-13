import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def tcp_server(self):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.setblocking(0)
        sock.bind((self.local_addr, int(self.local_port)))
        sock.listen(3)
        self.lsock.append(sock)
        print('[*] Listening on {0} {1}'  .format(self.local_addr,self.local_port))
        while True:
            readable, writable, exceptional = select.select(self.lsock, [], [])
            for s in readable:
                if s == sock:
                    rserver =self.remote_conn()
                    if rserver:
                        client, addr = sock.accept()
                        print('Accepted connection {0} {1}'.format(addr[0], addr[1]))
                        self.store_sock(client, addr, rserver)
                        break
                    else:
                        print('the connection with the remote server can\'t be \
                        established')
                        print('Connection with {} is closed'.format(addr[0]))
                        client.close()
                data = self.received_from(s, 3)
                self.msg_queue[s].send(data)
                if len(data) == 0:
                    self.close_sock(s)
                    break
                else:
                    print('Received {} bytes from client '.format(len(data)))
                    self.hexdump(data)
    except KeyboardInterrupt:
        print ('Ending server')        
    except:
        print('Failed to listen on {}:{}'.format(self.local_addr, self.local_port))
        sys.exit(0)      
    finally:
        sys.exit(0)

def remote_conn(self):
    try:
        remote_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote_sock.connect((self.remote_addr, int(self.remote_port)))
        return remote_sock
    except Exception as e:
        print(e)
        return False


def store_sock(self, client, addr, rserver):
    self.lsock.append(client)
    self.lsock.append(rserver)
    self.msg_queue[client] =  rserver
    self.msg_queue[rserver] =  client

def received_from(self, sock, timeout):
        data = ""
        sock.settimeout(timeout)
        try:
            while True:
                data = sock.recv(4096)
                if not data:
                    break
                data =+ data
        except:
            pass
        return data




