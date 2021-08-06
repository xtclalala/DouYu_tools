# -*- coding: utf-8 -*-
# author:      YYT
# create_time: 2021/8/5  16:39
import socket
import time

from lib.log.log_util import logging


class TCPSocket(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.closed = True

    def send(self, data):
        if self.closed:
            logging.debug("socket is closed")
            return None
        try:
            self.socket.sendall(data)
        except Exception as e:
            self.close()
            logging.warning("Socket sendall failed. Exception: %s" % e)
        return

    def close(self):
        if not self.closed:
            self.socket.close()
            self.closed = True

    def connect(self):
        if self.closed:
            while True:
                try:
                    self.socket.connect((self.host, self.port))
                except Exception as e:
                    logging.warning("Socket connect failed with %s:%d. Exception: %s"
                                    % (self.host, self.port, e))
                    self.socket.close()
                    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    logging.warning("Try reconnect in 5 seconds")

                    time.sleep(5)
                    continue
                else:
                    self.closed = False
                    logging.info("socket is successful")
                    break

    def receive(self, target_size):
        data = b''
        while target_size:
            try:
                tmp = self.socket.recv(target_size)
            except Exception as e:
                self.close()
                logging.warning("Socket recv failed. Exception: %s" % e)
                return None
            if not tmp:
                self.close()
                return None
            target_size -= len(tmp)
            data += tmp
        return data
