# EL9115 interactive config


Authors: Prince John, Jon Elson

Interactive configuration tool for EL9115 Analog Video Delay IC series.  

## Configuration Details

The SPI configuration for EL9115 is write only. An 8 bit word must be written in each transaction, I've specified the word structure below.

 Data word: $[b_7 \ b_6 \ b_5 \ b_4 \ b_3 \ b_2 \ b_1 \ b_0]$ 
 
Bit $b_7$ is always 0, bits $b_6$  and $b_5$ are the register address bits, and bits $b_4-b_0$ set the delay value.

Register address map: 
| Register     | $b_6$  $b_5$|
| ----------- | ----------- |
| test      | 0 0 |
| red   | 0 1 |
|green|1 0|
|blue|1 1|

The delay value is set in multiples of 2 ns, with the 5 bit unsigned int multiplication factor set using the bits $b_4-b_0$(MSB is $b_4$).

For example the data word for setting the green channel to 50 ns delay will be : `01011001`


## Usage

Before starting ensure that the `DEV_ENV` variable in the `spi_utilities.py` file within the src directory is set to `FALSE`. 

Start this utility by running the `main.py` file within the src directory.

I've written this tool to be used on a Raspberry Pi 3b+ but should be relatively easy to modify it for any SPI capable device that has the `spidev` python driver wrapper. 
