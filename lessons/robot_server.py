import socketserver


class Handler_TCPServer(socketserver.BaseRequestHandler):
    def executer_commande(self,msg):
        msg = msg.decode()
        cmd = msg[:4]
        valeur = msg[5:]
        valeur1 = valeur[:msg.index(" ")]
        valeur2 = valeur[msg.index(" "):]
        print(msg[5:])
        if cmd == "MOVE":
            lmotor,rmotor = [LargeMotor(address) for address in (OUTPUT_A , OUTPUT_D) ]

            lmotor.run_timed(speed_sp = -200, time_sp =850)
            rmotor.run_timed(speed_sp = 200, time_sp =850)
        if cmd == "STOP":
            print("stop")
        # just send back ACK for data arrival confirmation
        self.request.sendall("ACK from TCP Server".encode())
        #A compléter
    def handle(self):
        while 1:
            # self.request - TCP socket connected to the client
            data = self.request.recv(1024)
            if not data:
                break
            data.strip()
            print("{} sent:".format(self.client_address[0]))
            self.executer_commande(data)

if __name__ == "__main__":
    HOST, PORT = "100.75.155.155", 9999

    # Init the TCP server object, bind it to the localhost on 9999 port
    tcp_server = socketserver.TCPServer((HOST, PORT), Handler_TCPServer)

    # Activate the TCP server.
    # To abort the TCP server, press Ctrl-C.
    tcp_server.serve_forever()