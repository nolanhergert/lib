import numpy as np

#Moving average class for numbers, vectors, arrays, etc
#Just pass in shape parameter (arrayname.shape)
class MovingAverage(object):
    def __init__(self, shape, integration_time):
        self.sum                    = np.zeros((np.prod(shape),1),dtype=np.uint64)
        self.integration_time       = integration_time
        self.array                  = np.zeros((np.prod(shape), integration_time),dtype=np.int32)
        self.count                  = 0
        self.arrayIndex             = 0
        self.shape                  = shape
        self.temp                   = np.zeros((np.prod(shape),1),dtype=np.int32)
        
        

    def update(self,newupdate):
        self.count += 1
        #Reshape to a column vector. No, newupdate[:,None] doesn't work for some reason
        self.temp = np.reshape(newupdate,np.prod(self.shape))
        #New mean is simply removing the oldest vector from and adding the new vector
        #to the running sum

        self.sum[:,0] += self.temp - self.array[:,self.arrayIndex]
        self.array[:,self.arrayIndex] = self.temp
        self.arrayIndex = np.mod(self.arrayIndex+1,self.integration_time)
        
        # If we haven't received integration_time samples yet, then account for
        # that in the average (divide by count instead)
        # Also, return the *floating point* value for accuracy
        result = np.divide(self.sum,min(self.count,self.integration_time),dtype=np.float32)
        
        return np.reshape(result,self.shape)