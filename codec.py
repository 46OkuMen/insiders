"""
    Decompressor for Insiders '94.
"""
import sys

# TODO: These are magic values right now. They must come from somewhere...
MAGIC_BX = 0x2800
MAGIC_DX = 0x4b5a

def decode(filename):
    if "IDS" in filename:
        decompression_start = MAGIC_BX
    else:
        decompression_start = 0

    with open(filename, 'rb') as f:
        enc = f.read()

    with open('patched/%s.decompressed' % filename, 'wb') as f:
        cursor = 0
        while cursor < decompression_start:
            """
                push ax
                ax = ax XOR dx
                pop dx
                memory[bx] = ax
                bx += 2
                ax = memory[bx]
                loop
            """
            f.write(enc[cursor].to_bytes(length=1, byteorder='little'))
            cursor += 1
        cursor = decompression_start
        stack = []
        ax = 0
        dx = MAGIC_DX      # TODO Where does it get this value??
        while cursor < len(enc):
            # 5a, 1e becomes 1e5a
            ax = (enc[cursor+1] << 8) + enc[cursor]
            stack.append(ax)
            ax = ax ^ dx
            dx = stack.pop()
            f.write(ax.to_bytes(length=2, byteorder='little'))
            cursor += 2

def encode(filename):
    if filename.endswith('.decompressed'):
        src_filename = filename
        dest_filename = filename.replace('.decompressed', '')
    else:
        src_filename = filename
        dest_filename = filename + '.encoded'

    print(src_filename, dest_filename)


    if "IDS" in filename:
        compression_start = MAGIC_BX
    else:
        compression_start = 0

    with open(src_filename, 'rb') as f:
        decomp = f.read()

    with open(dest_filename, 'wb') as f:
        cursor = 0
        while cursor < compression_start:
            f.write(decomp[cursor].to_bytes(length=1, byteorder='little'))
            cursor += 1

        cursor = compression_start
        ax = 0
        dx = MAGIC_DX

        while cursor < len(decomp):
            ax = (decomp[cursor+1] << 8) + decomp[cursor]
            # Oh hey, this works
            dx = dx ^ ax
            f.write(dx.to_bytes(length=2, byteorder='little'))
            cursor += 2


if __name__ == '__main__':
    HELP_STRING = """usage: python codec.py [encode filename.decompressed] [decode filename]\n"""
    if len(sys.argv) < 3:
        print(HELP_STRING)
        sys.exit(1)

    mode = sys.argv[1]

    filename = sys.argv[2]

    if mode == 'encode':
        encode(filename)
    elif mode == 'decode':
        decode(filename)
    else:
        print(HELP_STRING)