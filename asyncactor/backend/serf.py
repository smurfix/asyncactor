
#
# Listener on top of an AsyncSerf connection
#
from asyncactor.abc import Transport, MonitorStream
from asyncserf import Serf
import msgpack

class SerfTransport(Transport):
    def __init__(self, conn: Serf, usertag: str):
        self.conn = conn
        self.tag = usertag

    def monitor(self):
        return SerfMonitor(self)

    async def send(self, payload):
        payload = msgpack.packb(payload, use_bin_type=True)
        await self.conn.event(name=self.tag, payload=payload, coalesce=False)

class SerfMonitor(MonitorStream):
    async def __aenter__(self):
        self._mon1 = self.transport.conn.stream("user:"+self.transport.tag)
        self._mon2 = await self._mon1.__aenter__()
        return self

    def __aexit__(self, *tb):
        return self._mon1.__aexit__(*tb)

    def __aiter__(self):
        self._it = self._mon2.__aiter__()
        return self

    async def __anext__(self):
        msg = await self._it.__anext__()
        msg = msgpack.unpackb(msg.payload, raw=False, use_list=False)
        return msg

Transport = SerfTransport