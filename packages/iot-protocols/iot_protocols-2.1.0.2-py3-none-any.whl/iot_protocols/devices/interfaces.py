from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict, List

from iot_protocols.data import RelayState, IOState, Serie


class Relay(ABC):

    @abstractmethod
    def read_relay(self) -> RelayState:
        """ Read current Relay State"""

    @abstractmethod
    def set_relay(self, value: RelayState) -> None:
        """ Set the current relay state value """


class RelayArray(ABC):

    @abstractmethod
    def read_relay_array(self) -> List[RelayState]:
        """ Read the relay array values """

    @abstractmethod
    def set_relay_array(self, value: List[RelayState]) -> None:
        """ Set the current relay array state """


class IO(ABC):

    @abstractmethod
    def read_io(self):
        """ Must read IO state """


class IOArray(ABC):

    @abstractmethod
    def read_io_array(self) -> List[IOState]:
        """ Read the current io array """



class EnergyMeter(ABC):

    @abstractmethod
    def read_energy(self, **kwargs) -> Dict:
        """
        Read the energy data from the meter and returns it.
        """
