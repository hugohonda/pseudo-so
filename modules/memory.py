class MemoryManager:
    """Pseudo OS memory manager.

    Memory allocation is organized as a set of contiguous blocks.
    Total of 1024 blocks.
    """
    def __init__(self):
        self.mem = [0]*1024  # memory total size, 1024 blocks

    def check_limits(self, process):
        """Check limits to process allocation.

        Args:
            process (`dict`) Process information.
        Raises:
            ValueError: If there are no space to allocate the process.
        """
        if process['priority'] == 0:  # real time processes
            base_seg, limit_seg = 0, 63
            proc_type = 'real-time'
        else:  # user processes
            base_seg, limit_seg = 64, 1023
            proc_type = 'user'

        # process size larger than expected for real-time processes
        if process['blocks'] > (limit_seg-base_seg)+1:
            raise ValueError(f'This process is too big to {proc_type} '
                             'processes memory space. It should contain '
                             f'less than {limit_seg+1} blocks.')

        # try to find place to allocate
        while base_seg <= limit_seg:
            free_b = 0  # possible blocks to allocation
            last_base = base_seg
            while not self.mem[base_seg]:
                free_b += 1
                if base_seg >= limit_seg:
                    break
                base_seg += 1
                if free_b == process['blocks']:
                    break

            # enough blocks to allocate the process
            if free_b == process['blocks']:
                return last_base

            if base_seg <= limit_seg:
                base_seg += 1

        raise ValueError(f'Memory space to {proc_type} processes is full or '
                         f'this process is too big to {proc_type} processes '
                         'current memory space.')

    def allocate(self, proc):
        """Allocates memory to a process.

        Args:
            process (:obj:`Process`) Process entity.
        """
        offset, proc_b = proc.offset, proc.blocks
        self.mem[offset:offset+proc_b] = [1]*proc_b

    def clean(self, proc):
        """Free memory allocated to a process.

        Args:
            process (:obj:`Process`) Process entity.
        """
        offset, proc_b = proc.offset, proc.blocks
        self.mem[offset:offset+proc_b] = [0]*proc_b
