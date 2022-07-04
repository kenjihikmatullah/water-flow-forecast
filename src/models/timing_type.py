from enum import Enum


class TimingType(Enum):

    # Timing type which simulation is done once (snapshot)
    SINGLE_PERIOD = 'SINGLE_PERIOD'

    # Timing type which simulation is done based on time-series periods
    # e.g. 7 times weekly
    TIME_SERIES = 'TIME_SERIES'
