import uuid

class Process:
    def __init__(self, pid=None):
        if pid == None:
            pid = uuid.uuid4()
        self.pid = pid
        self.priority = 0

class ProcessManager:
    def __init__(self, processes=[]):
        self.processes = processes
    
    def newProcess(self, pid=None):
        new = Process(pid)
        self.processes.append(new)