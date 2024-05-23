import socket
import threading
import random
import string
from google.protobuf.message import DecodeError
from google.protobuf.internal.encoder import _VarintBytes
from google.protobuf.internal.decoder import _DecodeVarint32
from abc import abstractmethod

from oms import IBKR_OMS_Messages_pb2 as pb


class E2T_OMS:

    @abstractmethod
    def status(self, requestId, orderId, live, cumQty, leavesQty, avgPx, lastPx):
        pass

    @abstractmethod
    def reject(self, idRef, reason):
        pass

    @abstractmethod
    def trade(self, orderId, execId, time, lastQty, lastPx, avgPx, cumQty):
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
                    size, new_pos = _DecodeVarint32(data, 0)
                    message.ParseFromString(data[new_pos:new_pos + size])

                    if message.messageType == pb.MessageType.ORDER_STATUS:
                        self.status(
                            message.orderStatus.requestId,
                            message.orderStatus.orderId,
                            message.orderStatus.live,
                            message.orderStatus.cumQty,
                            message.orderStatus.leavesQty,
                            message.orderStatus.avgPx,
                            message.orderStatus.lastPx
                        )
                    elif message.messageType == pb.MessageType.TRADE_ORDER:
                        self.trade(
                            message.tradeOrder.orderId,
                            message.tradeOrder.execId,
                            message.tradeOrder.time,
                            message.tradeOrder.lastQty,
                            message.tradeOrder.lastPx,
                            message.tradeOrder.avgPx,
                            message.tradeOrder.cumQty
                        )
                    elif message.messageType == pb.MessageType.REJECT:
                        self.reject(
                            message.reject.idRef,
                            message.reject.reason
                        )
                    else:
                        print(f"Unknown message type: {message.messageType}")
                except DecodeError as e:
                    print(f"Error decoding message: {e}")
                    break

        threading.Thread(target=handle_client, daemon=True).start()

    def send_order(self, order_buffer):
        if self.client:
            size = len(order_buffer)
            self.client.sendall(_VarintBytes(size) + order_buffer)
        else:
            print("Error: Cliente no disponible para el usuario")

    def send_limit_order(self, side, symbol, quantity, price):
        limit_order = pb.LimitOrder(
            requestId=''.join(random.choice(string.ascii_letters + string.digits) for _ in range(5)),
            side=side,
            symbol=symbol,
            quantity=quantity,
            price=price
        )
        message = pb.Message(
            messageType=pb.MessageType.LIMIT_ORDER,
            limitOrder=limit_order
        )
        buffer = message.SerializeToString()
        self.send_order(buffer)

    def send_limit_replace(self, order_id, quantity, price):
        limit_replace = pb.LimitReplace(
            requestId=''.join(random.choice(string.ascii_letters + string.digits) for _ in range(5)),
            orderId=int(order_id),
            quantity=quantity,
            price=price
        )
        message = pb.Message(
            messageType=pb.MessageType.LIMIT_REPLACE,
            limitReplace=limit_replace
        )
        buffer = message.SerializeToString()
        self.send_order(buffer)

    def send_limit_cancel(self, order_id):
        limit_cancel = pb.LimitCancel(
            requestId=''.join(random.choice(string.ascii_letters + string.digits) for _ in range(5)),
            orderId=int(order_id)

        )
        message = pb.Message(
            messageType=pb.MessageType.LIMIT_CANCEL,
            limitCancel=limit_cancel
        )
        buffer = message.SerializeToString()
        self.send_order(buffer)
