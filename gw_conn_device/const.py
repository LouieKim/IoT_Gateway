# coding=utf-8
# python 3.6

CONVERT_HIGHCODE = ['f', 'e', 'd', 'c', 'b', 'a', '9', '8', '7', '6', '5', '4', '3', '2', '1', '0']
CONVERT_LOWCODE = ['c', 'd', 'e', 'f', '8', '9', 'a', 'b', '4', '5', '6', '7', '0', '1', '2', '3']

SAMIN747_START_PACKET = "55aaaaaa0103060000"
SAMIN747_TARGETPOWER_START = 18
SAMIN747_TARGETPOWER_END = 22
SAMIN747_PREDICTPOWER_START = 1102
SAMIN747_PREDICTPOWER_END = 1106
SAMIN747_CURRENTPOWER_START = 1118
SAMIN747_CURRENTPOWER_END = 1122

SAMIN747_SEND_DEVICE_MODEL = b"\xaa\xaa\xaa\x02\x01\xff\x00\x00"

SAMIN747_SPLIT_INDEX01 = 22
SAMIN747_SPLIT_INDEX02 = 1036

SAMIN747_RETRY_COUNT = 3

CONTROL_SUCCESS_CODE = 0
CONTROL_FAIL_CODE = 1
CONTROL_FAIL_UNKNOW_CODE = 2

REQUIRED_PYTHON_VER = (3, 6, 0)