#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Simple Socket Server for Python

This is a simple socker server for python mostly for testing purposes. 
It can connect only to a single client, and delivers a simple message back.

Example:
    Start the server with either:

        $ python pysocket.py

    or 

        $ ./pysocket.py


    And connect to it with, for example, netcat.

        $ nc localhost 8000

Attributes:
    host (str): This is the host for the socket server. Usually `0.0.0.0`
    port (int): This is the port for the socket server. Default value is
        8000, per SimpleHTTPServer convention.
        
"""
import socket, select

class SimpleSocketServer:
    """ A basic python socker socket server. It handles one client. """

    def __init__(self, host = '0.0.0.0', port = 8000):
        """ Initialize the socket server 
        
        Args:
            host (str): This is the host for the socket server. Usually `0.0.0.0`
            port (int): This is the port for the socket server. Default value is
                8000, per SimpleHTTPServer convention.

        """
        self.host = host
        self.port = port
        self._build_socket()

    def _build_socket(self):
        """ Build the server socket """
        self._socket_create()
        self._socket_bind()
        self.sock.listen(1)
        
    def _socket_create(self):
        """ Create the socket """
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        except socket.error as error_message:
            print("Socket creation failed. \n\tError Code : {}\n\tMessage : {}".format(error_message[0], error_message[1]))

    def _socket_bind(self):
        """ Bind the socket """
        try:
            self.sock.bind((self.host, self.port))
        except socket.error as error_message:
            print("Socket creation failed. \n\tError Code : {}\n\tMessage : {}".format(error_message[0], error_message[1]))

    def close(self):
        """ Shut down the server socket. """
        print("Shutting down socket server at {}:{}".format(self.host, self.port))
        if self.sock:
            self.sock.close()
            self.sock = None

    def start(self):
        """ Accept a single incoming connection and respond. """
        print("Starting socket server at {}:{}".format(self.host, self.port))
        
        while True:
            client_sock, client_addr = self.sock.accept()
            print("Client {} connected".format(client_addr))
            connected = True
            while connected:
                if client_sock:
                    try:
                        read_op, _, _ = select.select([client_sock,], [], [])
                    except select.error:
                        print("Error reading from socket at {}".format(client_addr))
                        return 1

                    if len(read_op):
                        read_data = client_sock.recv(255)
                        if not len(read_data):
                            print('{} closed the socket.'.format(client_addr))
                            connected = False
                        else:
                            print('> {}'.format(read_data.rstrip()))
                            if read_data.rstrip() == b'close':
                                print('Closing socket connection to {}'.format(client_addr))
                                connected = False
                                client_sock.close()
                            elif  read_data.rstrip() == b'quit':
                                print('Closing socket connection to {}'.format(client_addr))
                                connected = False
                                client_sock.close()
                                return 0
                            else:
                                client_sock.send(read_data)

def main():
    server = SimpleSocketServer()
    server.start()
    print("Existing socket server.")

if __name__ == "__main__":
    main()
