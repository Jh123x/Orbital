import queue

#Main class for the checkable queue
class CheckableQueue(queue.Queue): # or OrderedSetQueue
    def __contains__(self, item):
        """Check if the item is inside the queue"""
        with self.mutex:
            return item in self.queue