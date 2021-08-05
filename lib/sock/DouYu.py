# -*- coding: utf-8 -*-
# author:      YYT
# create_time: 2021/8/5  15:53

import socket

from lib.log.log_util import logging
from .payload import PayloadMSG
from lib.config.config_util import ConfigUtil
from .TCP_socket import TCPSocket
# 接入检查数据


class DouYu(object):

    def __init__(self):
        self.payload_msg = PayloadMSG()
        self.config = ConfigUtil()
        self.client = None

    def socket_client(self):
        try:
            self.client = TCPSocket(self.config.host, self.config.port)
        except Exception as e:
            logging.error("socket is bad")



    def send_msg(self, msg_str):
        head, msg_bytes = self.payload_msg.msg(msg_str)
        self.client.send(head)
        self.client.send(msg_bytes)

    def get_msg(self):
        self.send_msg()


