from time import sleep
import spi_utilities
from interface_utilities import *

DEV_ENV = False

# Setup GPIO for Chip Select (CS)
cs_pin = 8


def main():
    chip = spi_utilities.el9115(cs_pin)

    try:
        while True:

            choice = show_menu()

            if choice == '1':
                set_delay_one_color('red', chip)

            elif choice == '2':
                set_delay_one_color('green', chip)

            elif choice == '3':
                set_delay_one_color('blue', chip)

            elif choice == '4':
                set_delay_all(chip)

            elif choice == '5':
                emulate_reset(chip)

            elif choice == '6':
                chip.view_current_configuration()

            elif choice == '7':
                print("CAUTION: Direct writes will not be reflected in the current configuration dictionary!!!")
                data = int(input("Enter 8-bit word to write in binary    "), base=0)
                chip.write_register(data)

            elif choice == '8':
                print("Exiting!")
                break

            else:
                print("Invalid choice. Please select an option between 1 and 8.")

    except KeyboardInterrupt:
        print("\nExiting due to user interruption.")
    finally:
        chip.close()


if __name__ == "__main__":
    main()
