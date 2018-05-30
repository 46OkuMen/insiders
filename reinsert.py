"""
    Insiders '94 reinserter.
    Based on the CRW reinserter.
"""

import os

from rominfo import FILES, FILE_BLOCKS
from romtools.disk import Disk, Gamefile, Block
from romtools.dump import DumpExcel
from codec import encode

ORIGINAL_ROM_PATH = os.path.join('original', 'Insiders94.hdm')
TARGET_ROM_PATH = os.path.join('patched', 'Insiders94.hdm')
DUMP_XLS_PATH = 'insiders_dump.xlsx'

Dump = DumpExcel(DUMP_XLS_PATH)
OriginalINS = Disk(ORIGINAL_ROM_PATH, dump_excel=Dump)
TargetINS = Disk(TARGET_ROM_PATH)

FILES_TO_REINSERT = ['IDS',]

for filename in FILES_TO_REINSERT:
    gamefile_path = os.path.join('original', 'decompressed', filename + '.decompressed')
    gamefile = Gamefile(gamefile_path, disk=OriginalINS, dest_disk=TargetINS)
    #pointers = PtrDump.get_pointers(gamefile)

    for block in FILE_BLOCKS[filename]:
        block = Block(gamefile, block)
        print(block)
        previous_text_offset = block.start
        diff = 0
        #print(repr(block.blockstring))
        for t in Dump.get_translations(block):
            if t.en_bytestring != t.jp_bytestring:
                print(t)
                loc_in_block = t.location - block.start + diff

                #print(t.jp_bytestring)
                i = block.blockstring.index(t.jp_bytestring)
                j = block.blockstring.count(t.jp_bytestring)

                index = 0
                while index < len(block.blockstring):
                    index = block.blockstring.find(t.jp_bytestring, index)
                    if index == -1:
                        break
                    index += len(t.jp_bytestring) # +2 because len('ll') == 2

                #if j > 1:
                #    print("%s multiples of this string found" % j)
                assert loc_in_block == i, (hex(loc_in_block), hex(i))

                block.blockstring = block.blockstring.replace(t.jp_bytestring, t.en_bytestring, 1)

                #gamefile.edit_pointers_in_range((previous_text_offset, t.location), diff)
                previous_text_offset = t.location

                this_diff = len(t.en_bytestring) - len(t.jp_bytestring)
                diff += this_diff

        block_diff = len(block.blockstring) - len(block.original_blockstring)
        if block_diff < 0:
            block.blockstring += (-1)*block_diff*b'\x00'
        block_diff = len(block.blockstring) - len(block.original_blockstring)
        assert block_diff == 0, block_diff

        block.incorporate()

    # TODO: Don't encode it if the file is in UNCOMPRESSED_FILES
    gamefile.write(skip_disk=True)
    decompressed_path = 'patched/%s' % gamefile.filename
    print(decompressed_path)
    encode(decompressed_path)
    encoded_path = 'patched/' + filename
    TargetINS.insert(encoded_path, path_in_disk='')
