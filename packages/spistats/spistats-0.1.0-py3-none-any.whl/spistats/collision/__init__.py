"""This module defines an interface to the probability law of the number of collisions per packet sent in a sequential pseudonyms scheme."""
import math
import numpy as np

class Collision:
    """Probabaility law of the number of collisions in function of various network parameters.
    """
    def __init__(self,nbr_dev,nbr_adr,adr_per_dev):
        """
        :param nbr_dev: Number of devices in the network.
        :type nbr_dev: int
        :param nbr_adr: Number of addresses to chose from. For instance an 8 bit scheme has 2**8 addresses.
        :type nbr_adr: int
        :param adr_per_dev: Number of pseudonymes maintained by each device.
        :type adr_per_dev: int
        """
        self.M = nbr_dev
        self.p = 1/nbr_adr
        self.q = 1-(1-self.p)**adr_per_dev

        mass = []
        for i in range(0,self.M-1):
            mass += [math.comb(nbr_dev-1,i)*self.q**i*(1-self.q)**(self.M-1-i)]
        self.mas = np.array(mass)
        self.cd = np.cumsum(mass)

    def mean(self):
        """Expectation of the number of collisions for each packet sent.

        :return: E(number of collisions)
        :rtype: int
        """
        return 1+(self.M-1)*self.q

    def mass(self, n):
        """Mass function of the number of collisions for each packet sent evaluated at n.
        In other words: P(number of collision = n).

        :param n: Number of collisions.
        :type n: int
        :return: P(number of collision = n)
        :rtype: float in [0,1]
        """
        if n==0:
            return 0
        elif n<=self.M:
            return self.mas[n-1]
        else:
            return 0

    def cdf(self, n):
        """Cumulativ distribution function of the number of collision evaluated at n.
        In other words: P(number of collision <= n):

        :param n: Number of collisions.
        :type n: int
        :return: P(number of collision <= n)
        :rtype: float in [0,1]
        """

        if n==0:
            return 0
        elif n<=self.M:
            return self.cd[n-1]
        else:
            return 1

    def cdfinv(self, p):
        """Inverse function of the cdf. 
        This function return n such that P(number of collision <= n) = p

        :param p: Probability that the number of collisions is lesser or equal than n.
        :type p: float in [0,1]
        :return: n such that P(number of collision <= n) = p.
        :rtype: int
        """
        n = 1+np.argwhere(self.cd>=p)[0][0]
        return n



