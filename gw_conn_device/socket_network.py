# coding=utf-8
# python 3.6

from loader import load_yaml
import logging
import socket
import time
import binascii
import const
from config import DEVICE_CONFIG


_LOGGER = logging.getLogger(__name__)

class cSocketNetwork:
    def __init__(self):
        self.clientSocket = None
        self.host = DEVICE_CONFIG['ip']
        self.port = DEVICE_CONFIG['port']

    def _socket_connect(self):
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientSocket.settimeout(60)
        self.clientSocket.connect((self.host, self.port))

    def _socket_close(self):
        self.clientSocket.close()        

    def socket_receive(self):
        strHeadRecvData = ""
        startFlag = False

        self._socket_connect()
        #Todo dangerous limit loop
        while True:
            recvData = self.clientSocket.recv(1024) # b'U\xaa\xaa\xaa\x01
            hexRecvData = binascii.b2a_hex(recvData) # binary ascii hex b'aaaaaa01
            strHexRecvData = hexRecvData.decode("utf-8") #binary to str

            if (startFlag == False) & (0 == strHexRecvData.find(const.SAMIN747_START_PACKET)):
                startFlag = True
            
            if startFlag == True:
                strHeadRecvData += strHexRecvData

            if len(strHeadRecvData) >= 1684:
                break

        self._socket_close()
        return strHeadRecvData

    def socket_sendMsg(self, msg):
        self._socket_connect()
        self.clientSocket.sendall(msg)
        self._socket_close()

    """
    try:
        pass
    except Exception as e:
        #raise("eccException") #Todo
        print(e)
    """
    """
    def socket_receive(self):
        self._socket_connect()
        time.sleep(1)
        recvData = self.clientSocket.recv(1024)
        self._socket_close()
        return recvData 
    """