from modules import filesystem
from modules import memory
from modules import processes
from modules import queue
from modules import resources
import os
import sys

def main():
    print('''dispatcher =>
        PID: 0
        offset: 0
        blocks: 64
        priority: 0
        time: 3
        printers: 0
        scanners: 0
        modems: 0
        drives: 0''')

if __name__ == '__main__':
    main()