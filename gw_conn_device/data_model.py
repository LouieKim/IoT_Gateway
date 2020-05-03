import socket_network
import binascii
import logging
from const import(
    SAMIN747_TARGETPOWER_START,
    SAMIN747_TARGETPOWER_END,
    SAMIN747_PREDICTPOWER_START,
    SAMIN747_PREDICTPOWER_END,
    SAMIN747_CURRENTPOWER_START,
    SAMIN747_CURRENTPOWER_END,
    CONVERT_HIGHCODE,
    CONVERT_LOWCODE,
    SAMIN747_SEND_DEVICE_MODEL,
    SAMIN747_SPLIT_INDEX01,
    SAMIN747_SPLIT_INDEX02
)

oSocketNetwork = socket_network.cSocketNetwork()
_LOGGER = logging.getLogger(__name__)

def receiveMsg():
    try:
        result = {}
        recvData = oSocketNetwork.socket_receive()
        
        result = {'targetPower' : targetPower, 'predictPower' : predictPower, 'currentPower' : currentPower}

    except Exception as e :
        _LOGGER.debug(e)
        return None
    
    return result

def assemble_data(targetPower):
    #Data
    return result

def sendMsg(msg):
    oSocketNetwork.socket_sendMsg(msg)

## dec2hexPeakvalue(self, peakvalue)
# 목표값 10진수의 값을 16진수로 바꿔주는 메소드
def dec2hexPeakvalue(peakvalue):
    p_value = format(peakvalue, '04x')
    rule1 = p_value[0:2]
    rule2 = p_value[2:]
    return rule1, rule2

## text2binary(self, data)
# 문자열을 바이너리 형식으로 변환하는 메소드
def text2binary(data):
    return bytes.fromhex(data)