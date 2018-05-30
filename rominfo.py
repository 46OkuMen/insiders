"""
    Rom description of Insiders '94.'
"""

FILES = ['IDS', 'ISS', 'IS2', 'ALD', 'AMD', 'BKD', 'CPU', 'DAT1', 'BOOK']

UNCOMPRESSED_FILES = ['BOOK',]

FILE_BLOCKS = {
    "IDS": [
        (0x3081, 0x30a5),
        (0x3310, 0x336b),
        (0x33a0, 0x33d0),  # SYSTEM
        (0x3400, 0x3431),
        (0x3436, 0x3477),
        (0x3478, 0x347f),
        (0x3480, 0x36dd),  # Lots of UU blocks that should be broken up
        (0xb080, 0xb14e),
        (0xb160, 0xb21a),
        (0xb230, 0xb2e2),
        (0xb300, 0xb353),
        (0xb401, 0xb6c2),
        (0xb800, 0xba36),
        (0xba80, 0xbab3),
        (0xbab8, 0xbae7),
        (0xbae9, 0xbc3f),  # Lots of UU blocks here too
    ],

    "ISS": [
        (0x8000, 0x81d7),
        (0x8401, 0x8e4a),
        (0x9001, 0x95c3),
        (0x9c01, 0xa26a),
        (0xac00, 0xb0db),
    ],

    "IS2": [
        (0x4a01, 0x4e50),
        (0x5d01, 0x62c1),
        (0x6901, 0x6f69),
        (0x7901, 0x7c1c),
        (0xa080, 0xa5a5),
        (0xa882, 0xabec),
        (0xac80, 0xaf55),
        (0xc4c1, 0xc4e4),
        (0xc4f0, 0xc937),
    ],

    "ALD": [
        (0x90, 0x1aa),
        (0x1b0, 0x1f7),
        (0x200, 0x234),
        (0x240, 0x263),
        (0x280, 0x30e),
        (0x310, 0x346),
        (0x600, 0x700),
        (0x800, 0x8e5),
    ],

    "AMD": [
        (0x80, 0xa8),
        (0x100, 0x187),
        (0x200, 0x664),
    ],

    "BKD": [
        (0x100, 0x1ff),
        (0x281, 0x2a4),
        (0x2a8, 0x2d5),
        (0x2d9, 0x2f0),
        (0x300, 0x314),
        (0x318, 0x338),
        (0x340, 0x34a),
        (0x350, 0x374),
        (0x380, 0x389),
        (0x390, 0x3b2),
        (0x3b8, 0x3d8),
    ],

    "CPU": [
        (0x101, 0x303),
    ],

    "DAT1": [
    ],

    "BOOK": [
    ],
}
