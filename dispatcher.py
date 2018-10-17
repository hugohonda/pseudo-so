from modules import filesystem
from modules import memory
from modules import process_manager
from modules import queue
from modules import resource_manager
import os
import sys

pm = process_manager.ProcessManager()
rm = resource_manager.ResourceManager()

def main():
    # inicialização dos recursos
    rm.newResource(type='scanner')
    rm.newResource(type='printer')
    rm.newResource(type='printer')
    rm.newResource(type='modem')
    rm.newResource(type='drive')
    rm.newResource(type='drive')
    print(rm.getCounts())

    pid = 0
    offset = 0
    blocks = 64
    priority = 0
    time = 3
    printers = 0
    scanners = 0
    modems = 0
    drives = 0 

    # print(f'''dispatcher =>
    #     PID: {pid}
    #     offset: {offset}
    #     blocks: {blocks}
    #     priority: {priority}
    #     time: {time}
    #     printers: {printers}
    #     scanners: {scanners}
    #     modems: {modems}
    #     drives: {drives}''')

if __name__ == '__main__':
    main()