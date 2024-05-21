"""This module defnies an interface to the probability law of the number of packet sent by a device befor desynchronization when using the sequential pseudonym scheme."""
import math
import numpy as np

class Law:
    """Probability law of the number of packet sent by a device dbefore desynchronization.
    """
    def __init__(self, p, m):
        """
        :param p: Probability to lose connection.
        :type p: float in [0,1]
        :param m: Number of pseudonyms maintained by the device.
        :type m: int
        """
        self.p = p
        self.q = 1-p
        self.a = (1-p)*p**m
        self.m = m
        self.eigen_computed = False

    def eigenvalues(self):
        """Computes the eigenvalues to solve the recursive sequence."""
        p = self.p 
        q = self.q 
        a = self.a
        m = self.m 

        pol_char = np.zeros(m+2).astype(float)
        pol_char[0] = 1
        pol_char[1] = -1
        pol_char[-1] = a
        roots = np.roots(pol_char)
        roots = roots.reshape(m+1)
        self.l = roots
        self.eigen_computed = True

        #Finding initial conditions
        u = np.zeros(m+1).astype(float)
        for n in range(m+1):
            u[n] = 1-p**m-n*(1-p)*p**m
        I = u[:m+1].reshape(-1,1)
        L = np.zeros([m+1,m+1]).astype(np.complex_)
        for i in range(m+1):
            L[i,:] = roots**(i)
        try:
            self.c = np.matmul(np.linalg.inv(L),I).reshape(m+1)
        except:
            self.c = float("nan")
            print("pas invers")

    def mass(self, N):
        """Mass function of the number of packet before desynchronization. 
        In other words return P(desynchronization of N packets sent).
        :param N: Number of packets.
        :type N: int
        :return: P(desynchronization of N packets sent)
        :rtype: float in [0,1]
        """
        m = self.m
        p = self.p
        if N<m:
            return 0
        elif N==m:
            return p**m
        elif N<=2*m:
            return (1-p)*p**m
        else:
            return np.real(np.sum(self.c*self.l**(N-2*m-1))*(1-p)*p**m)

    def cdf(self, N):
        """Cumulative distribution function of the number of packet before desynchronization.
        In other words return P(send less than N packets beforedesynchronization).

        :param N: number of packets.
        :type N: int
        :return: P(send less than N packets beforedesynchronization).
        :rtype: float in [0,1]
        """
        if not(self.eigen_computed):
            self.eigenvalues()
        p = self.p 
        q = self.q 
        a = self.a
        m = self.m 
        l = self.l
        c = self.c

        """P(D<=N)"""
        if N<m:
            return 0
        elif N<=2*m:
            return p**m+(N-m)*(1-p)*p**m
        else:
            un_sum = np.sum(c*(1-l**(N-2*m))/(1-l))
            return np.real(p**m+m*(1-p)*p**m + (1-p)*p**m*un_sum)

    def cdf_multin(self, N):
        """N : nombre de messages"""
        P = np.zeros_like(N).astype(float)
        for ni,n in enumerate(N):
            P[ni] = self.cdf(n)

        return np.mean(P)


    def cdf_position(self):
        """Return the position of the cumulative distribution function.

        :return: (start, end) such that the cumulative distribution function is greater than 0.01 after start and less than 0.99 after end.
        :rtype: tuple of floats
        """
        self.eigenvalues()
        p = self.p 
        q = self.q 
        a = self.a
        m = self.m 
        l = self.l
        c = self.c
         
        #cdf start point
        s = 0.01
        if self.cdf(m)<0.01:
            start = m
        else:
            x0=2*m+1
            x1 = x0
            #for i in range(1,niter):
            #while (np.abs(f(x0,p,m,l,c,s))>1):
            while (np.abs(self.cdf(x0)-s)>1):
                left = (s-p**m-m*q*p**m)/(q*p**m)
                f = np.real(np.sum(c*(1-l**(x0-2*m))/(1-l))) - left
                fp = (-1)*np.real(np.sum(c*(l**(x0-2*m)*np.log(l))/(1-l)))
                x1 = x0 - f/fp
                x0 = x1
            start = x1

        #cdf end point
        s = 0.99
        x0=2*m+1
        x1 = x0
        i = 0

        while (np.abs(self.cdf(x1)-s)>0.005):
            for i in range(1000):
                left = (s-p**m-m*q*p**m)/(q*p**m)
                f = np.real(np.sum(c*(1-l**(x0-2*m))/(1-l))) - left
                fp = (-1)*np.real(np.sum(c*(l**(x0-2*m)*np.log(l))/(1-l)))
                x1 = x0 - f/fp
                x0 = x1
                i += 1
            if math.isnan(x1):
                x0 = 2*m+1
                x1 = x0
                s = s - 0.1*s
            elif (np.abs(self.cdf(x1)-s)>0.005):
                s = s - 0.1*s

        end = x1

        return start, end

    def cdf_inv(self, s):
        """Inverse cumulative distribution function.

        :param s: Probability that the number of packet sent before desynchronization is at most N
        :type s: float in [0,1]
        :return: Return N such that P(send less than N packets beforedesynchronization) = N.
        :rtype: int
        """

        m = self.m
        p = self.p
        q = 1-p
        c = self.c
        l = self.l
        x0=2*m+1
        x1 = x0
        i = 0

        while (np.abs(self.cdf(x1)-s)>0.005):
                left = (s-p**m-m*q*p**m)/(q*p**m)
                f = np.real(np.sum(c*(1-l**(x0-2*m))/(1-l))) - left
                fp = (-1)*np.real(np.sum(c*(l**(x0-2*m)*np.log(l))/(1-l)))
                x1 = x0 - f/fp
                x0 = x1
                #i += 1

        return x1


    def mean(self):
        """Expectation of the number of packet sent before desynchronization computed using.

        :return: E(D) where D is the number of packet sent before desynchronization.
        :rtype: int
        """
        m = self.m
        p = self.p
        q = 1-p
        E = 0
        E += m*p**m + q*p**m*(3*m**2+m)/2
        E += q*p**m*(np.sum(self.c*self.l/(1-self.l)**2)+(2*m+1)*np.sum(self.c/(1-self.l)))
        return np.real(E)
