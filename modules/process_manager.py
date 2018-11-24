import uuid

class Process:
    def __init__(self, start_time, priority, cpu_time, n_blocks, 
                 printer, scanner, modem, disk, pid=None):
        self.start_time = start_time
        self.priority = priority
        self.cpu_time = cpu_time
        self.n_blocks = n_blocks
        self.printer = printer
        self.scanner = scanner
        self.modem = modem
        self.disk = disk
        if pid == None:
            pid = uuid.uuid4()
        self.pid = pid

    def __str__(self):
        return (
            f"{self.pid},"+
            f"{self.start_time},"+
            f"{self.priority},"+
            f"{self.cpu_time},"+
            f"{self.n_blocks},"+
            f"{self.printer},"+
            f"{self.scanner},"+
            f"{self.modem},"+
            f"{self.disk}"
        )
        
class ProcessManager:
    __instance = None
    @staticmethod 
    def getInstance():
        """ Static access method. """
        if ProcessManager.__instance == None:
            ProcessManager()
        return ProcessManager.__instance

    def __init__(self, processes=[]):
        if ProcessManager.__instance == None:
            self.processes = processes
            ProcessManager.__instance = self

    def newProcess(self, start_time, priority, cpu_time, n_blocks, 
                 printer, scanner, modem, disk, pid=None):
        new = Process(start_time, priority, cpu_time, n_blocks, 
                 printer, scanner, modem, disk, pid)
        self.processes.append(new)