class cd(object):
    """
    Coordinate difference
    """
    def __init__(self, dx, dy, dz):
        self.dx = dx
        self.dy = dy
        self.dz = dz
    def mlen(self):
        return sum([abs(self.dx), abs(self.dy), abs(self.dz)])
    def clen(self):
        return max(abs(self.dx), abs(self.dy), abs(self.dz))

class nd(cd):
    """
    Near coordinate difference
    """
    def __init__(self, dx, dy, dz):
        super().__init__(dx, dy, dz)
        assert 0 < self.mlen() <= 2 and self.clen() == 1
    def encode(self):
        return (self.dx + 1) * 9 + (self.dy + 1) * 3 + (self.dz + 1)

class ld(cd):
    """
    Linear coordinate difference
    """
    def __init__(self, dx, dy, dz):
        super().__init__(dx, dy, dz)
        assert sum([dx != 0, dy != 0, dz != 0]) == 1
    def encode_a(self):
        if self.dx != 0: return 1
        if self.dy != 0: return 2
        return 3
    def encode_i(self):
        if self.dx != 0: return self.dx + self.offset
        if self.dy != 0: return self.dy + self.offset
        return self.dz + self.offset

class sld(ld):
    """
    Short linear coordinate difference
    """
    offset = 5
    def __init__(self, dx, dy, dz):
        super().__init__(dx, dy, dz)
        assert self.mlen() <= self.offset

class lld(ld):
    """
    Long linear coordinate difference
    """
    offset = 15
    def __init__(self, dx, dy, dz):
        super().__init__(dx, dy, dz)
        assert self.mlen() <= self.offset

class command(object):
    """
    Nanobot command
    """
    @staticmethod
    def encode_all(cmds):
        out = bytearray()
        for cmd in cmds: cmd.encode(out)
        return out

class Halt(command):
    def encode(self, out):
        out.append(0b11111111)

class Wait(command):
    def encode(self, out):
        out.append(0b11111110)

class Flip(command):
    def encode(self, out):
        out.append(0b11111101)

class SMove(command):
    def __init__(self, lld):
        super().__init__()
        self.lld = lld
    def encode(self, out):
        out.append(self.lld.encode_a() << 4 | 0b0100)
        out.append(self.lld.encode_i())

class LMove(command):
    def __init__(self, sld1, sld2):
        super().__init__()
        self.sld1 = sld1
        self.sld2 = sld2
    def encode(self, out):
        out.append(self.sld2.encode_a() << 6 | self.sld1.encode_a() << 4
                                             | 0b1100)
        out.append(self.sld2.encode_i() << 4 | self.sld1.encode_i())

class FusionP(command):
    def __init__(self, nd):
        super().__init__()
        self.nd = nd
    def encode(self, out):
        out.append(self.nd.encode() << 3 | 0b111)

class FusionS(command):
    def __init__(self, nd):
        super().__init__()
        self.nd = nd
    def encode(self, out):
        out.append(self.nd.encode() << 3 | 0b110)

class Fission(command):
    def __init__(self, nd, m):
        super().__init__()
        self.nd = nd
        self.m = m
    def encode(self, out):
        out.append(self.nd.encode() << 3 | 0b101)
        out.append(self.m)

class Fill(command):
    def __init__(self, nd):
        super().__init__()
        self.nd = nd
    def encode(self, out):
        out.append(self.nd.encode() << 3 | 0b011)

if __name__ == "__main__":
    cmds = [
        Halt(),
        Wait(),
        Flip(),
        SMove(lld(12,0,0)), SMove(lld(0,0,-4)),
        LMove(sld(3,0,0), sld(0,-5,0)), LMove(sld(0,-2,0), sld(0,0,2)),
        FusionP(nd(-1,1,0)),
        FusionS(nd(1,-1,0)),
        Fission(nd(0,0,1), 5),
        Fill(nd(0,-1,0)),
    ]
    with open("example.nbt", "wb") as f:
        f.write(command.encode_all(cmds))
