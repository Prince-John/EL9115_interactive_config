from time import sleep
import spi_utilities

DEV_ENV = False

# Setup GPIO for Chip Select (CS)
cs_pin = 8


def show_menu():
    """Display the config menu and get user choice."""
    menu = """
-----------------------------------------------------------
EL9115 CHIP INTERFACE MENU
-----------------------------------------------------------
    1. Set Delay Red   - Ch-A
    2. Set Delay Green - Ch-B
    3. Set Delay Blue  - Ch-C
    4. Set Delay on all channels
    5. Reset
    6. View Current Delays
    7. Debug Mode - Direct register write
    8. Exit


Enter your choice (1-8): """

    return input(menu)


def get_integer_input(prompt="Enter a number: "):
    while True:
        user_input = input(prompt)
        try:
            # Attempt to convert the user input to an integer
            user_input_int = int(user_input)

            return user_input_int
        except ValueError:
            # If conversion fails, inform the user and prompt again
            print("Invalid input. Please enter a valid integer.")


def get_delay_input():
    delay = get_integer_input("Enter delay in ns up to 62ns, if not a multiple of 2ns it rounds down to the "
                              "nearest multiple:\t")
    if delay > 62 or delay < 0:
        # print("invalid choice choose a valid delay")
        # Not the best solution but this bodge forces the IC object to throw an error and prevents any SPI writes.
        return -1
    return delay


def set_delay_one_color(color, _chip):
    delay = get_delay_input()
    try:
        _chip.set_delay(color, delay)
    except ValueError as e:
        print(f"Configuration Failed, IC object raised error: {e}")


def set_delay_all(_chip):
    delay = get_delay_input()
    try:
        _chip.set_delay('red', delay)
        _chip.set_delay('green', delay)
        _chip.set_delay('blue', delay)
    except ValueError as e:
        print(f"Configuration Failed, IC object raised {e}")


def emulate_reset(_chip):
    """
    Our EL9115 eval board does not have a way to physically reset the IC. This call emulates a reset by setting the
    delay on all channels to zero. Also sets the test mode register to zero.

    :param _chip: SPI interface object for the EL9115 ic
    :return: None

    """

    delay = 0
    try:
        _chip.set_delay('red', delay)
        _chip.set_delay('green', delay)
        _chip.set_delay('blue', delay)
        _chip.set_delay('test', 0)

    except ValueError as e:
        print(f"Configuration Failed, IC object raised {e}")


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
