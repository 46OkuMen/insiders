"""
    Decompressor for Insiders '94. Currently works on the file IDS only.
"""


# TODO: These are magic values right now. They must come from somewhere...
MAGIC_BX = 0x2800
MAGIC_DX = 0x4b5a

decompression_start = MAGIC_BX

with open('original/IDS', 'rb') as f:
    enc = f.read()

cursor = 0
with open('patched/IDS.decompressed', 'wb') as f:
    while cursor < decompression_start:
        f.write(enc[cursor].to_bytes(length=1, byteorder='little'))
        cursor += 1
    cursor = decompression_start
    stack = []
    ax = 0
    dx = MAGIC_DX      # TODO Where does it get this value??
    while cursor < len(enc):
        # 5a, 1e becomes 1e5a
        ax = (enc[cursor+1] << 8) + enc[cursor]
        #print(hex(ax))
        stack.append(ax)
        ax = ax ^ dx
        #print(hex(ax))
        dx = stack.pop()
        #print(hex(dx))
        f.write(ax.to_bytes(length=2, byteorder='little'))
        cursor += 2