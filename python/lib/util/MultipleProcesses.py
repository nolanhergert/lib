import math
import multiprocessing
import sys
import time



class MultipleProcesses:
    """
    A class for parallelizing the same function call on the same machine and
    limiting the number of total processes in use.
    Adapted from: http://stackoverflow.com/questions/4685253/multiprocessing-in-python-ensuring-a-minimum-number-of-child-processes-are-act
    """
    def __init__(self, cores = math.floor(4*multiprocessing.cpu_count()/5)):
        
        self.cores = cores        
        self.processes = []
    
    def AddProcess(self, target=None, args=[], kwargs=[]):
        """
        It's probably good to not abuse this call.
        time.sleep() a few before calling again

        Parameters
        ----------
        target : function "handle"
            A reference to the function to call
        args : list
            The arguments that will be passed to target
        """
        if (self.Full() == False):
            # Make sure that args is a list
            if (type(args) != list):
                args = [args]
            p = multiprocessing.Process(target = target, args = args, kwargs=kwargs)
            self.processes.append(p)
            p.start()
            return True     # success
        else:
            return False    # failure, need to call again later

    def ReapAll(self):
        # Reap all dead children
        for n, p in enumerate(self.processes):
            if not p.is_alive():
                self.processes.pop(n)
                
    def Full(self):
        """
        Check if the pool is full
        """
        self.ReapAll()
        if (len(self.processes) >= self.cores):
            return True
        return False
    
    def Empty(self):
        """
        Check if the pool is empty
        """
        self.ReapAll()
        if (len(self.processes) > 0):
            return False
        return True
    
    
def TimeTest(seconds, num):
    for t in range(seconds):
        print str(num) + ': ' + str(t)
        sys.stdout.flush()
        time.sleep(1)

if __name__ == '__main__':

    pool = MultipleProcesses()
    for i in range(5):
        while (pool.AddProcess(TimeTest,args=[3,i]) == False):
            print 'Waiting to add another process'
            time.sleep(1)
    
    # Allow all of the processes to finish
    while(pool.Empty() == False):
        time.sleep(1)
        
    print 'Done!'