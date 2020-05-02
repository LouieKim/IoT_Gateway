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
        targetPower = int(recvData[SAMIN747_TARGETPOWER_START:SAMIN747_TARGETPOWER_END], 16)
        predictPower = int(recvData[SAMIN747_PREDICTPOWER_START:SAMIN747_PREDICTPOWER_END], 16)
        currentPower = int(recvData[SAMIN747_CURRENTPOWER_START:SAMIN747_CURRENTPOWER_END], 16)
        
        result = {'targetPower' : targetPower, 'predictPower' : predictPower, 'currentPower' : currentPower}

    except Exception as e :
        _LOGGER.debug(e)
        return None
    
    return result

def assemble_data(targetPower):
    tempRecvData = oSocketNetwork.socket_receive()
    strRecvData = tempRecvData[SAMIN747_SPLIT_INDEX01:SAMIN747_SPLIT_INDEX02]
    hex01TargetPower, hex02TargetPower = dec2hexPeakvalue(targetPower)
    strRecvData = hex01TargetPower + hex02TargetPower + strRecvData
    
    #Edit control data, remove some bytes and insert others bytes
    strControlData = strRecvData[:-22] + "3c00" + strRecvData[-18:-10] + "0f" + strRecvData[-8:]
    binaryPostfix = text2binary(strControlData)

    lrc = 0
    for i in binaryPostfix:
        lrc ^= i
    calc = format(lrc, '02x')

    secureCode1 = CONVERT_HIGHCODE[int(calc[0], 16)]
    secureCode2 = CONVERT_LOWCODE[int(calc[1], 16)]
    binarySecureCode = text2binary(secureCode1 + secureCode2)
    result = SAMIN747_SEND_DEVICE_MODEL + binaryPostfix + binarySecureCode
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