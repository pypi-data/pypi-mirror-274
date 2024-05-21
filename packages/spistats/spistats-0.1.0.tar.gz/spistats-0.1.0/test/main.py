import spistats as spi
import spistats.desynchronization as dsync
import spistats.plot as plt


#Number of devices in the network
nbr_dev = 100
#Number avialable addresses
nbr_adr = 2**12
#Number of addresses per device 
adr_per_dev = 10

col = spi.Collision(nbr_dev, nbr_adr, adr_per_dev)

#packet_count = dsync.NumberOfPacketBeforeDsync(0.2,5)
#packet_count = dsync.NumberOfPacketBeforeDsync_multi([0.2,0.3],5)

dsync_count = dsync.NumberOfDsync(0.2,2,10)
#print(dsync_count.mass(99))
plt.cdf(dsync_count)

quit()
import numpy as np
print((dsync_count.c>0.00000001).astype(int))
