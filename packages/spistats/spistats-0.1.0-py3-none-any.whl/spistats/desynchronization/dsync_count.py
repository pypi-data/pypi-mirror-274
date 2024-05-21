"""This module contains an interfaces to the probability law of the number of desynchronization of one device when sending n packets."""
import numpy as np
from .law import Law

class NumberOfDsync:
    """Probability law of the number of desynchronization of one device when sending n packets."""
    def __init__(self,p,m,n):
        """
        :param p: Probability of packet loss.
        :type p: float in [0,1]
        :param m: Size of the list of indentifiers maintained by each device.
        :type m: int
        :param n: Number of packet recived by the device.
        :type n: int
        """
        self.p = p
        self.m = m
        self.n = n

        self.law = Law(p,m)
        self.law.eigenvalues()

        #c is the matric used to compute the recursion sequence
        self.c = np.zeros([n,1]).astype(float)
        for l in range(1,n+1):
            self.c[l-1,0] = self.law.cdf(l)

    def mass(self, k):
        """Mass function of the number of number of desynchronization for each device evluated at k.
        In other words: P(number of desynchronization = n).

        :param k: Number of desynchronization.
        :type k: int
        :return: P(number of desynchronization = n)
        :rtype: float in [0,1]
        """
        size = np.shape(self.c)[1]
        if size >= k:
            return self.c[-1,k-1]
        else:
            #If we haven't generated enough values of c
            #We need to extend it by k-size columns
            padding = np.zeros([self.n,k-size])
            self.c = np.hstack([self.c,padding])
            print(np.shape(self.c))

            for j in range(2,k+1):
                for i in range(1,self.n+1):
                    s = 0
                    for l in range(1,i-j):
                        s += self.law.mass(l)*self.c[i-l-1,j-2]
                    self.c[i-1,j-1] = s

            return self.c[-1,k-1]

    def cdf(self, k):
        """Cumulativ distribution function of the number of desynchronizations evaluated at k.
        In other words: P(number of desynchronization <= n):

        :param k: Number of collisions.
        :type k: int
        :return: P(number of desynchronization <= n)
        :rtype: float in [0,1]
        """
        #We don't sum on the mass but directly on c
        #It removes a lot of operations
        size = np.shape(self.c)[1]
        if size >= k:
            return (1-self.law.cdf(self.n))+np.sum(self.c[-1,:k])
        else:
            #Compute missing values of c in the mass function
            self.mass(k)
            return (1-self.law.cdf(self.n))+np.sum(self.c[-1,:k])

    def cdf_position(self):
        """Indicate the position of the CDF in R+."""
        #Pre-compute c to save time when looping around cdf for plot
        self.mass(10)
        #return 1,int(self.n/self.m)
        return 1,10



