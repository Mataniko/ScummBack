
import argparse
import mmap
from os import path
from collections import namedtuple

# Set up the args
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--game', metavar='GAME',  help='Game identifier',
                    required=True, choices=['indy3', 'indy4', 'dig', 'loom'])
parser.add_argument('--exe', metavar=' EXE', dest='file',
                    help='Path to the game executable', required=True)
parser.add_argument('--out', metavar=' OUTPUT',
                    help='Optional path to export the file', default='')
args = parser.parse_args()

# First sixteen bytes of each game resource file.
DIG = b'\x52\x4E\x41\x4D\x00\x00\x04\x5F\x01\x93\x90\x98\x90\xFF\xFF\xFF'  # dig
INDY3 = b'\xF7\x01\x00\x00\x30\x52\x63\x00\x00\x00\x00\x00\x00\x31\x00\x00'  # indy3
LOOM = b'\x13\x03\x00\x00\x52\x4E\x01\x93\x90\x98\x90\xFF\xFF\xFF\xFF\xFF'  # loom
INDY4 = b'\x3B\x27\x28\x24\x69\x69\x6A\xBA\x68\xF5\xF9\xFA\xBB\xF9\xF0\xF0'  # indy4

# Known game variants and their offsets for Windows and Mac
Game = namedtuple('Game', 'bytes length filename name offsets')
games = {
    "indy3":  Game(INDY3,  6295, '00.LFL', 'Indiana Jones and the Last Crusade', [162056, 150368]),
    "loom":   Game(LOOM,   6295,  '000.LFL', 'Loom', [187248, 170464]),
    "indy4":  Game(INDY4,  12035, 'ATLANTIS.000', 'Indiana Jones and the Fate of Atlantis', [224336, 260224]),
    "dig":    Game(DIG,    16304,   'DIG.LA0', 'The Dig', [340632, 339744]),
}

# Extract the game file from the executable
game = games[args.game]
print('Attempting to extract {} from {}'.format(game.filename, args.file))
with open(args.file, 'rb') as file:
    mm = mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ)
    offset = mm.find(game.bytes)
    if offset > 0:
        print('Found game data at offset: {}'.format(offset))
        if not offset in game.offsets:
            print('WARNING: Offset is from an unknown variant')
        with open(path.join(args.out, game.filename), 'wb') as outfile:
            mm.seek(offset)
            outfile.write(mm.read(game.length))
            print('Successfuly extracted {}'.format(game.filename))
    else:
        print('Unable to find game data')
