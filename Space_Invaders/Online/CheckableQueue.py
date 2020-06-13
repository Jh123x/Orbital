import queue


#Main class for the checkable queue
class CheckableQueue(queue.Queue): # or OrderedSetQueue
    def __contains__(self, item):
        with self.mutex:
            return item in self.queue