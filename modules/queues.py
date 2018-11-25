from queue import PriorityQueue, Queue


class PriorityEntry:
    """Class to compare process priority order.

    Args:
        priority (`int`) Process priority.
        data (:obj:`Process`) Process entity.
    """
    def __init__(self, priority, data):
        self.data = data
        self.priority = priority

    def __lt__(self, other):
        return self.priority < other.priority


class QueueManager(Queue):
    """Pseudo OS queue manager.

    Ready processes queue is the global queue. Real-time processes are
    defined with priority 0 and user processes with 1, 2 and 3. This class
    controls the global queue `ready`.

    Ready queue are FIFO. Real time processes are non preemptive.
    User processes can be preemptive with a quantum equal to 1 second.
    """
    def __init__(self):
        super(QueueManager, self).__init__()
        self.qsize = 1000  # queue size
        self.ready_p = PriorityQueue(4*self.qsize)  # ready processes queue

    def put(self, proc):
        """Operation to put a process in the ready processes queue.

        Args:
            proc (:obj:`Process`) Process entity.
        """
        entry = PriorityEntry(proc.priority, proc)
        self.ready_p.put(entry)

    def get(self):
        """Operation to get a process from ready processes queue.

        Returns:
            Next :obj:`Process` or None if there are no processes to execute.
        """
        # selects next process from ready processes queue
        if self.ready_p.empty():
            return []
        else:
            return self.ready_p.get().data

    def update_priority(self):
        """Update priority using aging technique.

        Aging technique is used to solve starvation problem at the priority
        queue. After 5 clock ticks all user processes increase one priority
        level.
        """
        new_queue = PriorityQueue(4*self.qsize)
        for _ in range(self.ready_p.qsize()):
            curr_queue = self.ready_p.get().data
            if curr_queue.priority != 0 and curr_queue.priority != 1:
                curr_queue.priority -= 1

            entry = PriorityEntry(curr_queue.priority, curr_queue)
            new_queue.put(entry)

        self.ready_p = new_queue
        print('Priority updated in user processes queue.')
