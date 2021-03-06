import base64
from queue import Queue
from scapy.all import IP


class Packet(dict):
    src = None
    hostname = b''
    size = 254
    separate = 63
    used = 11
    count = 0
    maxlen = size - used
    id = None

    def __init__(self, data, **kwargs):
        self.hostname = kwargs.get('hostname', self.hostname)
        self.size = kwargs.get('size', self.size)
        self.separate = kwargs.get('separate', self.separate)
        self.used = kwargs.get('used', self.used)
        self.maxlen = self.size - self.used - len(self.hostname)
        if isinstance(data, int):
            self.count = data
            return
        self.src = data
        self.pack()

    def pack(self):
        self.id = IP(self.src).id
        self.count = self.split()

    def unpack(self):
        return self.decode(b''.join([s for s in self.values()]))

    def split(self):
        src = self.encode(self.src)
        seq = 0
        buf = b''
        while len(src):
            sec = src[:self.separate]
            if len(buf) + len(sec) + 1 + self.used > self.maxlen:
                p = self.maxlen - len(buf) - self.used - 1
                buf += src[:p]
                src = src[p:]
                self[seq] = buf
                buf = b''
                seq += 1
            else:
                src = src[self.separate:]
                buf += sec + b'.'
        if len(buf):
            self[seq] = buf[:-1]
            seq += 1
        return seq

    def encode(self, data):
        return base64.urlsafe_b64encode(data).replace(b'=', b'')

    def decode(self, data):
        data = data.replace(b'.', b'')
        padding = b'=' * ((4 - len(data) % 4) % 4)
        return base64.urlsafe_b64decode((data + padding))


class PacketPool(dict):

    def __init__(self):
        dict.__init__(self)
        self.queue = Queue()

    def push(self, data):
        return self.queue.put(data)

    def front(self):
        return self.queue.get()

    def pop(self):
        return self.queue.task_done()

    def empty(self):
        return self.queue.empty()
