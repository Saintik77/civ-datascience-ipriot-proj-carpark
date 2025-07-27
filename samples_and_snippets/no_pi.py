import tkinter as tk
import time


class CarParkDisplay(tk.LabelFrame):
    def __init__(self, master):
        super().__init__(master, text="Carpark Info")
        self.available_var = tk.StringVar()
        self.temp_var = tk.StringVar()
        self.time_var = tk.StringVar()

        self.available_label = tk.Label(self, textvariable=self.available_var)
        self.temp_label = tk.Label(self, textvariable=self.temp_var)
        self.time_label = tk.Label(self, textvariable=self.time_var)

        self.available_label.pack()
        self.temp_label.pack()
        self.time_label.pack()

        self._provider = None
        self.update_display()

    def set_data_source(self, provider):
        self._provider = provider

    def update_display(self):
        if self._provider:
            self.available_var.set(f"Available Spaces: {self._provider.available_spaces}")
            self.temp_var.set(f"Temperature: {self._provider.temperature}°C")
            self.time_var.set(time.strftime("Time: %H:%M:%S", self._provider.current_time))
        self.after(1000, self.update_display)


class CarDetectorWindow(tk.LabelFrame):
    def __init__(self, master):
        super().__init__(master, text="Car Detector")

        self.temp_label = tk.Label(self, text="Temperature:")
        self.temp_entry = tk.Entry(self)
        self.temp_button = tk.Button(self, text="Set Temp", command=self.set_temperature)

        self.plate_label = tk.Label(self, text="License Plate:")
        self.plate_entry = tk.Entry(self)
        self.incoming_button = tk.Button(self, text="Incoming", command=self.incoming_car)
        self.outgoing_button = tk.Button(self, text="Outgoing", command=self.outgoing_car)

        self.temp_label.grid(row=0, column=0)
        self.temp_entry.grid(row=0, column=1)
        self.temp_button.grid(row=0, column=2)

        self.plate_label.grid(row=1, column=0)
        self.plate_entry.grid(row=1, column=1)
        self.incoming_button.grid(row=1, column=2)
        self.outgoing_button.grid(row=1, column=3)

        self.listeners = []
        self.data_display = None

    def add_listener(self, listener):
        self.listeners.append(listener)

    def set_temperature(self):
        try:
            temp = float(self.temp_entry.get())
            self.temperature_changed(temp)
        except ValueError:
            print("Invalid temperature input.")

    def temperature_changed(self, temp):
        for listener in self.listeners:
            listener.temperature_reading(temp)
        if self.data_display and hasattr(self.data_display, 'update_display'):
            self.data_display.update_display()

    def incoming_car(self):
        plate = self.plate_entry.get().strip()
        if plate:
            for listener in self.listeners:
                listener.incoming_car(plate)

    def outgoing_car(self):
        plate = self.plate_entry.get().strip()
        if plate:
            for listener in self.listeners:
                listener.outgoing_car(plate)


if __name__ == "__main__":
    from mocks import MockCarparkManager

    root = tk.Tk()
    root.title("Carpark System")

    display = CarParkDisplay(root)
    display.pack()

    detector = CarDetectorWindow(root)
    detector.pack()

    mock = MockCarparkManager()
    detector.add_listener(mock)
    detector.data_display = display
    display.set_data_source(mock)

    root.mainloop()
