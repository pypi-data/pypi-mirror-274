"""This module defines an interface for the probability law of the number of packet before desynchronization when the probability to lose connection varies from a device to another."""
from scipy.stats import iqr
import numpy as np

from .law import Law

class Law_multip:
    """probability law of the number of packet before desynchronization when the probability to lose connection varies from a device to another."""
    def __init__(self, p,m):
        """
        :param p: Probability for a divice to lose connection.
        :type p: float in [0,1]
        :param m: Number of addresses per in each list managed by the devices.
        :type m :int
        """
        self.p = p
        self.m = m

    def cdf(self,n):
        """Cumulativ distribution function of the number of packets before desynchronization.
        In other words: P(number of packets before desynchronization <= n):

        :param n: Number of packets before desynchronization.
        :type n: int
        :return: P(number of pakets before desynchronization <= n)
        :rtype: float in [0,1]
        """
        P = np.zeros_like(self.p).astype(float)
        for pi,p in enumerate(self.p):
            law = Law(pi,self.m)
            law.eigenvalues()
            P[pi] = law.cdf(n)
        return np.mean(P)

    def cdf_position(self):
        """Return the position of the CDF in R+.
        :return: (start, end) where cdf(start)=0.01 and cdf(end)=0.99.
        :rtype: flot in R+
        """
        #Use smallest p to find the farther point
        law = Law(np.min(self.p), self.m)
        _,end = law.cdf_position()

        #Use bigest p to find the closest point
        law = Law(np.max(self.p), self.m)
        law.eigenvalues()
        start,_ = law.cdf_position()

        return start, end
