from abc import abstractmethod
import socket
import threading
import random
import string
from google.protobuf.message import DecodeError
from google.protobuf.internal.encoder import _VarintBytes
from google.protobuf.internal.decoder import _DecodeVarint32

import IBKR_MDG_Messages_pb2 as pb


class E2T_MKTDATA():

    @abstractmethod
    def snapshot(self, message):
        pass

    @abstractmethod
    def bid(self, type, symbol, value):
        pass

    @abstractmethod
    def bidQty(self, type, symbol, value):
        pass

    @abstractmethod
    def offer(self, type, symbol, value):
        pass

    @abstractmethod
    def offerQty(self, type, symbol, value):
        pass

    @abstractmethod
    def last(self, type, symbol, value):
        pass

    @abstractmethod
    def lastQty(self, type, symbol, value):
        pass

    @abstractmethod
    def open(self, type, symbol, value):
        pass

    @abstractmethod
    def close(self, type, symbol, value):
        pass

    @abstractmethod
    def high(self, type, symbol, value):
        pass

    @abstractmethod
    def low(self, type, symbol, value):
        pass

    @abstractmethod
    def volume(self, type, symbol, value):
        pass

    def connect(self, HOST, PORT):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((HOST, PORT))
        print(f"Conectado a {HOST}:{PORT}...")

        def handle_client():
            while True:
                try:
                    data = self.client.recv(1024)
                    if not data:
                        break
                    message = pb.Message()
                    # Decode the length prefix
                    size, new_pos = _DecodeVarint32(data, 0)
                    message.ParseFromString(data[new_pos:new_pos + size])
                    if message.messageType == pb.MessageType.SNAPSHOT:
                        print(message)
                    elif message.messageType == pb.MessageType.BID:
                        self.bid(
                            'BID',
                            message.bid.symbol,
                            message.bid.bid
                        )
                    elif message.messageType == pb.MessageType.BIDQTY:
                        self.bidQty(
                            'BIDQTY',
                            message.bidQty.symbol,
                            message.bidQty.bidQty
                        )
                    elif message.messageType == pb.MessageType.OFFER:
                        self.offer(
                            'OFFER',
                            message.offer.symbol,
                            message.offer.offer
                        )
                    elif message.messageType == pb.MessageType.OFFERQTY:
                        self.offerQty(
                            'OFFERQTY',
                            message.offerQty.symbol,
                            message.offerQty.offerQty
                        )
                    elif message.messageType == pb.MessageType.LAST:
                        self.last(
                            'LAST',
                            message.last.symbol,
                            message.last.last
                        )
                    elif message.messageType == pb.MessageType.LASTQTY:
                        self.lastQty(
                            'LASTQTY',
                            message.lastQty.symbol,
                            message.lastQty.lastQty
                        )
                    elif message.messageType == pb.MessageType.OPEN:
                        self.open(
                            'OPEN',
                            message.open.symbol,
                            message.open.open
                        )
                    elif message.messageType == pb.MessageType.CLOSE:
                        self.close(
                            'CLOSE',
                            message.close.symbol,
                            message.close.close
                        )
                    elif message.messageType == pb.MessageType.HIGH:
                        self.high(
                            'HIGH',
                            message.high.symbol,
                            message.high.high
                        )
                    elif message.messageType == pb.MessageType.LOW:
                        self.low(
                            'LOW',
                            message.low.symbol,
                            message.low.low
                        )
                    elif message.messageType == pb.MessageType.VOLUME:
                        self.volume(
                            'VOLUME',
                            message.volume.symbol,
                            message.volume.volume
                        )
                except DecodeError as e:
                    print(f"Error decoding message: {e}")
                    break

        threading.Thread(target=handle_client, daemon=True).start()

    def generate_random_string(length):
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

    def send_mktdata_req(self, symbol, bid, offer, last, open, close, high, low, volume):
        mkt_req = pb.MktDataReq(
            symbol=symbol,
            bid=bid,
            offer=offer,
            last=last,
            open=open,
            close=close,
            high=high,
            low=low,
            volume=volume
        )

        message = pb.Message(
            messageType=pb.MessageType.MTK_DATA_REQ,
            mktDataReq=mkt_req
        )
        buffer = message.SerializeToString()
        self.send_mkt_req(buffer)

    def send_mkt_req(self, mkt_req_buffer):
        if self.client:
            size = len(mkt_req_buffer)
            self.client.sendall(_VarintBytes(size) + mkt_req_buffer)
        else:
            print(f"Error al enviar Market Data Request")
