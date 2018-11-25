from queue import PriorityQueue, Queue


class QueueManager(Queue):
    """Queue manager from pseudo operating system.

    There are 2 main queues: ready processes and user processes. This class
    controls the global queue `ready`. Real time processes enter in ready
    queue with first priority.

    Ready queue are FIFO, user processes queue has 3 priorities queues.
    Real time processes are non preemptive. User processes can be preemptive
    with a quantum equal to 1 second.
    """
    def __init__(self):
        super(QueueManager, self).__init__()
        self.qsize = 1000  # queues size

        # ready processes
        self.ready_p = PriorityQueue(self.qsize)
        # user processes priorities queues
        self.p_queues = [Queue(self.qsize), Queue(self.qsize),
                         Queue(self.qsize)]
        # user processes main queue
        self.user_p = PriorityQueue(self.qsize)

    def put(self, proc):
        """Operation to put a process at the right queue.

        Args:
            proc (:obj:`Process`) Process entity.
        """
        if not proc.priority:  # real-time process
            self.ready_p.put((0, proc))

    def get(self):
        """Operation to get a process from ready processes queue.

        Returns:
            Next :obj:`Process` or None if there are no processes to execute.
        """
        # selects next process from ready processes queue
        if self.ready_p.empty():
            return []
        else:
            return self.ready_p.get()[1]
