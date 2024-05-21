"""This module generates the graphs of the paper https://inria.hal.science/hal-04525080.
Based on Markov chains we compute the average number of packet sent before desynchronization.
Executing this module with python -m generates the plots in a directory named "plot" in the current working directory.
"""
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import os

if __name__=="__main__":
    plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.size":30
    })


def Ef(p,m):
    """Expectation of the number of packet before desynchronization based on Markov chains theory.
    :param p: Packet loss rate.
    :type p: float in [0,1]
    :param m: Size if the identifier list.
    :type m: int
    :return: Expectation of the number of packet before desynchronization.
    :rtype: float
    """
    return (p**(-m)-1)/(1-p)

if __name__=="__main__":
    path = Path("plot")
    os.makedirs(path,exist_ok=True)

    ps = np.array([0.01,0.05,0.1,0.3,0.4,0.5])
    ms = np.array([5,10,15,20,25,30])

    E = np.zeros([len(ps),len(ms)]).astype(float)
    for i,p in enumerate(ps):
        for j,m in enumerate(ms):
            E[i,j] = Ef(p,m)


    psl = [f"PLR={int(p*100)}\%" for p in ps]
    linestyle_tuple = [
        ('solid', 'solid'),
        #  ('densely dotted',        (0, (1, 1))),
        #  ('loosely dashed',        (0, (5, 10))),
        ('dashed',                (0, (5, 5))),
        ('dotted',                (0, (1, 1))),
        ('densely dashdotdotted', (0, (3, 1, 1, 1, 1, 1))),
        # ('loosely dashdotted',    (0, (3, 10, 1, 10))),
        ('long dash with offset', (5, (10, 3))),
        ('dashdotted',            (0, (3, 5, 1, 5))),
        # ('densely dashdotted',    (0, (3, 1, 1, 1))),
        ('dashdotdotted',         (0, (3, 5, 1, 5, 1, 5))),
        ('loosely dotted',        (0, (1, 10))),
        ('densely dashed',        (0, (5, 1))),
        ('loosely dashdotdotted', (0, (3, 10, 1, 10, 1, 10))),
    ]
    all_styles = []
    for name, t in linestyle_tuple: 
        all_styles.append(t)
    style=iter(all_styles)
    psl = iter(psl)

    for i in range(np.shape(E)[0]):
        plt.plot(ms,np.transpose(np.log(E[i,:]))/np.log(10),label=next(psl),linestyle=next(style))
    plt.ylim([0,20])
    plt.legend(loc='lower right',bbox_to_anchor=(1.3, 0))
    plt.xlabel("Pre-generated list length")
    ax=plt.gca()
    log_lab = ax.get_yticks()
    m = int(np.min(log_lab))
    M = int(np.max(log_lab))
    pos = np.linspace(0,M,M+1)
    idx = np.linspace(0,len(pos)-1,len(pos)).astype(int)
    pos = pos[idx%5==0]
    ax.set_yticks(pos)
    ax.set_xticks(ms)
    ax.set_yticklabels([f"$10^{{ {int(t)} }}$" for t in pos])
    plt.ylabel("Average number of packets\nbefore desynchronization")
    figure = plt.gcf()  # get current figure
    figure.set_size_inches(16, 7) # set figure's size manually to your full screen (32x18)
    plt.savefig(Path(path,"mvsE.pdf"),bbox_inches="tight")
    plt.clf()
