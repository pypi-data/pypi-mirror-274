"""This packet contains utilities to study the odds of desynchronization in the sequential pseudonym scheme."""

from .law import Law as NumberOfPacketBeforeDsync
from .law_multi import Law_multip as NumberOfPacketBeforeDsync_multi
from .dsync_count import NumberOfDsync
