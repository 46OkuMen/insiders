import os
import regex as re
from rominfo import FILE_BLOCKS
from romtools.dump import BorlandPointer, DumpExcel, PointerExcel
from romtools.disk import Gamefile, Block, Disk

pointer_regex = r'\\xbe\\x([0-f][0-f])\\x([0-f][0-f])\\xe8'

def find_all(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1: return
        yield start
        start += len(sub) # use start += 1 to find overlapping matches


def capture_pointers_from_function(regex, hx): 
    return re.compile(regex).finditer(hx, overlapped=True)

def location_from_pointer(pointer, constant):
    try:
        result = '0x' + str(format((unpack(pointer[0], pointer[1]) + constant), '05x'))
    except:
        result = '0x' + str(format((unpack(hex(pointer[0]), hex(pointer[1])) + constant), '05x'))
    return result

def unpack(s, t=None):
    if t is None:
        t = str(s)[2:]
        s = str(s)[0:2]
    s = int(s, 16)
    t = int(t, 16)
    value = (t * 0x100) + s
    return value

DUMP_XLS_PATH = 'insiders_dump.xlsx'
POINTER_XLS_PATH = 'insiders_pointers.xlsx'
Dump = DumpExcel(DUMP_XLS_PATH)
# TODO: Add ORITTLE back in once I've mapped the CD version.
files_to_search = ['IDS']
pointer_files = ['ICS']

problem_count = 0

try:
    os.remove(POINTER_XLS_PATH)
except WindowsError:
    pass
PtrXl = PointerExcel(POINTER_XLS_PATH)

pf_hex = {}

for pf in pointer_files:
    with open('original\\' + pf, 'rb') as f:
        only_hex = u''
        bs = f.read()
        for c in bs:
            only_hex += u'\\x%02x' % c

        pf_hex[pf] = only_hex


for f in files_to_search:
    GF = Gamefile(os.path.join('original', f))
    file_blocks = FILE_BLOCKS[f]
    pointer_constant = 0
    pointer_tables = []
    
    # Note: Ugly, but otherwise PointerExcel can't find the right sheet name
    worksheet_name = GF.filename + '.decompressed'

    found_text_locations = []
    print(f)

    previous_pointer_locations = []

    try:
        worksheet = PtrXl.add_worksheet(worksheet_name)
    except AttributeError:
        print("You have the worksheet open. Close it and try again")
        worksheet = PtrXl.add_worksheet(worksheet_name)
    row = 1

    for pf in pf_hex:
        pointers = capture_pointers_from_function(pointer_regex, pf_hex[pf])
        for p in pointers:
            #print(p)
            pointer_location = p.start()//4 + 1
            pointer_location = '0x%05x' % pointer_location
            #print(pointer_location)

            text_location = int(location_from_pointer((p.group(1), p.group(2)), pointer_constant), 16)
            for (start, stop) in FILE_BLOCKS[f]:
                if start <= text_location < stop:
                    print(pointer_location, " points to ", hex(text_location))

                    obj = BorlandPointer(GF, pointer_location, text_location)
                    worksheet.write(row, 0, hex(text_location))
                    worksheet.write(row, 1, pointer_location)

                    # TODO: To write useful info columns like "bytes" or "points to", need to rewrite some stuff - the pointers are in a different file than the text

                    row += 1

                    previous_pointer_locations.append(pointer_location)

PtrXl.workbook.close()
