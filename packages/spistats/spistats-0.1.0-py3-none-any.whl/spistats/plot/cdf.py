"""This module provides a function to plot the cdf of the law of the number of desynchronization before desynchronization."""
import numpy as np
import matplotlib.ticker as mtick
import matplotlib.pyplot as plt

def cdf(law, scale="linear"):
    """Plot the cdf of the probability law of the number of desynchronization.

    :param law: Probability law of the number of desynchronization.
    :type law: spistats.desynchronization.NumberOfDsync()
    :param scale: (Optional, default="linear") The scale of the graph. Can only be "linear" at the moment. Log scale is planned for a future version.
    :type scale: string
    """
     
    start,end = law.cdf_position()

    num_samp = 100
    if scale=="linear":
        x = np.unique(np.linspace(start,end,num_samp).astype(int))
        curve = np.zeros(len(x)).astype(float)
        for xi,xx in enumerate(x):
            curve[xi] = law.cdf(xx)
        plt.plot(x,curve)
        plt.show()

    else:
        log_x = np.linspace(np.log(start)/np.log(10),np.log(end)/np.log(10),num_samp)
        curve = np.zeros(num_samp).astype(float)
        for xi,xx in enumerate(10**log_x):
            curve[xi] = law.cdf(xx)

        plt.plot(log_x,curve)

        end_tick = int(np.log(end)/np.log(10))+2
        start_tick = int(np.log(start)/np.log(10))-1
        ticks = np.array([10**n for n in range(start_tick,end_tick)])
        plt.xticks(np.log(ticks)/np.log(10), ticks)
        plt.xticks(rotation=45)
        ax = plt.gca()
        ax.xaxis.set_major_formatter(mtick.ScalarFormatter(useMathText=True))
        labels = [item.get_text() for item in ax.get_xticklabels()]
        for li in range(len(labels)):
            labels[li] = f"10^{labels[li]}"
        ax.set_xticklabels(labels)

        import matplotlib.patches as mpatches
        plt.xlabel("Number of packets sent")
        plt.ylabel("Probability to have lost\nconnection")
        #plt.savefig("packet_loss.pdf", bbox_inches="tight")
        plt.show()

