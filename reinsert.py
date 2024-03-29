"""
    Insiders '94 reinserter.
    Based on the CRW reinserter.
"""

import os

from rominfo import FILES, FILE_BLOCKS, CONTROL_CODES, UNCOMPRESSED_FILES
from romtools.disk import Disk, Gamefile, Block
from romtools.dump import DumpExcel, PointerExcel
from codec import encode

ORIGINAL_ROM_PATH = os.path.join('original', 'Insiders94.hdm')
TARGET_ROM_PATH = os.path.join('patched', 'Insiders94.hdm')
DUMP_XLS_PATH = 'insiders_dump.xlsx'
POINTER_XLS_PATH = 'insiders_pointers.xlsx'

Dump = DumpExcel(DUMP_XLS_PATH)
PtrDump = PointerExcel(POINTER_XLS_PATH)

OriginalINS = Disk(ORIGINAL_ROM_PATH, dump_excel=Dump, pointer_excel=PtrDump)
TargetINS = Disk(TARGET_ROM_PATH)

FILES_TO_REINSERT = ['IDS', 'ISS']

# TODO: Unsure if there are multiple pointer files, but there is ICS so far
pointer_gamefile_path = os.path.join('original', 'ICS')
pointer_gamefile = Gamefile(pointer_gamefile_path, disk=OriginalINS, dest_disk=TargetINS, pointer_sheet_name='IDS.decompressed')

for filename in FILES_TO_REINSERT:
    gamefile_path = os.path.join('original', 'decompressed', filename + '.decompressed')
    gamefile = Gamefile(gamefile_path, disk=OriginalINS, dest_disk=TargetINS)

    for block in FILE_BLOCKS[filename]:
        block = Block(gamefile, block)
        #print(block)
        previous_text_offset = block.start
        diff = 0


        #print(repr(block.blockstring))
        for t in Dump.get_translations(block):
            if t.en_bytestring != t.jp_bytestring:
                print(t)
                loc_in_block = t.location - block.start + diff

                # Replace control codes
                for cc in CONTROL_CODES:
                    if cc in t.en_bytestring:
                        #print("Found the cc")
                        t.en_bytestring = t.en_bytestring.replace(cc, CONTROL_CODES[cc])
                    if cc in t.jp_bytestring:
                        print("Found a control code")
                        t.jp_bytestring = t.jp_bytestring.replace(cc, CONTROL_CODES[cc])
                #print(t.en_bytestring)

                print(t.jp_bytestring)
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

                # Translated text replacement
                block.blockstring = block.blockstring.replace(t.jp_bytestring, t.en_bytestring, 1)
                #print(block.blockstring)

                # TODO: Is this doing anything?
                pointer_gamefile.edit_pointers_in_range((previous_text_offset, t.location), diff)
                previous_text_offset = t.location

                this_diff = len(t.en_bytestring) - len(t.jp_bytestring)
                diff += this_diff

        block_diff = len(block.blockstring) - len(block.original_blockstring)
        if block_diff < 0:
            block.blockstring += (-1)*block_diff*b'\x00'
        block_diff = len(block.blockstring) - len(block.original_blockstring)
        assert block_diff == 0, block_diff

        block.incorporate()

    if filename in UNCOMPRESSED_FILES:
        # No compression needed if the file is uncompressed to begin with
        gamefile.write()
        # TODO: Do I need to explcitly insert it into the disk too?
    else:
        gamefile.write(skip_disk=True)
        decompressed_path = 'patched/%s' % gamefile.filename
        encode(decompressed_path)
        encoded_path = 'patched/' + filename
        TargetINS.insert(encoded_path, path_in_disk='')

# TODO: Probably need to watch out for writing this multiple times?
print(pointer_gamefile)
pointer_gamefile.write(path_in_disk='')
