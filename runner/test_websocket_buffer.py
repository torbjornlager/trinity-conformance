"""The first WebSocket frame may share a TCP read with the HTTP upgrade."""
import base64
import hashlib
import json
import struct
import unittest
from unittest.mock import patch
from run import WebSocket

class UpgradeSocket:
    def __init__(self, split=False):
        self.chunks=[]
        self.split=split
    def settimeout(self, value): pass
    def sendall(self, request):
        key=next(x.split(': ',1)[1] for x in request.decode().split('\r\n') if x.startswith('Sec-WebSocket-Key:'))
        accept=base64.b64encode(hashlib.sha1((key+'258EAFA5-E914-47DA-95CA-C5AB0DC85B11').encode()).digest()).decode()
        header=f'HTTP/1.1 101 Switching Protocols\r\nSec-WebSocket-Accept: {accept}\r\n\r\n'.encode()
        payload=json.dumps({'type':'ready'}).encode()
        frame=bytes([0x81,len(payload)])+payload
        self.chunks=[header[:17],header[17:]+frame[:3],frame[3:]] if self.split else [header+frame]
    def recv(self,n):
        if not self.chunks:return b''
        data=self.chunks.pop(0)
        if len(data)>n:self.chunks.insert(0,data[n:])
        return data[:n]
    def close(self): pass

class UpgradeBufferTests(unittest.TestCase):
    def test_coalesced_first_frame(self):
        for fragmented in [False, True]:
            with self.subTest(fragmented=fragmented), patch('run.socket.create_connection',return_value=UpgradeSocket(fragmented)):
                ws=WebSocket('ws://127.0.0.1/ws',1)
                self.assertEqual(ws.recv_json(),{'type':'ready'})

if __name__=='__main__':unittest.main()
