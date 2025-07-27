import time
from interfaces import CarparkSensorListener, CarparkDataProvider


class MockCarparkManager(CarparkSensorListener, CarparkDataProvider):
    def __init__(self):
        self._temperature = 0
        self._spaces = 1000
        self._max_spaces = 1000
        self._cars_inside = set()  # Track plates of cars currently inside

    @property
    def available_spaces(self):
        return self._spaces

    @property
    def temperature(self):
        return self._temperature

    @property
    def current_time(self):
        return time.localtime()

    def incoming_car(self, license_plate):
        if license_plate in self._cars_inside:
            print(f"Duplicate entry blocked: {license_plate} is already inside.")
            return

        if self._spaces == 0:
            print("Carpark full! Cannot allow more cars in.")
            return

        log = f"[IN] {license_plate} at {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
        print('Car in! ' + license_plate)
        with open("log.txt", "a") as f:
            f.write(log)

        self._spaces -= 1
        self._cars_inside.add(license_plate)

    def outgoing_car(self, license_plate):
        if license_plate not in self._cars_inside:
            print(f"Exit blocked: {license_plate} not found in carpark.")
            return

        log = f"[OUT] {license_plate} at {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
        print('Car out! ' + license_plate)
        with open("log.txt", "a") as f:
            f.write(log)

        self._spaces += 1
        self._cars_inside.remove(license_plate)

    def temperature_reading(self, reading):
        print(f'temperature is {reading}')
        self._temperature = reading
