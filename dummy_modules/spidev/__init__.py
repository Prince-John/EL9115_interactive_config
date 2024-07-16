class SpiDev:
    def __init__(self):
        self.mode = 0
        self.speed_hz = 0

    def open(self, bus, device):
        print(f"Dummy SpiDev: Pretending to open SPI device on bus {bus}, device {device}")

    def xfer2(self, data):
        formatted_data = [f"{byte:08b}({byte})" for byte in data]
        print(f"Dummy SpiDev: Pretending to transfer data {formatted_data}")
        return data  # Return the same data for simplicity

    def close(self):
        print("Dummy SpiDev: Pretending to close SPI device")
