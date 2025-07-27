from abc import ABC, abstractmethod


class CarparkSensorListener(ABC):
    @abstractmethod
    def incoming_car(self, license_plate):
        pass

    @abstractmethod
    def outgoing_car(self, license_plate):
        pass

    @abstractmethod
    def temperature_reading(self, reading):
        pass


class CarparkDataProvider(ABC):
    @property
    @abstractmethod
    def available_spaces(self):
        pass

    @property
    @abstractmethod
    def temperature(self):
        pass

    @property
    @abstractmethod
    def current_time(self):
        pass
