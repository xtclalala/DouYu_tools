# -*- coding: utf-8 -*-
# author:      YYT
# create_time: 2021/8/5  15:53
import queue
import time

from threading import Thread
from lib.log.log_util import logging
from .payload import PayloadMSG
from .TCP_socket import TCPSocket


# 接入检查数据


class DouYu(object):

    def __init__(self, room_id,
                 heartbeat_interval,
                 barrage_host,
                 barrage_port):
        self.room_id = room_id
        self.heartbeat_interval = heartbeat_interval
        self.barrage_host = barrage_host
        self.barrage_port = barrage_port
        self.tcp_socket = TCPSocket(self.barrage_host, self.barrage_port)
        self.message_worker = MessageWorker(self.tcp_socket, self.room_id)
        self.heartbeat_worker = HeartbeatWorker(self.tcp_socket, self.heartbeat_interval)

    def add_handler(self, msg_type, handler):
        self.message_worker.add_handler(msg_type, handler)

    def set_heartbeat_interval(self, heartbeat_interval):
        self.heartbeat_interval = heartbeat_interval

    def refresh_object(self):
        self.tcp_socket = TCPSocket(self.barrage_host, self.barrage_port)
        self.message_worker = MessageWorker(self.tcp_socket, self.room_id)
        self.heartbeat_worker = HeartbeatWorker(self.tcp_socket, self.heartbeat_interval)

    def set_room_id(self, room_id):
        self.room_id = room_id

    def start(self):
        self.tcp_socket.connect()
        self.message_worker.start()
        self.heartbeat_worker.start()

    def stop(self):
        self.message_worker.set_stop()
        self.heartbeat_worker.set_stop()
        self.tcp_socket.close()
        self.refresh_object()


class HeartbeatWorker(Thread):
    def __init__(self, sock, heartbeat_interval=45):
        Thread.__init__(self)
        self.need_stop = False
        self.socket = sock
        self.heartbeat_interval = heartbeat_interval

    def set_stop(self, need_stop=True):
        self.need_stop = need_stop

    def run(self):
        while not self.need_stop:
            data = PayloadMSG.assemble_heartbeat_str()
            self.socket.send(data)
            time.sleep(self.heartbeat_interval)


class MessageConsumer(Thread):
    def __init__(self, msg_queue):
        Thread.__init__(self)
        self.need_stop = False
        self.msg_queue = msg_queue
        self.handlers = {}

    def add_handler(self, msg_type, handler):
        if msg_type not in self.handlers:
            self.handlers[msg_type] = []
        self.handlers[msg_type].append(handler)

    def set_stop(self, need_stop=True):
        self.need_stop = need_stop

    def run(self):
        while not self.need_stop:
            data = self.msg_queue.get()
            ori_str = PayloadMSG.extract_str_from_data(data)
            msg = PayloadMSG.parse_str_to_dict(ori_str)
            try:
                msg_type = msg['type']
                if msg_type in self.handlers:
                    for handler in self.handlers[msg_type]:
                        handler(msg, msg_type)
            except Exception as e:
                logging.warning("Invalid msg received. Exception: %s"
                                % e)
            self.msg_queue.task_done()


class MessageWorker(Thread):
    def __init__(self, sock, room_id):
        Thread.__init__(self)
        self.need_stop = False
        self.socket = sock
        self.room_id = room_id
        self.msg_queue = queue.Queue()
        self.message_consumer = MessageConsumer(self.msg_queue)

    def add_handler(self, msg_type, handler):
        self.message_consumer.add_handler(msg_type, handler)

    def set_stop(self, need_stop=True):
        self.need_stop = need_stop
        self.message_consumer.set_stop(need_stop)

    def prepare(self):
        self.message_consumer.start()
        self.enter_room()

    def enter_room(self):
        data = PayloadMSG.assemble_login_str(self.room_id)
        self.socket.send(data)
        logging.info("login is successful")
        data = PayloadMSG.assemble_join_group_str(self.room_id)
        self.socket.send(data)
        logging.info("group is successful")

    def run(self):
        self.prepare()
        while not self.need_stop:
            packet_size = self.socket.receive(4)
            if packet_size is None:
                logging.warning("Socket closed")
                self.socket.connect()
                self.enter_room()
                continue
            packet_size = int.from_bytes(packet_size, byteorder='little')
            data = self.socket.receive(packet_size)
            if data is None:
                logging.warning("Socket closed")
                self.socket.connect()
                self.enter_room()
                continue
            self.msg_queue.put(data)
