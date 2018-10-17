from modules import filesystem
from modules import memory
from modules import process
from modules import queue
from modules import resource
import os
import sys

def main():
    PID = 0
    offset = 0
    blocks = 64
    priority = 0
    time = 3
    printers = 0
    scanners = 0
    modems = 0
    drives = 0 

    print(f'''dispatcher =>
        PID: {PID}
        offset: {offset}
        blocks: {blocks}
        priority: {priority}
        time: {time}
        printers: {printers}
        scanners: {scanners}
        modems: {modems}
        drives: {drives}''')

if __name__ == '__main__':
    main()