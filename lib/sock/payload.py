# -*- coding: utf-8 -*-
# author:      YYT
# create_time: 2021/8/5  16:07
import time

from lib.items.singleton import Singleton

client_msg_type = 689
reserved_data_field = 0


def wai(func, *args, **kwargs):
    def assemble_transfer_data():
        ori_str = func(*args, **kwargs)
        data_size = len(ori_str)
        packet_size = 4 * 2 + data_size + 1
        data = packet_size.to_bytes(4, byteorder='little')
        data += packet_size.to_bytes(4, byteorder='little')
        data += client_msg_type.to_bytes(2, byteorder='little')
        data += reserved_data_field.to_bytes(2, byteorder='little')
        data += ori_str.encode()
        data += b'\0'
        return data

    return assemble_transfer_data

class PayloadMSG(metaclass=Singleton):

    # @staticmethod
    # def msg(msg_str):
    #     msg_bytes = msg_str.encode()
    #     msg_length = len(msg_bytes) + 8
    #     msg_code = 689
    #     msg_head = int.to_bytes(msg_length, 4, "little") \
    #                + int.to_bytes(msg_length, 4, "little") \
    #                + int.to_bytes(msg_code, 4, "litter")
    #     return msg_head, msg_bytes

    @staticmethod
    @wai
    def assemble_login_str(room_id):
        res = "type@=loginreq/roomid@=" + str(room_id) + "/"
        return res

    @staticmethod
    @wai
    def assemble_join_group_str(room_id):
        res = "type@=joingroup/rid@=" + str(room_id) + "/gid@=-9999/"
        return res


    @wai
    def assemble_heartbeat_str(self):
        res = "type@=keeplive/tick@=%s/" % int(time.time()) + "/"
        return res



    @staticmethod
    def extract_str_from_data(data):
        packet_size = int.from_bytes(data[0:4], byteorder='little')
        if packet_size != len(data):
            return ""
        return data[8:].decode("utf8", "ignore")

    @staticmethod
    def parse_str_to_dict(ori_str):
        res = {}
        ori_strs = ori_str.split("/")
        for ori_str in ori_strs:
            kv = ori_str.split("@=")
            if len(kv) == 2:
                res[kv[0]] = kv[1]
        return res
