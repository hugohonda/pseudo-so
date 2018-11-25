from .memory import MemoryManager
from .queues import QueueManager

EMPTY_PROCESS = {'proc': None, 'pc': 0}


class Process:
    """Process entity.

    Creates a process object.

    Args:
        process_desc (`dict`) Process description. Parameters: boot_time,
                              priority, cpu_time, blocks, printer_id,
                              scanner_req, modem_req and disk_id.
    """
    def __init__(self, process_desc, offset, pid):
        for k, v in process_desc.items():
            setattr(self, k, int(v))
        self.offset = offset
        self.pid = pid

    def __str__(self):
        return (
            f'\tPID: {self.pid}\n'+
            f'\toffset: {self.offset}\n'+
            f'\tblocks: {self.blocks}\n'+
            f'\tpriority: {self.priority}\n'+
            f'\ttime: {self.cpu_time}\n'+
            f'\tprinters: {self.printer_id}\n'+
            f'\tscanners: {self.scanner_req}\n'+
            f'\tmodems: {self.modem_req}\n'+
            f'\tdrivers: {self.disk_id}\n\n'+
            f'process {self.pid} =>'
        )


class ProcessManager:
    """Pseudo OS process manager.

    Manage resources, memory, queues and disk according to each process demand.
    """
    def __init__(self):
        self.curr_pid = 0
        self.mem_m = MemoryManager()
        self.q_m = QueueManager()
        self.curr_proc_context = dict(EMPTY_PROCESS)

    def new_process(self, process_desc):
        """Try to creates a process.
        """
        # TODO: check resources
        try:
            # check memory limits to current process
            offset = self.mem_m.check_limits(process_desc)
        except ValueError as err:
            print(f'Current process cannot be allocated due to : {err}')
            return False

        # creates a process entity with process description
        proc = Process(process_desc, offset, self.curr_pid)
        self.curr_pid += 1
        # allocates process in memory
        self.mem_m.allocate(proc)
        # put process at the queue
        self.q_m.put(proc)
        print(proc)  # shows process information

    def empty(self):
        """Check if there are no process running.
        """
        return self.curr_proc_context['proc'] is None

    def next(self):
        """Simulate next process.

        Returns:
            ``True`` if a process execute with success, ``False`` if some error
            occurred during execution or there are no process to execute.
        """
        if self.curr_proc_context['proc'] is None:
            # select a process from ready processes queue
            curr_proc = self.q_m.get()
            if not curr_proc:
                return False

            self.curr_proc_context['proc'] = curr_proc
            self.curr_proc_context['pc'] = curr_proc.boot_time
            print(f'P{curr_proc.pid} STARTED')
        else:  # continue execution
            curr_proc = self.curr_proc_context['proc']
            pc = self.curr_proc_context['pc']

            # process finished execution
            if pc >= (curr_proc.boot_time+curr_proc.cpu_time):
                print(f'P{curr_proc.pid} return SIGINT')
                self.mem_m.clean(curr_proc)  # free memory
                self.next_process()  # get next process
            else:  # executes another instruction
                instr = pc-curr_proc.boot_time
                print(f'P{curr_proc.pid} instruction {instr+1}')
                self.curr_proc_context['pc'] += 1

    def next_process(self):
        self.curr_proc_context = dict(EMPTY_PROCESS)
