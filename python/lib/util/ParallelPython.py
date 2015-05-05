import pp

from python.lib.util.ParallelPythonTestFunction import TestFunc


class ParallelPython():
    
    # Potentially available network machines. They will be queried over the
    # network to see if the ppserver.py script is started
    ##                all of these are 24-core Xeon machines
    #ppservers = (r'\\USIR-MJZECWL',r'\\USIR-MJZECWK',r'\\USIR-MJZECWM',r'\\USR-MJZECWH')
    ppservers = (r'10.50.8.120',)
    
    def __init__(self):
        self.job_server = pp.Server(ppservers=self.ppservers)

    
#    def SubmitCmdLine(self, CmdLineCall):
#        self.job_server.submit(subprocess.call, [CmdLineCall], kwargs={'shell':True, 'stderr':subprocess.PIPE})
    
    
    
if __name__ == '__main__':
    p = ParallelPython()
    f1 = p.job_server.submit(TestFunc,(),(),('subprocess',))
    print f1()
    
    print 2
    
        
