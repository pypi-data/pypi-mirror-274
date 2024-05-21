LoRaWAN, a widely deployed LPWAN protocol, raises privacy concerns due to metadata exposure, particularly concerning the exploitation of stable device identifiers. For the first time in literature, we propose two privacy-preserving pseudonym schemes tailored for LoRaWAN: resolvable pseudonyms and sequential pseudonyms. We extensively evaluate their performance and applicability through theoretical analysis and simulations based on a large-scale real-world dataset of 71 million messages. We conclude that sequential pseudonyms are the best solution.

This repository analyses the performances of sequential private identifiers: a LoRaWAN privacy orentied communication protocol.

We use efficient numerical methods to compute the mass function and the CDF of streaks of repeating events. The expectation of packet loss is computed using Markov chains for improved performances.

# Research work
This work is based on an extention of the follwoing research paper: https://inria.hal.science/hal-04525080 Please cite this paper if you use this package in your research project.

# Installation 
```bash
pip install spistats
```

# Documentation
The full API documentation is available here https://jaalmoes.com/doc/spistats/.

# Usage
## Generating figures of the paper
```bash
python -m spistats.markov
```
## Collision
```python
import spistats as spi
col = spi.Collision(nbr_dev, nbr_adr, adr_per_dev)
```

## Desynchronization
```python
import spistats.desynchronization as dsync
packet_count = dsync.NumberOfPacketBeforeDsync(0.2,5)
packet_count = dsync.NumberOfPacketBeforeDsync_multi([0.2,0.3],5)
```

## Plotting
```python
import spistats.plot as plt
import spistats.desynchronization as dsync
dsync_count = dsync.NumberOfDsync(0.2,2,10)
plt.cdf(dsync_count)
```

