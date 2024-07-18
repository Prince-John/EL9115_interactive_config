import json

DEV_ENV = True
if DEV_ENV:
    from dummy_modules import spidev
    from dummy_modules import RPi as GPIO
else:
    import RPi.GPIO as GPIO
    import spidev


class BitSequenceEncoder(json.JSONEncoder):
    """
    Function to override the default json encoder to show register data in binary.
    Note: This function was generated using ChatGPT-4o on July 15, 24. Might behave unexpectedly.
    """
    def encode(self, obj):
        def convert_bits(item):
            if isinstance(item, dict):
                return {k: convert_bits(v) if k != 'bits' else f'{v:08b}' for k, v in item.items()}
            return item

        converted_obj = convert_bits(obj)
        return super(BitSequenceEncoder, self).encode(converted_obj)


class el9115:

    def __init__(self, cs_pin, max_speed_in_hz=50000):
        """
        SPI interface object with the EL9115 ic
        :param cs_pin: GPIO pin on RPi used as cs, default is 8. Datasheet calls this NSENABLE
        :param max_speed_in_hz: max SPI bus speed, default is 50 kHz.
        """
        self.spi = spidev.SpiDev()
        self.cs_pin = cs_pin
        self.max_speed_hz = max_speed_in_hz
        self.register_map = dict(red=1, green=2, blue=3, test=0)
        self.configuration = {color: {'delay': 0, 'bits': self.assemble_command_byte(color, 0)}
                              for color in self.register_map.keys()}
        self.initialize_hardware()

    def initialize_hardware(self):
        """
        Sets up the raspberry pi hardware gpio and spi bus
        :return: None
        """

        # GPIO Setup
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.cs_pin, GPIO.OUT, initial=GPIO.HIGH)

        self.spi.open(0, 0)  # Open SPI bus 0, device 0
        self.spi.max_speed_hz = self.max_speed_hz  # SPI speed
        self.spi.mode = 0b01  # SPI clock phase mode, SCLK is low before CS/ is pulled low, Data is shifted out at
        # the rising edge and sampled on the falling edge.

    def assemble_command_byte(self, color, delay_multiplier):
        """
        Assembles the 8 bit word that is sent over SPI to configure the delay

        :param color: channel color(red, green, blue, or test)
        :param delay_multiplier: delay multiplication factor from 0-31, delays in multiples of 2ns.

        :raises: ValueError: if color or delay_multiplier is out of bounds.

        """
        if color not in self.register_map:
            raise ValueError("Not a valid color")

        if not isinstance(delay_multiplier, int) or delay_multiplier < 0 or delay_multiplier > 31:
            raise ValueError("delay_multiplier must be an integer between 0 and 31")

        command_byte = 0x7F & (self.register_map[color] << 5) | delay_multiplier

        return command_byte

    def write_register(self, data):
        """
        Creates the SPI call to write the assembled data byte to EL9115.

        :param data: A valid 8-bit data word with channel address and delay code
        :return: None
        """

        GPIO.output(self.cs_pin, GPIO.LOW)  # Enable communication
        self.spi.xfer2([data])  # Send the command and value
        GPIO.output(self.cs_pin, GPIO.HIGH)  # Disable communication

    def set_delay(self, color, delay):
        """
        Sets the required delay to the specified channel.

        :param color: channel color
        :param delay: delay in ns, if not a multiple of 2ns it rounds down to the nearest multiple.
        :return: None
        :raises: ValueError: if color or delay_multiplier is out of bounds.

        """

        delay_multiplier = delay // 2
        data_word = self.assemble_command_byte(color, delay_multiplier)
        self.configuration[color]["delay"] = delay
        self.configuration[color]["bits"] = data_word
        self.write_register(data_word)

    def view_current_configuration(self):
        """
        Prints out the current configuration
        :return: None
        """
        print(json.dumps(self.configuration, cls=BitSequenceEncoder, indent=4))

    def close(self):
        """
        Graceful exit for the SPI bus and GPIO connections.
        :return: None
        """
        self.spi.close()
        GPIO.cleanup()
