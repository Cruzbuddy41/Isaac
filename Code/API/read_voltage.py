import spidev
import time
import math

# Open SPI bus
spi = spidev.SpiDev()
spi.open(0, 0)  # Open SPI bus 0, device 0
spi.max_speed_hz = 1000000  # Set SPI clock speed to 1MHz

# --- VOLTAGE DIVIDER CONFIGURATION ---
# IMPORTANT: Adjust these values to match the resistors you used in your voltage divider.
R1 = 10000.0  # Resistance of the resistor connected to the battery (+) in Ohms (e.g., 10kΩ)
R2 = 3300.0  # Resistance of the resistor connected to GND and ADC input in Ohms (e.g., 3.3kΩ)
VOLTAGE_REFERENCE = 3.3  # The voltage supplied to the MCP3008's VREF pin (from Pi's 3.3V pin)

# Calculate the voltage divider ratio
voltage_ratio = (R1 + R2) / R2


def read_adc(channel):
    """
    Reads the analog input value from the specified channel (0-7) of the MCP3008.
    """
    # MCP3008 command format: [start_bit, single_ended_bit + channel, dummy_bits]
    # 1 followed by the channel (e.g., 8 for channel 0, 9 for channel 1)
    command = [1, (8 + channel) << 4, 0]

    # Send the command and receive the data
    r = spi.xfer2(command)

    # Extract the 10-bit analog value from the returned bytes
    # The result is spread across r[1] and r[2]
    adc_out = ((r[1] & 3) << 8) + r[2]
    return adc_out


def convert_to_voltage(adc_value):
    """
    Converts the raw 10-bit ADC value (0-1023) to a real-world voltage.
    """
    # The ADC provides a 10-bit reading (0 to 1023) where 1023 corresponds to the VREF (3.3V)
    # The actual voltage at the ADC input is: (adc_value * VOLTAGE_REFERENCE) / 1023
    # We then multiply by the voltage divider ratio to get the actual battery voltage.
    voltage = (adc_value * VOLTAGE_REFERENCE / 1023.0) * voltage_ratio
    return voltage


try:
    while True:
        # Read the raw value from Channel 0 (adjust as needed if you use a different channel)
        adc_value = read_adc(0)

        # Convert the value to voltage
        battery_voltage = convert_to_voltage(adc_value)

        # Print the result
        print(f"Raw ADC Value: {adc_value}, Battery Voltage: {battery_voltage:.2f} V")

        time.sleep(2)  # Wait for 2 seconds before the next reading

except KeyboardInterrupt:
    # Close the SPI connection when the script is stopped
    spi.close()
