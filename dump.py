"""
    Generic dumper of Shift-JIS text into an excel spreadsheet.
    Meant for quick estimations of how much text is in a game.
"""

import sys
import os
import xlsxwriter
from rominfo import FILE_BLOCKS, FILES, UNCOMPRESSED_FILES
from romtools.disk import Gamefile, Block

COMPILER_MESSAGES = [b'Turbo', b'Borland', b'C++', b'Library', b'Copyright']

ASCII_MODE = 2
# 0 = none
# 1: punctuation and c format strings only (not implemented)
# 2: All ascii

THRESHOLD = 4

"""
def find_blocks(file):
"""
       # WIP. Finds blocks of normal strings separated with 00s.
"""
    THRESHOLD = 10

    with open(file, 'rb') as f:
        gf = Gamefile(file)
        contents = f.read()

        cursor = 0
        blocks = []

        sjis_buffer = b''

        block_start = 0

        while cursor < len(contents):
            if 0x80 <= contents[cursor] <= 0x9f or 0xe0 <= contents[cursor] <= 0xef:
                #print(bytes(contents[cursor]))
                sjis_buffer += contents[cursor].to_bytes(1, byteorder='little')
                cursor += 1
                sjis_buffer += contents[cursor].to_bytes(1, byteorder='little')

            # ASCII text
            # TODO: But don't count continuous UUUUUUUUUUU
            elif 0x20 <=contents[cursor] <= 0x7e and ASCII_MODE in (1, 2):
                sjis_buffer += contents[cursor].to_bytes(1, byteorder='little')

            # 00s are okay, since we're looking for blocks
            elif contents[cursor] == 0x00:
                sjis_buffer += contents[cursor].to_bytes(1, byteorder='little')

            else:
                if len(sjis_buffer) > THRESHOLD:
                    blocks.append(Block(gf, (block_start, cursor+1)))
                sjis_buffer = b''
                block_start = cursor+1
            cursor += 1

        if sjis_buffer:
            blocks.append(Block(gf, (block_start, cursor+1)))

        for b in blocks:
            print(b)
"""



def dump(files):
    for filename in files:
        #clean_filename = filename.replace('.decompressed', '')

        worksheet = workbook.add_worksheet(filename)
        worksheet.write(0, 0, 'Offset', header)
        worksheet.write(0, 1, 'Japanese', header)
        worksheet.write(0, 2, 'JP_len', header)
        worksheet.write(0, 3, 'English', header)
        worksheet.write(0, 4, 'EN_len', header)
        worksheet.write(0, 5, 'Comments', header)

        worksheet.set_column('A:A', 8)
        worksheet.set_column('B:B', 60)
        worksheet.set_column('C:C', 5)
        worksheet.set_column('D:D', 60)
        worksheet.set_column('E:E', 5)
        worksheet.set_column('F:F', 60)

        row = 1
        blocks = FILE_BLOCKS[filename]

        if filename not in UNCOMPRESSED_FILES:
            src_filepath = 'original/decompressed/%s.decompressed' % filename
        else:
            src_filepath = 'original/%s' % filename

        with open(os.path.join(src_filepath), 'rb') as f:
            contents = f.read()

            cursor = 0
            sjis_buffer = b""
            sjis_buffer_start = 0
            sjis_strings = []

            for c in COMPILER_MESSAGES:
                print(c)
                if c in contents:
                    #print(contents)
                    cursor = contents.index(c)
                    sjis_buffer_start = contents.index(c)
                    break

            for (start, stop) in blocks:
                cursor = start
                sjis_buffer_start = cursor

                while cursor <= stop:
                    # First byte of SJIS text. Read the next one, too
                    if 0x80 <= contents[cursor] <= 0x9f or 0xe0 <= contents[cursor] <= 0xef:
                        #print(bytes(contents[cursor]))
                        sjis_buffer += contents[cursor].to_bytes(1, byteorder='little')
                        cursor += 1
                        sjis_buffer += contents[cursor].to_bytes(1, byteorder='little')

                    # Halfwidth katakana
                    elif 0xa1 <= contents[cursor] <= 0xdf:
                        sjis_buffer += contents[cursor].to_bytes(1, byteorder='little')

                    # ASCII text
                    elif 0x20 <=contents[cursor] <= 0x7e and ASCII_MODE in (1, 2):
                        sjis_buffer += contents[cursor].to_bytes(1, byteorder='little')

                    # C string formatting with %
                    #elif contents[cursor] == 0x25:
                    #    #sjis_buffer += b'%'
                    #    cursor += 1
                    #    if contents[cursor]

                    # End of continuous SJIS string, so add the buffer to the strings and reset buffer
                    else:
                        sjis_strings.append((sjis_buffer_start, sjis_buffer))
                        sjis_buffer = b""
                        sjis_buffer_start = cursor+1
                    cursor += 1
                    #print(sjis_buffer)

                # Catch anything left after exiting the loop
                if sjis_buffer:
                    sjis_strings.append((sjis_buffer_start, sjis_buffer))
                    sjis_buffer = b''


            if len(sjis_strings) == 0:
                continue

            for s in sjis_strings:
                # Remove leading U's
                while s[1].startswith(b'U'):
                    s = (s[0] + 1, s[1][1:])
                    #s[1] = s[1][1:]
                    #s[0] += 1

                s = (s[0], s[1].rstrip(b'U'))

                if len(s[1]) < THRESHOLD:
                    continue

                loc = '0x' + hex(s[0]).lstrip('0x').zfill(5)
                try:
                    jp = s[1].decode('shift-jis')
                except UnicodeDecodeError:
                    print("Couldn't decode that")
                    continue

                if len(jp.strip()) == 0:
                    continue
                print(loc, jp)

                worksheet.write(row, 0, loc)
                worksheet.write(row, 1, jp)
                row += 1

    workbook.close()

if __name__ == '__main__':
    #if len(sys.argv) < 2:
    #    print("Usage: python dumper.py folderwithgamefilesinit")
    #    sys.exit(1)
    #'patched' = sys.argv[1]
    workbook = xlsxwriter.Workbook("insiders" + '_dump.xlsx')
    header = workbook.add_format({'bold': True, 'align': 'center', 'bottom': True, 'bg_color': 'gray'})
    #FILES = [f for f in os.listdir('patched') if os.path.isfile(os.path.join('patched', f))]
    #FILES = ['IDS.decompressed', 'IS2.decompressed']
    print(FILES)
    dump(FILES)

    #find_blocks('patched/IDS.decompressed')
