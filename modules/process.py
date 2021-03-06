from .resources import ResourceManager
from .memory import MemoryManager
from .queues import QueueManager


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
            setattr(self, k, v)
        self.offset = offset
        self.pid = pid
        self.pc = self.boot_time + self.cpu_time  # process execution counter
        self.started = False

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
            f'\tdrivers: {self.disk_id}\n'
        )


class ProcessManager:
    """Pseudo OS process manager.

    Manage resources, memory and priorities queues according to each process
    demand.
    """
    def __init__(self):
        self.system_clock = 0
        self.curr_proc = None
        self.curr_pid = 0
        # old processes that contains processes that runned with
        # success and their number of operations available
        self.old_procs = {}

        # managers
        self.res_m = ResourceManager()
        self.mem_m = MemoryManager()
        self.q_m = QueueManager()

    def process_status(self, pid):
        """Process status.

        Args:
            pid (`int`) Process id to search.
        Returns:
            0 if the process never existed, 1 if the process is running,
            2 if the process existed and finished its execution.
        """
        if self.curr_proc is not None and self.curr_proc.pid == pid:
            return 1
        if pid >= self.curr_pid:
            return 0
        return 2

    def new_process(self, process_desc):
        """Try to creates a process.

        Args:
            process_desc (`dict`) Process description. Parameters: boot_time,
                                  priority, cpu_time, blocks, printer_id,
                                  scanner_req, modem_req and disk_id.
        """
        try:
            # checks if resources demanded from process is available
            self.res_m.resources_available(process_desc)
        except ValueError as err:
            print(f'Current process cannot be allocated due to : {err}')
            return False

        try:
            # checks memory limits to current process
            offset = self.mem_m.check_limits(process_desc)
        except ValueError as err:
            print(f'Current process cannot be allocated due to : {err}')
            return False

        # creates a process entity with process description
        proc = Process(process_desc, offset, self.curr_pid)
        self.curr_pid += 1
        # allocates process in memory
        self.mem_m.allocate(proc)
        # allocates process resources
        self.res_m.allocate(proc)
        # put process at the queue
        self.q_m.put(proc)
        print(proc)  # shows process information

    def empty(self):
        """Check if there are no process running.

        Returns:
            ``True`` if there are no current process, ``False`` otherwise.
        """
        return self.curr_proc is None

    def next(self):
        """Simulate next process.

        Returns:
            ``True`` if a process execute with success, ``False`` if some error
            occurred during execution or there are no process to execute.
        """
        self.system_clock += 1
        if self.curr_proc is None:  # there are no process running
            if self.next_process() is None:  # try catch next process
                return False
        else:  # continue execution
            # execute instruction
            instr = self.curr_proc.pc-self.curr_proc.boot_time
            print(f'P{self.curr_proc.pid} instruction {instr+1}')
            self.curr_proc.pc += 1

            # every 5 clock ticks update priority, OS init doesn't count
            if self.system_clock != 0 and not self.system_clock%5:
                self.q_m.update_priority()

            limit_time = self.curr_proc.boot_time + self.curr_proc.cpu_time
            if self.curr_proc.pc >= limit_time:  # process finished execution
                print(f'P{self.curr_proc.pid} return SIGINT')
                self.curr_proc.pc = limit_time
                self.mem_m.clean(self.curr_proc)  # free memory
                self.res_m.free(self.curr_proc)  # free resources
                self.old_procs[self.curr_proc.pid] = {
                                        'itr': self.curr_proc.cpu_time,
                                        'priority': self.curr_proc.priority}
                self.next_process()
                return True

            if self.curr_proc.priority != 0:  # swap user processes
                # put current process back to queue if is not over
                if self.curr_proc.pc < limit_time:
                    self.q_m.put(self.curr_proc)
                self.next_process()  # get next process

        return True

    def next_process(self):
        """Get next process from ready processes queue.

        Returns:
            Next :obj:`Process` or None.
        """
        self.curr_proc = None
        # select a process from ready processes queue
        curr_proc = self.q_m.get()
        if not curr_proc:
            return None

        self.curr_proc = curr_proc
        # process was never executed
        if not curr_proc.started:
            curr_proc.pc = curr_proc.boot_time
            curr_proc.started = True
            print(f'process {curr_proc.pid} =>\nP{curr_proc.pid} STARTED')
